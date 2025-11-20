# System-Architektur: V2 Pipeline

Vollständige Dokumentation der V2 Pipeline-Architektur - ein 3-Agent-System mit deterministic Rendering für intelligente Slide-Generierung.

---

## Übersicht

Die Slide Assistant Architektur besteht aus **5 Hauptkomponenten**:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USER INPUT (Markdown, Stichpunkte, Statistiken)          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. CONTENT ANALYZER AGENT V2 (LLM)                          │
│    └─ Versteht Input, extrahiert Struktur                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. PRESENTATION STRATEGIST AGENT V2 (LLM)                   │
│    └─ Plant Layout, wählt Komponenten-Types                 │
│    └─ FEEDBACK LOOP: Kann Plan anpassen                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. CONTENT GENERATOR AGENT V2 (LLM)                         │
│    └─ Generiert strukturierte Text-Daten (KEIN HTML!)      │
│    └─ Validiert gegen Component-Schemas                     │
│    └─ Feedback zurück an Strategist falls Fehler           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. HTML COMPONENT RENDERER (Jinja2, KEIN LLM)               │
│    └─ Rendert Templates (100% deterministic)                │
│    └─ Wendet Design-System an                               │
│    └─ Speichert Markdown + HTML                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE: HTML + Markdown + Metadaten                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent 1: Content Analyzer V2

**Datei:** `presentation/api/agents/content_analyzer_v2.py`

**Funktion:** Versteht den Benutzer-Input und extrahiert Struktur.

### Aufgaben

1. **Content-Typ Klassifizierung**
   - statistics (€ Mio, %, Zahlen)
   - narrative (Geschichten, Erklärtexte)
   - list (Aufzählungen, Features)
   - quote (Zitate, Testimonials)
   - image (Bilder, Grafiken)
   - mixed (Mehreres kombiniert)
   - phased (Phasen, Timelines)
   - hierarchical (Verschachtelt, Baumstruktur)

2. **Metadaten Extraktion**
   - Schlüsselbotschaften (max. 3)
   - Statistiken & Einheiten
   - Bilder-Referenzen
   - Quellen & Attribution
   - Zeitreferenzen

3. **Sprach-Auto-Detection**
   - Deutsch (de) oder Englisch (en)
   - Mischt Input & Output-Sprache

4. **Qualitäts-Bewertung**
   - Content Density (low, medium, high, too_high)
   - Confidence Score (0.0-1.0)
   - Warnings (z.B. "Zu viel Text")

### Input

```python
{
  "user_input": "Unser Umsatz: €42,5 Mio. Wachstum: +18%. Kunden: 8.500",
  "slide_title": "Geschäftsergebnisse 2024",
  "language": "de"
}
```

### Output (ContentAnalysis)

```json
{
  "content_type": "statistics",
  "key_messages": [
    "Gesamtumsatz im Jahr 2024 betrug €42,5 Millionen",
    "Wir verzeichneten ein Wachstum von 18 Prozent gegenüber dem Vorjahr",
    "Unsere Kundenbasis umfasst 8.500 Unternehmen"
  ],
  "has_statistics": true,
  "has_lists": false,
  "has_quotes": false,
  "has_images": false,
  "confidence_score": 0.95,
  "content_density": "low",
  "recommended_components": 1,
  "warnings": []
}
```

### Pydantic Schema

```python
class ContentAnalysis(BaseModel):
    content_type: Literal["statistics", "narrative", "list", "quote",
                         "image", "mixed", "phased", "hierarchical"]
    key_messages: List[str]  # Max 3
    raw_content: str

    # Flags
    has_statistics: bool
    has_lists: bool
    has_quotes: bool
    has_images: bool
    has_icons: bool

    # Optional metadata
    image_references: Optional[List[str]]
    sources: Optional[List[str]]
    temporal_context: Optional[List[str]]
    phases: Optional[List[PhaseInfo]]

    # Quality
    content_density: Literal["low", "medium", "high", "too_high"]
    confidence_score: float  # 0.0-1.0
    warnings: List[str]
```

---

## Agent 2: Presentation Strategist V2

**Datei:** `presentation/api/agents/presentation_strategist_v2.py`

**Funktion:** Plant die Slide-Layout und wählt Komponenten-Types basierend auf Content-Analyse.

### Aufgaben

1. **Component Selection**
   - Auswahl aus 10 Komponenten-Types
   - Max. 3 Komponenten pro Slide
   - Layout-Position (top, middle, bottom)

2. **Design-System Integration**
   - Liest `design-guide.json` des Themes
   - Respektiert Component-Constraints
   - Wendet Token-System an

3. **Kognitives Load Management**
   - Zu viel Text? Aufteilen
   - Richtige Balance? OK
   - Leere Folie? Mehr Content

4. **Feedback Loop**
   - Wird vom Content Generator aufgerufen, falls Validierung scheitert
   - Kann Plan anpassen & neu planen

### Input

```python
{
  "analysis": ContentAnalysis(...),
  "theme": "github",
  "design_guide": {...}  # Aus design-guide.json
}
```

### Output (PresentationStrategy)

```json
{
  "recommended_components": [
    {
      "type": "stat-grid",
      "content_indices": [0, 1, 2],
      "layout_position": "top"
    }
  ],
  "component_count": 1,
  "layout_strategy": "single_statistics_card_layout",
  "styling_suggestions": [
    "Nutze 4 Stat-Cards für die 4 KPIs",
    "Grüne Farbe für positive Metriken",
    "Subtitle für Währung/Kontext"
  ],
  "reasoning": "Der Input besteht aus reinen Statistiken. Das Stat-Grid Component ist optimal für KPI-Displays. Empfehlung: 1 Component für cleane, fokussierte Folie.",
  "cognitive_load_score": "low"
}
```

### Pydantic Schema

```python
class ComponentRecommendation(BaseModel):
    type: Literal["stat-grid", "bullet-list", "quote", "text",
                  "image", "table", "image-grid", "feature-grid",
                  "process", "process-horizontal"]
    content_indices: List[int]  # Which key_messages to address
    layout_position: Literal["top", "middle", "bottom"]
    structure: Optional[str]

class PresentationStrategy(BaseModel):
    recommended_components: List[ComponentRecommendation]
    component_count: int  # 1-3
    layout_strategy: str
    styling_suggestions: List[str]
    reasoning: str
    cognitive_load_score: Literal["low", "medium", "high", "too_high"]
```

### Layout Strategien

**Single Component Layout**
```
┌──────────────────────┐
│   Slide Title        │
├──────────────────────┤
│                      │
│   [COMPONENT]        │
│                      │
└──────────────────────┘
```

**Two Component Layout (Vertikal)**
```
┌──────────────────────┐
│   Slide Title        │
├──────────────────────┤
│   [COMPONENT 1]      │
├──────────────────────┤
│   [COMPONENT 2]      │
└──────────────────────┘
```

**Three Component Layout (Vertikal)**
```
┌──────────────────────┐
│   Slide Title        │
├──────────────────────┤
│   [COMPONENT 1]      │
├──────────────────────┤
│   [COMPONENT 2]      │
├──────────────────────┤
│   [COMPONENT 3]      │
└──────────────────────┘
```

---

## Agent 3: Content Generator V2

**Datei:** `presentation/api/agents/content_generator_v2.py`

**Funktion:** Generiert strukturierte Text-Daten (KEIN HTML!) basierend auf Plan.

### Aufgaben

1. **Structured Text Generation**
   - Generiert Daten, nicht HTML
   - Respektiert Component-Schemas
   - Pydantic-validiert

2. **Format Specific Output**
   - For `stat-grid`: Statistiken mit Value + Unit + Label
   - For `bullet-list`: Listeneinträge mit 5-7 Items
   - For `quote`: Text + Author
   - For `text`: Mehrere Paragraphen

3. **Language Handling**
   - Generiert in erkannter Input-Sprache
   - Respektiert kulturelle Kontexte

4. **Feedback Integration**
   - Validiert gegen Component-Schema
   - Falls Fehler: Gibt Feedback an Strategist zurück
   - Strategist passt Plan an

### Input

```python
{
  "analysis": ContentAnalysis(...),
  "strategy": PresentationStrategy(...),
  "raw_content": "Umsatz 2024: €42,5 Mio. Wachstum: +18%. Kunden: 8.500",
  "language": "de"
}
```

### Output (FormattedSlide)

```json
{
  "slide_title": "Geschäftsergebnisse 2024",
  "slide_subtitle": null,
  "components": [
    {
      "type": "stat-grid",
      "title": "Unsere Ergebnisse",
      "subtitle": "2024 Jahresvergleich",
      "stats": [
        {
          "value": "€42,5",
          "unit": "Mio",
          "label": "Gesamtumsatz",
          "source": null
        },
        {
          "value": "+18",
          "unit": "%",
          "label": "Wachstum YoY"
        },
        {
          "value": "8.500",
          "label": "Kunden weltweit"
        }
      ]
    }
  ],
  "metadata": {
    "content_type": "statistics",
    "component_count": 1,
    "generated_at": "2025-11-20T10:30:00Z"
  }
}
```

### Pydantic Schema (FormattedSlide)

```python
class StatGrid(BaseModel):
    type: Literal["stat-grid"]
    title: Optional[str]
    subtitle: Optional[str]
    stats: List[Statistic]

class BulletList(BaseModel):
    type: Literal["bullet-list"]
    title: Optional[str]
    subtitle: Optional[str]
    bullets: List[str]  # 5-7 items

class Quote(BaseModel):
    type: Literal["quote"]
    quote_text: str
    quote_author: Optional[str]

# ... weitere Component-Schemas

class FormattedSlide(BaseModel):
    slide_title: str
    slide_subtitle: Optional[str]
    components: List[Union[StatGrid, BulletList, Quote, ...]]
    metadata: SlideMetadata
```

### Feedback Loop

Falls Validierung scheitert:

```
ContentGenerator → Validation Error
       ↓
"Der Stat-Grid braucht min. 2 und max. 6 Stats"
       ↓
Strategist (aufgerufen mit Feedback)
       ↓
Neuer Plan (z.B. switch zu bullet-list)
       ↓
ContentGenerator (Retry)
```

---

## Agent Orchestrator V2

**Datei:** `presentation/api/agents/orchestrator_v2.py`

**Funktion:** Koordiniert alle 3 Agenten + Rendering + File-Service.

### Multi-Provider Support

Der Orchestrator unterstützt mehrere LLM-Provider:

```python
MODEL_TO_PROVIDER = {
    # OpenAI
    "gpt-4o": "openai",
    "gpt-5": "openai",
    "gpt-5-mini": "openai",

    # Anthropic
    "claude-sonnet-4.5": "anthropic",
    "claude-3-5-sonnet": "anthropic",

    # Google
    "gemini-3.0-pro": "google",
    "gemini-2.5-pro": "google",
}
```

### Agent Initialization

```python
def __init__(
    self,
    model: str = "gpt-4o",
    test_mode: bool = False,
    provider: str = None
):
    # Auto-detect provider
    provider = MODEL_TO_PROVIDER.get(model, "openai")

    # Select appropriate agent class
    if provider == "openai":
        self.analyzer = ContentAnalyzerAgentV2(model=model)
        self.strategist = PresentationStrategistAgentV2(model=model)
        self.generator = ContentGeneratorAgentV2(model=model)

    elif provider == "anthropic":
        self.analyzer = ContentAnalyzerAgentAnthropic(model=model)
        self.strategist = PresentationStrategistAgentAnthropic(model=model)
        self.generator = ContentGeneratorAgentAnthropic(model=model)

    elif provider == "google":
        self.analyzer = ContentAnalyzerAgentGoogle(model=model)
        self.strategist = PresentationStrategistAgentGoogle(model=model)
        self.generator = ContentGeneratorAgentGoogle(model=model)

    # Test mode
    if test_mode:
        self.analyzer = MockContentAnalyzer()
        self.strategist = MockStrategist()
        self.generator = MockGenerator()
```

### Generation Flow

```python
def generate_slide(self, user_input, project_name, slide_title, theme, ...):
    # Step 1: Analyze
    analysis = self.analyzer.analyze(user_input)

    # Step 2: Plan
    strategy = self.strategist.plan(analysis, theme)

    # Step 3: Generate (with feedback loop)
    max_iterations = 3
    for iteration in range(max_iterations):
        formatted_slide = self.generator.generate(
            analysis,
            strategy,
            user_input
        )

        # Validate
        if self.is_valid(formatted_slide):
            break

        # Feedback loop
        feedback = self.get_feedback(formatted_slide)
        strategy = self.strategist.replan(
            analysis,
            feedback=feedback
        )

    # Step 4: Render (Jinja2)
    html = self.renderer.render(formatted_slide, theme)
    markdown = self.convert_to_markdown(formatted_slide)

    # Step 5: Save
    file_service.save(html, markdown, project_name, slide_title)

    return {
        "success": True,
        "html_content": html,
        "markdown_content": markdown,
        "feedback_iterations": iteration
    }
```

---

## Component Renderer (Jinja2)

**Datei:** `presentation/api/renderers/component_renderer.py`

**Funktion:** Rendert FormattedSlide zu HTML mit 100% Determinismus.

### Templates

Jinja2-Templates für jede Komponente in:
```
presentation/templates/components/
├── stat-grid.html.j2
├── bullet-list.html.j2
├── quote.html.j2
├── text.html.j2
├── table.html.j2
├── image-frame.html.j2
├── image-grid.html.j2
├── feature-grid.html.j2
├── process.html.j2
└── process-horizontal.html.j2
```

### Template Beispiel: stat-grid.html.j2

```jinja2
{% if title %}
  <h2>{{ title }}</h2>
{% endif %}
{% if subtitle %}
  <p>{{ subtitle }}</p>
{% endif %}

<div class="stat-grid">
{% for stat in stats %}
  <div class="stat-card">
    <span class="stat-number">
      {{ stat.value }}
      {% if stat.unit %}<span class="unit">{{ stat.unit }}</span>{% endif %}
    </span>
    <span class="stat-label">
      {{ stat.label }}
      {% if stat.source %}<br>({{ stat.source }}){% endif %}
    </span>
  </div>
{% endfor %}
</div>
```

### Rendering Process

```python
class HTMLComponentRenderer:
    def __init__(self, theme, design_guide):
        self.theme = theme
        self.design_guide = design_guide
        self.jinja_env = Environment(loader=FileSystemLoader('templates'))

    def render(self, formatted_slide, theme):
        html_parts = []

        # Title
        html_parts.append(f"<h1>{formatted_slide.slide_title}</h1>")

        if formatted_slide.slide_subtitle:
            html_parts.append(f"<h2>{formatted_slide.slide_subtitle}</h2>")

        # Components
        for component in formatted_slide.components:
            component_html = self.render_component(component, theme)
            html_parts.append(component_html)

        # Wrap in slide
        return self.wrap_slide(html_parts, theme)

    def render_component(self, component, theme):
        template_name = f"{component.type}.html.j2"
        template = self.jinja_env.get_template(template_name)

        # Convert component to dict for Jinja2
        component_data = component.model_dump()

        # Apply design tokens from design-guide.json
        tokens = self.design_guide.get('tokens', {})
        component_data['tokens'] = tokens

        # Render
        return template.render(**component_data)
```

### Design System Integration

`design-guide.json` definiert:

```json
{
  "tokens": {
    "primary-color": "#238636",
    "text-color": "#c9d1d9",
    "font-family": "sans-serif",
    "spacing": "20px"
  },
  "components": {
    "stat-grid": {
      "max_items": 6,
      "layout": "grid",
      "css_class": "stat-grid"
    }
  }
}
```

---

## File Service

**Datei:** `presentation/api/services/file_service.py`

**Funktion:** Speichert generierte Dateien und verwaltet Backups.

### Speicherung

```
projects/beispiel-projekt/
├── markdown/
│   ├── input/          # Original-Markdown (von Benutzern)
│   └── optimized/      # AI-Generierte Markdown
│       ├── folie-01-...md
│       ├── folie-02-...md
│       └── folie-46-geschaeftsergebnisse.md
├── html/
│   ├── folie-01-...html
│   ├── folie-02-...html
│   └── folie-46-geschaeftsergebnisse.html
├── images/
│   └── uploads/
│       ├── chart-sales.png
│       └── team-photo.jpg
└── styles/
    ├── github/
    │   ├── design-guide.json
    │   ├── style.css
    │   └── variables.css
    ├── modern/
    └── minimal/
```

### Backup Strategie

```python
def save(self, html, markdown, project_name, slide_title):
    # Create paths
    md_path = self.get_markdown_path(project_name, slide_title)
    html_path = self.get_html_path(project_name, slide_title)

    # Backup if exists
    if os.path.exists(md_path):
        backup_path = f"{md_path}.backup-{timestamp}"
        shutil.copy(md_path, backup_path)

    # Save
    write_file(md_path, markdown)
    write_file(html_path, html)

    return {
        "markdown_path": md_path,
        "html_path": html_path
    }
```

---

## API Routes

**Datei:** `presentation/api/routes/v2.py`

**Funktion:** HTTP-Endpoint für Slide-Generierung.

### POST /api/v2/generate

```python
@router.post("/api/v2/generate")
async def generate_slide_v2(request_data: Dict[str, Any]):
    # Extract parameters
    project_name = request_data["project_name"]
    user_input = request_data["user_input"]
    theme = request_data.get("theme", "github")
    language = request_data.get("language", "de")
    model = request_data.get("model", DEFAULT_MODEL)

    # Auto-detect provider
    provider = MODEL_TO_PROVIDER.get(model, "openai")

    # Initialize orchestrator
    orchestrator = AgentOrchestratorV2(
        model=model,
        provider=provider,
        test_mode=TEST_MODE
    )

    # Generate
    result = orchestrator.generate_slide(
        user_input=user_input,
        project_name=project_name,
        slide_title=slide_title,
        theme=theme,
        language=language
    )

    return result
```

---

## Data Flow Diagram

```
USER INPUT
    │
    ▼
┌──────────────────────────────────────┐
│ CONTENT ANALYZER V2                  │
│ - Klassifiziert Content-Typ          │
│ - Extrahiert Metadaten               │
│ → ContentAnalysis (Pydantic)         │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ PRESENTATION STRATEGIST V2           │
│ - Plant Layout                       │
│ - Wählt Komponenten                  │
│ - Liest design-guide.json            │
│ → PresentationStrategy (Pydantic)    │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ CONTENT GENERATOR V2                 │
│ - Generiert Daten (KEIN HTML)        │
│ - Respektiert Strategy               │
│ - Validiert gegen Schemas            │
│ → FormattedSlide (Pydantic) oder     │
│   → FEEDBACK an Strategist           │
└──────────┬───────────────────────────┘
           │
           ├─────────────────────────┐
           │ [Wenn Validierung OK]   │
           ▼                         │
┌──────────────────────────────────────┐
│ HTML COMPONENT RENDERER (Jinja2)     │
│ - Template: component-type.html.j2   │
│ - Wendet Design-Tokens an            │
│ - Deterministic HTML Output          │
│ → HTML String                        │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ MARKDOWN CONVERTER                   │
│ - Konvertiert FormattedSlide zu MD   │
│ → Markdown String                    │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ FILE SERVICE                         │
│ - Speichert HTML & Markdown          │
│ - Erstellt Backups                   │
│ → Saved files in projects/           │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ API RESPONSE                         │
│ {                                    │
│   "success": true,                   │
│   "html_content": "...",             │
│   "markdown_content": "...",         │
│   "saved_files": {...},              │
│   "feedback_iterations": 0           │
│ }                                    │
└──────────────────────────────────────┘
```

---

## Feedback Loop Example

### Scenario: Initial Plan ist zu viel Content

```
1. USER INPUT
   "Wir haben 1000 neue Kunden, 50 neuen Features,
    und sind jetzt in 25 Ländern. Unser Support-Team
    wuchs um 200 Prozent."

2. ANALYZER
   content_type: "mixed"
   content_density: "too_high"
   warning: "Zu viel Informationen für eine Folie"
   recommended_components: 1

3. STRATEGIST (Iteration 1)
   Plan A: 3 Components
   - bullet-list mit 4 Items
   - stat-grid mit 3 Metriken
   - bullet-list mit Features

4. GENERATOR (Iteration 1) - VALIDATION FAILS
   Error: "Max 3 Features pro bullet-list, aber 50 gegeben"

5. STRATEGIST (Iteration 2 - mit Feedback)
   Feedback: "Zu viele Features. Fokus auf Top 3 Features,
             rest ignorieren."

   Plan B: 1 Component (vereinfacht)
   - stat-grid mit 3 KPIs (Kunden, Länder, Support)

6. GENERATOR (Iteration 2) - SUCCESS
   FormattedSlide:
   {
     "type": "stat-grid",
     "stats": [
       {"value": "1.000", "label": "Neue Kunden"},
       {"value": "25", "label": "Länder", "unit": "global"},
       {"value": "+200%", "label": "Support-Team Wachstum"}
     ]
   }

7. RENDERER
   HTML mit designertem stat-grid

8. RESPONSE
   feedback_iterations: 1
```

---

## Performance Optimization

### Token Usage (Pro Slide)

| Provider | Model | Tokens | Time | Cost |
|----------|-------|--------|------|------|
| OpenAI | gpt-4o | ~2,000 | 3-5s | ~$0.02 |
| OpenAI | gpt-5 | ~3,000 | 8-12s | ~$0.05 |
| Anthropic | claude-sonnet-4.5 | ~2,500 | 4-6s | ~$0.01 |
| Google | gemini-3.0-pro | ~2,000 | 3-5s | ~$0.005 |

### Caching Opportunities (kommend)

1. **Design-Guide Caching** - design-guide.json wird geladen einmal pro Theme
2. **Template Caching** - Jinja2 Templates werden compiled
3. **Semantic Caching** - Ähnliche Inputs → ähnliche Outputs
4. **Component Library** - Häufig verwendete Patterns speichern

---

## Testing & Mock Mode

### TEST_MODE in config.py

```python
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

if TEST_MODE:
    # Use mock agents (no API calls)
    from agents.mock_agents_v2 import (
        MockContentAnalyzer,
        MockStrategist,
        MockGenerator
    )
```

### Mock Agents

```python
class MockContentAnalyzerV2:
    def analyze(self, user_input):
        # Return hardcoded response
        return ContentAnalysis(
            content_type="statistics",
            key_messages=["Mock message 1", "Mock message 2"],
            has_statistics=True,
            confidence_score=0.95,
            # ... more fields
        )
```

### Running in Test Mode

```bash
cd presentation/api
export TEST_MODE=true
python3 -m pytest test_agents_v2.py -v
```

---

## Design System

### design-guide.json Struktur

```json
{
  "name": "GitHub Design",
  "version": "2.0",

  "tokens": {
    "colors": {
      "primary": "#238636",
      "text": "#c9d1d9",
      "border": "#30363d"
    },
    "typography": {
      "family": "sans-serif",
      "size": {
        "base": "15px",
        "lg": "18px"
      }
    },
    "spacing": {
      "unit": "8px",
      "gap": "20px"
    }
  },

  "components": {
    "stat-grid": {
      "max_items": 6,
      "layout": "grid",
      "grid_columns": "auto-fit, minmax(200px, 1fr)"
    },
    "bullet-list": {
      "max_items": 7,
      "min_items": 2
    }
  },

  "layouts": {
    "single": {
      "title": "Single Component",
      "components": 1,
      "description": "Fokussierte Folie mit einer Komponente"
    }
  }
}
```

---

## Error Handling

### Agent Errors

```python
try:
    analysis = self.analyzer.analyze(user_input)
except OpenAIError as e:
    return {
        "success": False,
        "error": f"OpenAI API error: {str(e)}",
        "provider": "openai"
    }
```

### Validation Errors

```python
try:
    formatted_slide = FormattedSlide(**data)
except ValidationError as e:
    # Trigger feedback loop
    feedback = extract_feedback_from_error(e)
    strategy = self.strategist.replan(..., feedback=feedback)
```

### File Errors

```python
try:
    self.file_service.save(html, markdown, ...)
except IOError as e:
    return {
        "success": False,
        "error": f"File save failed: {str(e)}"
    }
```

---

## Extensibility

### Adding New Component Type

1. **Create Template:** `presentation/templates/components/newtype.html.j2`
2. **Create Pydantic Schema:** `presentation/api/agents/schemas.py`
3. **Update Strategist:** Add to component selection logic
4. **Update Generator:** Add generation logic
5. **Update design-guide.json:** Add component definition
6. **Test:** Add unit & integration tests

### Adding New Provider

1. **Create Agent Classes:**
   - `content_analyzer_{provider}.py`
   - `presentation_strategist_{provider}.py`
   - `content_generator_{provider}.py`

2. **Update Orchestrator:** Add import & provider routing

3. **Update config.py:** Add model mappings

4. **Test:** Integration tests with real API

---

## Monitoring & Logging

### Key Metrics

```python
logging.info(f"Generation started: {project_name}/{slide_title}")
logging.info(f"Content type: {analysis.content_type}")
logging.info(f"Components: {strategy.component_count}")
logging.info(f"Generation time: {time_ms}ms")
logging.info(f"Feedback iterations: {feedback_iterations}")
```

### Performance Monitoring

```python
start_time = time.time()

# Step 1: Analyze
analysis = self.analyzer.analyze(user_input)
logging.info(f"Analysis: {time.time() - start_time:.2f}s")

# Step 2: Plan
strategy = self.strategist.plan(analysis, theme)
logging.info(f"Planning: {time.time() - start_time:.2f}s")

# ... etc
```

---

## Verwandte Dokumentation

- **[API Endpoints](endpoints.md)** - HTTP-Schnittstelle
- **[Komponenten-Referenz](components.md)** - Alle Component-Types
- **[Erste Folie Tutorial](../guides/first-slide-tutorial.md)** - Praktische Beispiele
- **[CLAUDE.md](../../CLAUDE.md)** - Projekt-Übersicht

---

**Version:** 2.0 (Deterministic, Multi-Provider)
**Zuletzt aktualisiert:** 2025-11-20
**Status:** Production-Ready

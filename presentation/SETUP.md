# Slide Assistant - Setup Guide

Willkommen beim AI-powered Slide Assistant! Diese Anleitung führt dich durch die Installation und Einrichtung der V2-Architektur.

## 📋 Übersicht

Das System besteht aus:
- **Frontend**: `unified-editor.html` - Integrierter Editor mit Live-Preview
- **Backend**: FastAPI Server mit V2 Multi-Agent-Architektur
- **Templates**: Jinja2-basierte deterministische HTML-Generierung
- **LLM Integration**: OpenAI GPT-4o/GPT-5 (oder Mock-Modus für Entwicklung)

## 🚀 Quick Start (5 Minuten)

### 1. Virtual Environment erstellen

```bash
cd presentation/api
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# oder auf Windows: venv\Scripts\activate
```

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. Umgebung konfigurieren

```bash
cp .env.example .env
# Editiere .env und füge OPENAI_API_KEY hinzu
# ODER setze TEST_MODE=true für Entwicklung
```

### 4. API starten

```bash
# Vom presentation/ Ordner:
cd ..
python3 run_api.py
```

Server läuft unter: `http://localhost:8001`

### 5. Unified Editor öffnen

```bash
# Option 1: File-Protokoll (kann CORS-Probleme haben)
open unified-editor.html

# Option 2: Mit lokalem Server (empfohlen)
python3 -m http.server 8000
# Dann: http://localhost:8000/unified-editor.html
```

## ⚙️ Konfiguration

### Umgebungsvariablen (`.env`)

Erstelle `presentation/api/.env`:

```env
# Für Entwicklung (Standard)
TEST_MODE=true

# Für Produktion mit OpenAI
OPENAI_API_KEY=sk-your-key-here
TEST_MODE=false
DEFAULT_MODEL=gpt-4o  # oder gpt-5, gpt-5-mini
```

**TEST_MODE aktivieren (empfohlen für Entwicklung):**
- ✅ Nutzt Mock Agents statt echtem OpenAI
- ✅ Keine API Kosten
- ✅ Schnelle Entwicklung
- ✅ Deterministisches Testing
- ❌ Keine echten AI-Generierungen

**Für echte OpenAI Integration:**
1. API Key von [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) holen
2. In `.env` setzen: `OPENAI_API_KEY=sk-...`
3. Setzen: `TEST_MODE=false`

## 📁 Projektstruktur

```
presentation/
├── unified-editor.html           # Hauptanwendung (NEU!)
├── run_api.py                    # API Starter Script
├── api/                          # Backend V2
│   ├── main.py                   # FastAPI Server
│   ├── config.py                 # Konfiguration
│   ├── agents/                   # V2 Agenten
│   │   ├── orchestrator.py       # Agent-Koordinator
│   │   ├── content_analyzer_v2.py
│   │   ├── presentation_strategist_v2.py
│   │   ├── content_generator_v2.py
│   │   └── mock_agents_v2.py     # Mock Agents für TEST_MODE
│   ├── renderers/                # HTML-Rendering
│   │   └── component_renderer.py # Jinja2-Renderer
│   ├── routes/                   # API Endpoints
│   │   └── v2.py                 # V2 Endpoints
│   ├── services/                 # Services
│   │   ├── file_service.py
│   │   ├── project_service.py
│   │   ├── style_parser.py
│   │   └── template_loader.py
│   ├── tests/                    # Test Suite
│   └── requirements.txt          # Dependencies
├── templates/                    # Jinja2 Templates
│   ├── components/               # Component Templates (10 Typen)
│   └── wrappers/                 # Wrapper Templates
└── projects/
    └── beispiel-projekt/
        ├── markdown/
        │   ├── input/
        │   └── optimized/        # Generated Slides
        ├── html/                 # Generated HTML
        ├── images/uploads/       # Uploaded Images
        └── styles/               # Design Themes
            ├── github/
            ├── modern/
            └── minimal/
```

## 💬 Wie du es nutzt

### Unified Editor Features

Der **unified-editor.html** kombiniert alle Funktionen:

**Links (Input):**
- Projekt-Auswahl
- Slide-Titel eingeben
- Folien-Nummer setzen
- Freier Text-Input
- Theme-Auswahl (GitHub/Modern/Minimal)

**Rechts (Preview):**
- Live HTML-Rendering mit echtem CSS
- Theme-Switch ohne Page-Reload
- Export-Funktionen
- Regenerierung mit Feedback

**Features:**
- Side-by-side Layout für bessere Übersicht
- Kompakte Komponenten-Anzeige
- Live Preview während Generierung
- Theme-Switcher
- Slide-Management

### Schritt-für-Schritt

#### 1. Projekt wählen

Wähle aus der Dropdown-Liste (z.B. "beispiel-projekt")

#### 2. Slide-Info eingeben

```
Slide-Titel: Folie 12: Team-Übersicht
Slide-Nummer: 12
```

#### 3. Content eingeben

**Stichpunkte:**
```
- 5 erfahrene Experten
- 20+ Jahre kombinierte Erfahrung
- Standorte: Berlin & München
```

**Strukturierter Text:**
```
Unser Team besteht aus 5 erfahrenen Experten mit über 20 Jahren
kombinierter Erfahrung in der Softwareentwicklung. Wir haben
Standorte in Berlin und München.
```

**Statistiken:**
```
- 5 Team-Mitglieder
- 20+ Jahre Erfahrung
- 100% Remote-fähig
```

#### 4. Theme auswählen

- **GitHub** (Default) - Clean, professional
- **Modern** - Contemporary styling
- **Minimal** - Simplified design

#### 5. Generieren

1. "Generate" Button klicken
2. Warte 3-5 Sekunden (V2 ist schnell!)
3. Live-Preview zeigt Ergebnis

#### 6. Review & Export

- Prüfe Preview rechts
- Nutze Theme-Switch zum Vergleichen
- Export als HTML oder Screenshot

## 🔧 V2 Agent Chain (Architektur)

```
User Input
    ↓
Agent 1: Content Analyzer (1-2s)
  └─ Analysiert Input-Typ
  └─ Erkennt Sprache (DE/EN)
  └─ Identifiziert Content-Blöcke
    ↓
Agent 2: Presentation Strategist (1-2s) ←──┐ Feedback Loop
  └─ Plant Component-Typen                 │ (bei Validation-Fehler)
  └─ Referenziert design-guide.json        │
  └─ Erstellt Slide-Blueprint              │
    ↓──────────────────────────────────────┘
Agent 3: Content Generator (1-2s)
  └─ Generiert FormattedSlide (pure data, KEIN HTML!)
  └─ Validiert gegen Pydantic schemas
    ↓
Jinja2 Renderer (<1s)
  └─ Lädt Templates
  └─ Rendert HTML deterministisch
  └─ Wendet Theme-Tokens an
    ↓
HTML + Markdown Output

Total: ~3-5s (V2 ist 3-4x schneller als V1!)
```

## 📂 Generierte Dateien

Nach der Generierung entstehen:

```
projects/beispiel-projekt/
├── markdown/optimized/folie-12-team-übersicht.md  # Markdown Source
└── html/folie-12-team-übersicht.html              # Rendered HTML
```

Diese kannst du:
- Im unified-editor.html live bearbeiten
- In PowerPoint als Screenshots einfügen
- Weiter manuell anpassen
- Für Dokumentation verwenden

## ❌ Fehlerbehandlung

### "OPENAI_API_KEY not found"
**Solution**: Setze `TEST_MODE=true` in `presentation/api/.env`

### "Connection refused"
**Solution**: API Server läuft nicht
```bash
cd presentation
python3 run_api.py
```

### "Template not found"
**Solution**: Templates sind in `presentation/templates/`, nicht `presentation/api/templates/`

### "Module import error"
**Solution**: Stelle sicher, dass `__init__.py` in `api/schemas/` und `api/tests/` existiert

### "Tests failing"
**Solution**: Nutze TEST_MODE für Development
```bash
cd presentation/api
export TEST_MODE=true
python3 -m pytest tests/ -v
```

## 🧪 Testing

### Quick Test (Mock Mode)

```bash
cd presentation/api
export TEST_MODE=true
python3 -m pytest tests/ -v
```

### Test einzelne Components

```bash
# Renderer Tests
python3 -m pytest tests/test_renderer_fix.py -v

# Agent Tests
python3 -m pytest tests/test_agents_v2.py -v

# Integration Tests
python3 -m pytest tests/test_v2_integration.py -v
```

Siehe [TESTING.md](../TESTING.md) für vollständige Test-Dokumentation.

## 🎨 Style Guide Integration

Das System liest automatisch Design Guides:

```
projects/{project}/styles/{theme}/
├── design-guide.json  # Component definitions & tokens
├── design-guide.md    # Human-readable guide
├── style.css          # Theme CSS
└── variables.css      # CSS custom properties
```

Die Agents respektieren diese Vorgaben beim Generieren!

## 📊 API Endpoints

### V2 Endpoints (Current)

```bash
# Generate slide (V2)
curl -X POST http://localhost:8001/api/v2/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "beispiel-projekt",
    "user_input": "...",
    "slide_title": "Folie 12",
    "slide_number": 12,
    "theme": "github",
    "language": "de"
  }'

# Health check
curl http://localhost:8001/health

# List projects
curl http://localhost:8001/api/projects

# Get project info
curl http://localhost:8001/api/projects/beispiel-projekt
```

### Legacy Endpoints (Removed)
- ❌ `/api/generate` → Use `/api/v2/generate`
- ❌ `/api/regenerate` → Merged into `/api/v2/generate`

## 🆘 Support & Troubleshooting

### API lädt nicht
1. Python 3.10+ installiert? `python3 --version`
2. Virtual environment aktiviert? `source api/venv/bin/activate`
3. Port 8001 frei? `lsof -i :8001` (macOS/Linux)

### Frontend zeigt keine Projekte
- Browser-Console öffnen (F12)
- Fetch-Fehler checken
- API läuft unter localhost:8001?

### Generierung dauert zu lange
- **Mit OpenAI API:** 3-5s normal
- **Mit TEST_MODE:** <2s
- **Bei Timeout:** API-Logs prüfen

## 🎯 Next Steps

1. ✅ Setup abgeschlossen
2. 💻 Öffne `unified-editor.html`
3. 🎨 Wähle Projekt & Theme
4. ✍️ Schreibe Test-Content
5. 🚀 Generate!
6. 📊 Teste verschiedene Themes

## 📚 Weitere Dokumentation

- **[CLAUDE.md](../CLAUDE.md)** - Vollständige Projekt-Dokumentation
- **[README.md](../README.md)** - Projekt-Übersicht
- **[TESTING.md](../TESTING.md)** - Test-Guide
- **[api/README.md](api/README.md)** - API-Dokumentation
- **[QUALITY-GUIDE.md](QUALITY-GUIDE.md)** - Qualitätsstandards
- **[MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md)** - V1→V2 Migration

## 🤝 Contributing

### Neue Features hinzufügen

**Neue Component-Type:**
1. Template erstellen: `presentation/templates/components/my-component.html.j2`
2. Schema definieren: `api/agents/schemas.py`
3. Renderer updaten: `api/renderers/component_renderer.py`
4. Tests schreiben: `api/tests/test_template_system.py`

**Neuer Agent:**
1. Agent erstellen: `api/agents/my_agent_v2.py`
2. In Orchestrator integrieren: `api/agents/orchestrator.py`
3. Tests schreiben: `api/tests/test_my_agent.py`

**Frontend Änderungen:**
1. Editiere `unified-editor.html`
2. Teste mit lokalem Server
3. Prüfe Browser-Kompatibilität

## 🔍 Debugging

### Enable Verbose Logging

```python
# In presentation/api/config.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Agent Output

```bash
cd presentation/api
python3 -c "
from agents.orchestrator import AgentOrchestrator
orch = AgentOrchestrator('beispiel-projekt')
result = orch.generate_slide('Test input', 'Folie 1', 1)
print(result)
"
```

### Inspect Templates

```bash
ls -la presentation/templates/components/
# Should show 10 .j2 files
```

## 🎉 Happy Content Generating!

Bei Fragen:
- Check [CLAUDE.md](../CLAUDE.md) für Details
- Review [TESTING.md](../TESTING.md) für Tests
- Siehe [api/README.md](api/README.md) für API-Details

# AI Content Editor - Setup Guide

Willkommen beim AI-powered Content Editor für deinen Slides Helper! Diese Anleitung führt dich durch die Installation und Einrichtung.

## 📋 Übersicht

Das System besteht aus:
- **Frontend**: `ai-editor.html` - Webbasierter Chat-Editor mit Live-Preview
- **Backend**: FastAPI Server mit Multi-Agent-Architektur
- **LLM Integration**: OpenAI GPT-4o (oder Mock-Modus für Entwicklung)

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

### 3. API starten

```bash
# Vom presentation Ordner:
python3 run_api.py
```

Server läuft unter: `http://localhost:8001`

### 4. Editor öffnen

Öffne die Datei `ai-editor.html` im Browser:
```bash
# Option 1: File-Protokoll (funktioniert ohne Server für UI, aber keine Generierung)
open ai-editor.html

# Option 2: Mit lokalem Server (volle Funktionalität)
python3 -m http.server 8000
# Dann: http://localhost:8000/ai-editor.html
```

## ⚙️ Konfiguration

### Umgebungsvariablen (`.env`)

Bereits vorkonfiguriert mit TEST_MODE=true:

```env
# Für echte OpenAI Integration
OPENAI_API_KEY=sk-your-key-here
TEST_MODE=false

# Für Entwicklung (ohne API Key)
TEST_MODE=true
```

**TEST_MODE aktivieren:**
- Nutzt Mock Agents statt echtem OpenAI
- Generiert Dummy-Content für Entwicklung
- Keine API Kosten
- Perfekt zum Testen der UI

**Für echte OpenAI Integration:**
1. API Key von [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) holen
2. In `.env` setzen: `OPENAI_API_KEY=sk-...`
3. Setzen: `TEST_MODE=false`

## 📁 Projektstruktur

```
presentation/
├── api/                          # Backend FastAPI
│   ├── main.py                   # Hauptserver
│   ├── agents/                   # AI Agents
│   │   ├── content_analyzer.py
│   │   ├── presentation_strategist.py
│   │   ├── content_generator.py
│   │   └── mock_agents.py        # Test Agents
│   ├── services/                 # Services
│   │   ├── style_parser.py
│   │   ├── file_service.py
│   │   └── project_service.py
│   └── requirements.txt           # Python Dependencies
├── ai-editor.html                # Frontend Editor
├── run_api.py                    # API Starter Script
├── component-viewer.html         # Klassischer Viewer
└── projects/
    └── beispiel-projekt/
        ├── markdown/
        │   ├── input/
        │   └── optimized/        # Generated Slides
        ├── html/                 # Generated HTML
        └── styles/               # Design System
```

## 💬 Wie du es nutzt

### Schritt 1: Projekt wählen

Öffne `ai-editor.html` und wähle ein Projekt aus der Dropdown-Liste aus.

### Schritt 2: Content eingeben

Im Chat-Panel auf der linken Seite kannst du folgende Formate eingeben:

**Stichpunkte:**
```
- Team: 5 Experten
- 20 Jahre Erfahrung
- Standorte: Berlin & München
```

**Markdown:**
```
# Team

## Komponente 1: Größe
- 5 Experten
- Top-Talent

## Komponente 2: Standorte
- Berlin
- München
```

**Strukturierter Text:**
```
Beschreibe dein Team: 5 erfahrene Experten mit 20 Jahren kombinierter Erfahrung,
basierend in Berlin und München mit weltweiter Präsenz.
```

### Schritt 3: Generieren lassen

1. Text eingeben
2. Slide Title optional setzen
3. "Generate" Button klicken
4. Warten auf Content-Generierung

### Schritt 4: Vorschau & Regenerierung

Im Preview-Panel auf der rechten Seite siehst du:
- Generierte Slide-Titel
- Komponenten-Liste
- Dateipfade

**So regenerierst du mit Feedback:**
1. Feedback eingeben: z.B. "Mach es prägnanter" oder "Füge Statistiken hinzu"
2. "🔄 Regenerate" Button klicken
3. Agent analysiert Feedback und generiert neu

## 🔧 Agent Chain Erklärung

Wenn du Content eingibst, laufen folgende Agenten ab:

```
1. Content Analyzer (5 Sek)
   └─ Analysiert deinen Input
   └─ Erkennt Inhaltstyp (Text, Liste, Statistiken)

2. Presentation Strategist (5 Sek)
   └─ Prüft Design System deines Projekts
   └─ Empfiehlt optimale Komponenten
   └─ Plant Layout

3. Content Generator (10 Sek)
   └─ Generiert Markdown
   └─ Generiert HTML mit CSS-Klassen
   └─ Speichert beide Formate

Total: ~20 Sekunden
```

Alle Schritte siehst du live im Chat-Panel!

## 📂 Generierte Dateien

Nach der Generierung entstehen:

```
projects/beispiel-projekt/
├── markdown/optimized/folie-xyz.md      # Markdown Source
└── html/folie-xyz.html                  # Rendered HTML
```

Diese kannst du:
- Mit [component-viewer.html](component-viewer.html) anschauen
- In PowerPoint importieren
- Manuell editieren
- Weiter verarbeiten

## ❌ Fehlerbehandlung

### "API Key not configured"
- **Solution**: `TEST_MODE=true` in `.env` setzen für Entwicklung

### "Connection refused"
- **Solution**: API Server läuft nicht. Starte `python3 run_api.py`

### "Project not found"
- **Solution**: Wähle ein Projekt aus der Dropdown-Liste

### "Generate button grayed out"
- **Solution**: Warten bis vorherige Generierung abgeschlossen ist

## 🎨 Style Guide Integration

Der System liest automatisch den Style Guide deines Projekts:
- `projects/{project}/styles/{theme}/variables.css` → Farben, Fonts
- `projects/{project}/styles/{theme}/design-guide.md` → Design Rules
- `projects/{project}/styles/{theme}/style.css` → CSS Komponenten

Die Agents respektieren diese Vorgaben beim Generieren!

## 🧪 Test Mode Features

Mit `TEST_MODE=true` (Standard):
- ✅ Schnelle Mock-Generierung (sofort)
- ✅ Kein API-Schlüssel nötig
- ✅ Perfekt zum Testen der UI
- ✅ Vollständige Agent Chain Simulation
- ❌ Inhalte sind nicht LLM-generiert (Mock Content)

## 📊 API Endpoints (Für Advanced Users)

```bash
# List projects
curl http://localhost:8001/api/projects

# Get project info
curl http://localhost:8001/api/projects/beispiel-projekt

# Generate content
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"project_name":"beispiel-projekt","user_input":"..."}'

# Regenerate slide
curl -X POST http://localhost:8001/api/regenerate \
  -H "Content-Type: application/json" \
  -d '{"project_name":"beispiel-projekt","slide_name":"team","feedback":"..."}'
```

## 🆘 Support & Troubleshooting

### API lädt nicht
1. Stelle sicher, dass Python 3.10+ installiert ist: `python3 --version`
2. Virtual environment aktiviert: `source api/venv/bin/activate`
3. Port 8001 ist frei: `lsof -i :8001` (macOS/Linux)

### Frontend zeigt keine Projekte
- Browser-Console öffnen (F12)
- Auf Fetch-Fehler checken
- Sicherstellen, dass API läuft

### Generierung dauert zu lange
- Mit OpenAI API: Normal 30-60 Sekunden
- Mit TEST_MODE: Sollte <5 Sekunden sein
- Bei Timeout: API-Anfrage überprüfen

## 🎯 Next Steps

1. ✅ Setup abgeschlossen
2. 💬 Öffne `ai-editor.html`
3. 🎨 Wähle ein Projekt
4. ✍️ Schreibe Test-Content
5. 🚀 Generate!
6. 🔄 Experimentiere mit Feedback-Loop

## 📚 Weitere Dokumentation

- [API README](api/README.md) - Technische API Doku
- [component-viewer.html](component-viewer.html) - Klassischer Content-Viewer
- [LLM-PROMPT.md](LLM-PROMPT.md) - Prompt für manuelle LLM-Nutzung
- [QUICK-START.md](QUICK-START.md) - 5-Minuten Übersicht

## 🤝 Contributing

Möchtest du neue Features hinzufügen?

1. Neue Agent? → Füge in `api/agents/` hinzu
2. Neue Service? → Füge in `api/services/` hinzu
3. Frontend Verbesserungen? → Editiere `ai-editor.html`
4. Bugs gefunden? → Schau dir die Error Logs an

Happy content generating! 🎉

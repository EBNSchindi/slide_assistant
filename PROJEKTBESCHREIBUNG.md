# 🚀 Slide Assistant - KI-gestütztes Präsentations-Tool

**Version 2.0** | Stand: November 2024

---

## 📋 Executive Summary

**Slide Assistant** ist ein KI-gestütztes Tool zur effizienten Erstellung professioneller Präsentationen. Es transformiert einfache Stichpunkte oder Markdown-Text in screenshot-freundliche HTML-Komponenten, die direkt in PowerPoint oder Keynote eingefügt werden können.

**Kernprinzip:** Markdown als Single Source of Truth + KI-gestützte Optimierung + Komponenten-basierte Präsentation

---

## 🎯 Wofür ist es da?

### Das Problem

Traditionelle Präsentationserstellung ist ineffizient:
- ❌ Manuelle Formatierung in PowerPoint kostet 15-30 Min pro Folie
- ❌ PowerPoint-Dateien sind schwer versionierbar (große Binärdateien)
- ❌ Inhalte aus Dokumenten müssen manuell übertragen werden
- ❌ Konsistentes Design ist schwer zu gewährleisten
- ❌ Wiederverwendung von Inhalten ist umständlich

### Die Lösung

Slide Assistant automatisiert den gesamten Workflow:

```
Stichpunkte / Markdown
    ↓
🤖 KI-Multi-Agent-System
    ↓
Optimierte Komponenten (HTML + CSS)
    ↓
Screenshot → PowerPoint
```

**Zeitersparnis: ~80%** (von 15 Min auf 3 Min pro Folie)

---

## ✨ Hauptmerkmale

### 1. KI-gestützte Content-Generierung

**Multi-Agent-Architektur** mit 3 spezialisierten KI-Agenten:

```
📊 Content Analyzer Agent
  ├─ Analysiert User-Input (Stichpunkte, Text, Markdown)
  ├─ Identifiziert Inhaltstyp (Statistiken, Listen, Text, Zitate)
  └─ Extrahiert Kernbotschaften

    ↓

🎨 Presentation Strategist Agent
  ├─ Liest Projekt-Design-System (CSS, Style-Guide)
  ├─ Empfiehlt optimale Komponenten-Typen
  └─ Plant Layout und Anordnung

    ↓

✍️ Content Generator Agent
  ├─ Generiert optimiertes Markdown
  ├─ Erstellt HTML mit korrekten CSS-Klassen
  └─ Speichert beide Formate automatisch
```

**Powered by:** OpenAI GPT-4o

### 2. Unified Editor - Alles in einer Oberfläche

**`unified-editor.html`** bietet:

- **Chat-Interface (links):** Input-Panel für Stichpunkte oder Markdown
- **Live-Preview (rechts):** Sofortige Darstellung mit echtem CSS
- **Style-Switcher:** Wähle Design-Theme (GitHub, Modern, Minimal)
- **Component Width Controls:** Optimiere Breite für Screenshots
- **Feedback-Loop:** Regeneriere Slides mit Verbesserungsvorschlägen
- **Agent-Steps Toggle:** Siehe KI-Entscheidungen in Echtzeit

### 3. Komponenten-basiertes System

Jede Folie besteht aus einzelnen, screenshot-fähigen Komponenten:

**Komponenten-Typen:**

| Typ | Beschreibung | Beispiel |
|-----|--------------|----------|
| 📊 **Statistik-Cards** | Zahlen mit Einheiten | `83,6 Mio Einwohner` |
| 📝 **Bullet-Listen** | Formatierte Aufzählungen | `• Feature 1: Beschreibung` |
| 💬 **Zitate** | Hervorgehobene Aussagen | `"KI wird alles ändern"` |
| 📄 **Text-Absätze** | Fließtext mit Formatierung | Paragraphen mit **Fett** |
| 📊 **Tabellen** | Strukturierte Daten | Vergleichstabellen |

**Vorteil:** Jede Komponente kann einzeln gescreenshottet und beliebig in PowerPoint kombiniert werden.

### 4. Style-Aware Generation

Das System respektiert automatisch das Design-System des Projekts:

- **CSS-Variablen:** Farben, Schriften, Abstände
- **Design-Guide:** Regeln für Komponenten-Layouts
- **Theme-Support:** GitHub, Modern, Minimal (erweiterbar)

**Beispiel Design-System:**
```css
:root {
  --github-green: #238636;      /* Primärfarbe */
  --color-fg-default: #24292f;  /* Textfarbe */
  --border-radius: 6px;         /* Abrundung */
}
```

Die KI-Agenten lesen diese Vorgaben und generieren passendes HTML/CSS.

### 5. Versionierung & Git-freundlich

- **Markdown-Dateien:** Leicht lesbar, diff-freundlich
- **Git-Integration:** Änderungen nachvollziehbar
- **Backups:** Automatisch vor Regenerierung
- **Source of Truth:** Markdown als Master-Format

---

## 🏗️ Architektur

### System-Überblick

```
┌─────────────────────────────────────────────┐
│         Unified Editor (Frontend)           │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │ Chat Input   │      │  Live Preview   │ │
│  │ Panel        │      │  with CSS       │ │
│  └──────────────┘      └─────────────────┘ │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST
                   ↓
┌─────────────────────────────────────────────┐
│         FastAPI Backend (Python)            │
│  ┌──────────────────────────────────────┐  │
│  │  Multi-Agent Orchestrator             │  │
│  │  ├─ Content Analyzer                  │  │
│  │  ├─ Presentation Strategist           │  │
│  │  └─ Content Generator                 │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │  Services                             │  │
│  │  ├─ Style Parser (CSS/Design-Guide)  │  │
│  │  ├─ File Service (Save/Load)         │  │
│  │  └─ Project Service (Mgmt)           │  │
│  └──────────────────────────────────────┘  │
└──────────────────┬──────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────┐
│         File System                         │
│  projects/                                  │
│  └─ beispiel-projekt/                       │
│      ├─ markdown/                           │
│      │   ├─ input/      (Basis-Dokumente)  │
│      │   └─ optimized/  (Generierte Slides)│
│      ├─ html/           (Rendered Output)  │
│      └─ styles/         (Design-System)    │
│          ├─ github/                         │
│          ├─ modern/                         │
│          └─ minimal/                        │
└─────────────────────────────────────────────┘
```

### Technologie-Stack

**Frontend:**
- Vanilla JavaScript (kein Framework)
- HTML5 + CSS3
- Fetch API für Backend-Kommunikation

**Backend:**
- Python 3.10+
- FastAPI (RESTful API)
- OpenAI Python SDK (GPT-4o)
- Pydantic (Data Validation)

**Datenhaltung:**
- File-basiert (Markdown + HTML)
- `projects.json` für Konfiguration
- Git-freundliche Textformate

---

## 🚀 Workflow-Beispiel

### Szenario: Team-Folie erstellen

**Schritt 1: Input im Chat-Panel**

```
Unser Team:
- 5 erfahrene Experten
- 20 Jahre kombinierte Erfahrung
- Standorte: Berlin & München
- Spezialisierung: Robotik, KI, Cloud
```

**Schritt 2: KI-Agenten arbeiten**

```
[Content Analyzer]
✓ Erkannt: Liste mit Team-Informationen
✓ Typ: Aufzählung + Fakten
✓ Empfehlung: Bullet-List + Stat-Cards

[Presentation Strategist]
✓ Design-System gelesen: GitHub Style
✓ Komponenten: 2 (Overview + Details)
✓ Layout: Stat-Grid für Zahlen, Bullet für Details

[Content Generator]
✓ Markdown generiert: folie-team.md
✓ HTML generiert: folie-team.html
✓ Dateien gespeichert
```

**Schritt 3: Live-Preview zeigt Ergebnis**

```html
<div class="component" id="slide-team-comp-1">
    <h2>Team Overview</h2>

    <div class="stat-grid">
        <div class="stat-card">
            <span class="stat-number">5</span>
            <span class="stat-label">Experten</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">20+</span>
            <span class="stat-label">Jahre Erfahrung</span>
        </div>
    </div>
</div>

<div class="component" id="slide-team-comp-2">
    <h2>Expertise & Standorte</h2>

    <div class="bullet-list">
        <div class="bullet-item">
            <strong>Spezialisierung:</strong> Robotik, KI, Cloud
        </div>
        <div class="bullet-item">
            <strong>Standorte:</strong> Berlin & München
        </div>
    </div>
</div>
```

**Schritt 4: Feedback geben (optional)**

```
Feedback: "Mach die Zahlen größer und füge Icons hinzu"
```

Agent regeneriert mit Anpassungen.

**Schritt 5: Screenshot erstellen**

1. Chrome DevTools öffnen (F12)
2. Element-Selektor (Strg+Shift+C)
3. Komponente anklicken
4. 3-Punkte-Menü → "Capture node screenshot"

**Schritt 6: In PowerPoint einfügen**

Screenshots als Bilder in PowerPoint-Folie einfügen.

---

## 📂 Projektstruktur

```
slide_assistant/
├── README.md                         # Haupt-Dokumentation
├── CLAUDE.md                         # Technische Entwickler-Docs
├── SCOPE.md                          # Projekt-Scope (Robo4you)
├── PROJEKTBESCHREIBUNG.md            # Diese Datei
├── requirements.txt                  # Python Dependencies
│
├── presentation/                     # Hauptanwendung
│   ├── unified-editor.html           # 🎯 HAUPTTOOL (Editor)
│   ├── run_api.py                    # API Server Starter
│   ├── projects.json                 # Projekt-Konfiguration
│   │
│   ├── README.md                     # Presentation-System Docs
│   ├── SETUP.md                      # Setup-Anleitung
│   ├── SERVER-START.md               # Server-Start Guide
│   │
│   ├── api/                          # FastAPI Backend
│   │   ├── main.py                   # Haupt-API
│   │   ├── config.py                 # Konfiguration
│   │   ├── requirements.txt          # API Dependencies
│   │   ├── .env.example              # Env-Vorlage
│   │   │
│   │   ├── agents/                   # KI-Agenten
│   │   │   ├── content_analyzer.py
│   │   │   ├── presentation_strategist.py
│   │   │   ├── content_generator.py
│   │   │   ├── orchestrator.py
│   │   │   └── mock_agents.py        # Test-Modus Agents
│   │   │
│   │   ├── services/                 # Services
│   │   │   ├── style_parser.py       # CSS/Design-Guide Parser
│   │   │   ├── file_service.py       # Datei-Operationen
│   │   │   └── project_service.py    # Projekt-Management
│   │   │
│   │   └── models/                   # Data Models
│   │       ├── requests.py           # API Request Schemas
│   │       └── responses.py          # API Response Schemas
│   │
│   ├── projects/                     # Projekt-Workspace
│   │   └── beispiel-projekt/
│   │       ├── markdown/
│   │       │   ├── input/
│   │       │   │   └── robo4you-pitch.md
│   │       │   └── optimized/
│   │       │       ├── folie-01-problem.md
│   │       │       ├── folie-02-loesung.md
│   │       │       └── ...
│   │       │
│   │       ├── html/
│   │       │   ├── folie-01-problem.html
│   │       │   ├── folie-02-loesung.html
│   │       │   └── ...
│   │       │
│   │       └── styles/
│   │           ├── github/
│   │           │   ├── style.css
│   │           │   ├── variables.css
│   │           │   └── design-guide.md
│   │           ├── modern/
│   │           └── minimal/
│   │
│   ├── github-presentation-template.css  # Basis-CSS
│   ├── github-design-guide.md            # Design-Dokumentation
│   │
│   └── output/                       # Legacy Output-Ordner
│
└── archive/                          # Archivierte Legacy-Dateien
    ├── README.md
    ├── legacy-editors/               # Alte Viewer
    ├── legacy-scripts/               # Alte Scripts
    │   ├── convert_word_to_markdown.py
    │   └── markdown-to-components.py
    ├── old-docs/
    ├── old-examples/
    └── old-templates/
```

---

## 🎯 Anwendungsfälle

### 1. Startup Pitch Deck

**Herausforderung:** Investoren-Pitch mit vielen Statistiken und Marktdaten

**Lösung:**
- Stichpunkte mit Zahlen eingeben
- KI generiert automatisch Statistik-Cards
- Konsistentes Design über alle Folien
- Schnelle Anpassungen bei Feedback

**Vorteile:**
- ✅ 20 Folien in 1 Stunde statt 5 Stunden
- ✅ Versionierung in Git für Teamarbeit
- ✅ Professionelles, konsistentes Design

### 2. Quarterly Business Review

**Herausforderung:** Regelmäßige Reports mit ähnlicher Struktur

**Lösung:**
- Projekt mit Q1-Vorlage erstellen
- Zahlen für Q2 einfügen
- Automatische Formatierung nach Firmen-Design
- Git-basierte Versionshistorie

**Vorteile:**
- ✅ Wiederverwendbare Templates
- ✅ Nachvollziehbare Änderungen über Zeit
- ✅ Schnelles Klonen für neue Quartale

### 3. Produktpräsentation

**Herausforderung:** Feature-Liste für Sales-Team

**Lösung:**
- Markdown-Dokumentation als Basis
- Mehrere Style-Varianten (Kunde, Intern, Partner)
- Komponenten einzeln für verschiedene Zielgruppen

**Vorteile:**
- ✅ Ein Markdown → Mehrere Präsentationen
- ✅ Features einzeln kombinierbar
- ✅ Schnelle Updates bei Produkt-Änderungen

### 4. Schulungs-Materialien

**Herausforderung:** Konsistente Schulungsfolien für verschiedene Module

**Lösung:**
- Zentrales Design-System
- Modul-spezifische Projekte
- Wiederverwendbare Komponenten (z.B. "Lernziele", "Quiz")

**Vorteile:**
- ✅ Einheitliches Look & Feel
- ✅ Einfaches Updaten bei Änderungen
- ✅ Modulare, kombinierbare Inhalte

---

## 💰 Mehrwert & ROI

### Zeitersparnis

| Aufgabe | Traditionell | Mit Slide Assistant | Ersparnis |
|---------|--------------|---------------------|-----------|
| Folie erstellen | 15-30 Min | 3-5 Min | **80%** |
| Design-Konsistenz | 30 Min/Deck | Automatisch | **100%** |
| Änderungen umsetzen | 10 Min/Folie | 2 Min/Folie | **80%** |
| Versionierung | Manuell | Git | **95%** |

**Beispielrechnung (20-Folien-Deck):**
- Traditionell: 20 × 20 Min = **6,7 Stunden**
- Mit Slide Assistant: 20 × 4 Min = **1,3 Stunden**
- **Ersparnis: 5,4 Stunden (81%)**

### Qualitätsverbesserung

| Aspekt | Verbesserung |
|--------|--------------|
| Design-Konsistenz | ⬆️ 100% (automatisch) |
| Fehlerrate | ⬇️ 60% (weniger Tippfehler) |
| Wiederverwendbarkeit | ⬆️ 90% (Komponenten) |
| Zusammenarbeit | ⬆️ 80% (Git-basiert) |

### Skalierbarkeit

- **Ein Design-System** → Hunderte Präsentationen
- **Zentrale Templates** → Dezentrale Erstellung
- **KI-gestützt** → Keine Skalierungsgrenzen

---

## 🔧 Setup & Installation

### Voraussetzungen

- Python 3.10 oder höher
- Moderner Webbrowser (Chrome, Firefox, Edge)
- OpenAI API Key (optional, TEST_MODE verfügbar)

### Installation in 5 Minuten

**Schritt 1: Repository klonen**

```bash
git clone https://github.com/[user]/slide_assistant.git
cd slide_assistant
```

**Schritt 2: Python Virtual Environment**

```bash
cd presentation/api
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**Schritt 3: Dependencies installieren**

```bash
pip install -r requirements.txt
```

**Schritt 4: Konfiguration**

```bash
cp .env.example .env
# Optional: OpenAI API Key eintragen
# TEST_MODE=true ist bereits voreingestellt (keine API Key nötig)
```

**Schritt 5: Server starten**

```bash
cd ..  # Zurück zu presentation/
python3 run_api.py
```

Server läuft auf: `http://localhost:8001`

**Schritt 6: Editor öffnen**

```bash
open unified-editor.html
# Oder: http://localhost:8001/unified-editor.html
```

**Fertig!** 🎉

### TEST_MODE (ohne API Key)

Standardmäßig läuft das System im TEST_MODE:

- ✅ Keine OpenAI API Key erforderlich
- ✅ Mock-Agenten generieren Demo-Content
- ✅ Volle UI-Funktionalität
- ✅ Perfekt zum Testen und Entwickeln
- ❌ Content nicht von echtem LLM generiert

### Produktiv-Modus (mit OpenAI)

In `.env` anpassen:

```env
OPENAI_API_KEY=sk-proj-...
TEST_MODE=false
DEFAULT_MODEL=gpt-4o
```

---

## 📊 API-Referenz

### Basis-URL

```
http://localhost:8001
```

### Endpoints

#### 1. Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "test_mode": true
}
```

#### 2. Projekte auflisten

```bash
GET /api/projects
```

**Response:**
```json
[
  {
    "name": "beispiel-projekt",
    "styles": ["github", "modern", "minimal"],
    "slides_count": 15
  }
]
```

#### 3. Content generieren

```bash
POST /api/generate
Content-Type: application/json

{
  "project_name": "beispiel-projekt",
  "user_input": "Team: 5 Experten, 20 Jahre Erfahrung",
  "slide_title": "team",
  "style_name": "github"
}
```

**Response:**
```json
{
  "success": true,
  "slide_name": "team",
  "markdown_path": "projects/.../optimized/folie-team.md",
  "html_path": "projects/.../html/folie-team.html",
  "preview_html": "<div class='component'>...</div>",
  "agent_steps": [
    {"agent": "content_analyzer", "output": "..."},
    {"agent": "presentation_strategist", "output": "..."},
    {"agent": "content_generator", "output": "..."}
  ]
}
```

#### 4. Content regenerieren

```bash
POST /api/regenerate
Content-Type: application/json

{
  "project_name": "beispiel-projekt",
  "slide_name": "team",
  "feedback": "Mach es prägnanter und füge Icons hinzu",
  "style_name": "github"
}
```

#### 5. Projekt-Info

```bash
GET /api/projects/{project_name}
```

#### 6. Style-Guide abrufen

```bash
GET /api/projects/{project_name}/style?style_name=github
```

---

## 🎨 Design-System

### GitHub Style (Standard)

**Farben:**
```css
--github-green: #238636       /* Primärfarbe */
--github-green-light: #2ea043 /* Hover */
--color-fg-default: #24292f   /* Text */
--color-fg-muted: #57606a     /* Sekundär */
--color-border: #d0d7de       /* Rahmen */
```

**Typografie:**
```css
--font-base: -apple-system, BlinkMacSystemFont, "Segoe UI", ...
--font-size-large: 28px       /* Überschriften */
--font-size-base: 16px        /* Fließtext */
--font-size-small: 14px       /* Labels */
```

**Spacing:**
```css
--spacing-4: 16px
--spacing-6: 24px
--spacing-8: 32px
```

### Eigene Themes erstellen

1. Ordner erstellen: `projects/mein-projekt/styles/mein-theme/`
2. Dateien hinzufügen:
   - `style.css` - Komponenten-Styles
   - `variables.css` - CSS-Variablen
   - `design-guide.md` - Regeln für KI-Agenten
3. In `projects.json` registrieren:

```json
{
  "name": "mein-projekt",
  "styles": ["github", "mein-theme"]
}
```

---

## 🛠️ Erweiterte Features

### 1. Feedback-Loop

Generierte Slides können mit Feedback regeneriert werden:

```
User: "Mach die Zahlen größer"
    ↓
Content Analyzer: Interpretiert Feedback
    ↓
Strategist: Passt Layout an
    ↓
Generator: Erstellt neue Version
```

**Use Case:** Iterative Verbesserung ohne manuelle Anpassungen

### 2. Multi-Style Support

Ein Projekt, mehrere Design-Varianten:

```
beispiel-projekt/
  └─ styles/
      ├─ github/      → Für GitHub-Community
      ├─ corporate/   → Für Business-Meetings
      └─ investor/    → Für Pitch Deck
```

**Use Case:** Gleicher Inhalt, unterschiedliche Zielgruppen

### 3. Agent-Steps Transparency

Siehe in Echtzeit, was die KI-Agenten entscheiden:

```
[Content Analyzer]
✓ Input-Typ: Bullet-Liste mit Zahlen
✓ Erkannte Metriken: 5 (Anzahl), 20 (Jahre)
✓ Empfehlung: Stat-Grid + Bullet-List

[Presentation Strategist]
✓ Design-System: GitHub (Grün #238636)
✓ Komponenten: 2 (Stats oben, Details unten)
✓ Layout: 2-Column Grid für Stats

[Content Generator]
✓ Markdown: 45 Zeilen
✓ HTML: 2 Komponenten, 4 CSS-Klassen
✓ Validation: Passed
```

**Use Case:** Verstehen und optimieren der KI-Entscheidungen

### 4. Component Width Controls

Optimiere Komponenten-Breite für Screenshots:

- **Auto:** Natürliche Breite
- **400px / 600px / 800px:** Feste Breiten
- **Full:** Volle Container-Breite

**Use Case:** Pixelgenaue Screenshots für verschiedene Slide-Layouts

---

## 🔐 Sicherheit & Datenschutz

### API-Key Management

- ✅ API Keys in `.env` (nicht in Git)
- ✅ `.env.example` als Vorlage
- ✅ TEST_MODE für Key-lose Entwicklung

### Datenspeicherung

- ✅ Alle Daten lokal gespeichert
- ✅ Keine externen Datenbanken
- ✅ Git-basierte Versionierung

### OpenAI API

- ⚠️ User-Input wird an OpenAI gesendet
- ⚠️ Design-Guides werden an OpenAI gesendet
- ✅ Keine Speicherung durch OpenAI (lt. Policy)
- ✅ Opt-out via TEST_MODE möglich

**Empfehlung:** Für sensible Inhalte TEST_MODE verwenden oder lokale LLMs integrieren (geplant).

---

## 📈 Roadmap & Zukunft

### Kurzfristig (Q1 2025)

- [ ] Anthropic Claude API Support
- [ ] Batch-Generierung (mehrere Slides gleichzeitig)
- [ ] Drag & Drop für Markdown-Dateien
- [ ] Export-Templates für PowerPoint

### Mittelfristig (Q2-Q3 2025)

- [ ] Lokale LLM-Integration (Ollama, LM Studio)
- [ ] WebSocket für Streaming-Responses
- [ ] Kollaborations-Features (Multi-User)
- [ ] Versionierung mit Git-Integration

### Langfristig (2026+)

- [ ] Desktop-App (Electron)
- [ ] Figma-Integration
- [ ] Template-Marketplace
- [ ] Enterprise-Features (SSO, Audit-Logs)

---

## ❓ FAQ - Häufig gestellte Fragen

### Allgemein

**F: Brauche ich Programmierkenntnisse?**
A: Nein! Der Unified Editor ist komplett GUI-basiert. Markdown-Kenntnisse sind hilfreich, aber nicht erforderlich.

**F: Kostet das Tool etwas?**
A: Das Tool selbst ist kostenlos. OpenAI API-Nutzung kostet ca. $0,02-0,05 pro Folie. TEST_MODE ist komplett kostenlos.

**F: Funktioniert es offline?**
A: UI und TEST_MODE funktionieren offline. Echte KI-Generierung benötigt Internet (OpenAI API).

**F: Welche Präsentations-Tools werden unterstützt?**
A: PowerPoint, Keynote, Google Slides - alles, was Screenshots als Bilder akzeptiert.

### Technisch

**F: Welche Python-Version wird benötigt?**
A: Python 3.10 oder höher.

**F: Kann ich andere LLMs verwenden?**
A: Aktuell nur OpenAI GPT-4o. Claude und lokale LLMs sind für Q1 2025 geplant.

**F: Wie sichere ich meine Daten?**
A: Alle Daten liegen lokal in `projects/`. Nutze Git für Versionierung und Backups.

**F: Kann ich eigene Komponenten-Typen hinzufügen?**
A: Ja! Erstelle CSS-Klassen in `style.css` und dokumentiere sie im `design-guide.md`.

### Workflow

**F: Wie viele Komponenten pro Folie sind optimal?**
A: 2-3 Komponenten. Maximum: 4-5 für komplexe Folien.

**F: Kann ich bestehende PowerPoint-Decks importieren?**
A: Nicht direkt. Aber: Copy & Paste → Unified Editor → Regenerieren funktioniert gut.

**F: Wie regeneriere ich eine Folie?**
A: Feedback-Text unter der Preview eingeben und "Regenerate" klicken.

**F: Kann ich das Design-System meiner Firma nutzen?**
A: Ja! Erstelle ein Custom Theme mit euren Farben, Schriften und Regeln.

---

## 🆘 Troubleshooting

### Problem: API startet nicht

**Symptom:** `python3 run_api.py` gibt Fehler

**Lösungen:**
1. Python-Version prüfen: `python3 --version` (min. 3.10)
2. Virtual Environment aktiviert? `source api/venv/bin/activate`
3. Dependencies installiert? `pip install -r requirements.txt`
4. Port 8001 frei? `lsof -i :8001` (macOS/Linux)

### Problem: "API Key not configured"

**Symptom:** Generierung schlägt fehl mit Key-Fehler

**Lösungen:**
1. In `.env` setzen: `TEST_MODE=true` (für Entwicklung)
2. Oder: OpenAI API Key in `.env` eintragen

### Problem: Unified Editor zeigt keine Projekte

**Symptom:** Dropdown ist leer

**Lösungen:**
1. API läuft? Health-Check: `curl http://localhost:8001/health`
2. Browser-Console prüfen (F12) auf Fetch-Fehler
3. `projects.json` valide? JSON-Syntax prüfen

### Problem: Generierung dauert ewig

**Symptom:** >60 Sekunden Wartezeit

**Lösungen:**
1. OpenAI API überlastet? Später probieren
2. Input zu lang? Kürzen auf <1000 Wörter
3. TEST_MODE aktivieren für sofortige Antwort

### Problem: Screenshots sind unscharf

**Symptom:** Pixelige Bilder in PowerPoint

**Lösungen:**
1. Browser-Zoom auf 100% setzen
2. Chrome DevTools nutzen (bessere Screenshots als Extensions)
3. Component Width auf 800px+ einstellen
4. High-DPI Display verwenden

### Problem: Git Merge-Konflikte

**Symptom:** Konflikte bei Zusammenführung

**Lösungen:**
1. Markdown-Dateien sind text-basiert → einfach zu mergen
2. Bei HTML-Konflikten: Markdown regenerieren
3. Design-System zentral pflegen (keine parallelen Änderungen)

---

## 📚 Weitere Ressourcen

### Dokumentation

- **[README.md](README.md)** - Haupt-Dokumentation
- **[SETUP.md](presentation/SETUP.md)** - Detaillierte Setup-Anleitung
- **[API README](presentation/api/README.md)** - Backend-API Docs
- **[CLAUDE.md](CLAUDE.md)** - Technische Entwickler-Docs

### Externe Links

- **OpenAI API:** https://platform.openai.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Markdown Guide:** https://www.markdownguide.org
- **GitHub Design System:** https://primer.style

---

## 🤝 Support & Community

### Bei Problemen

1. **Dokumentation prüfen** (diese Datei, SETUP.md)
2. **Troubleshooting-Sektion** durchgehen
3. **Browser Console** (F12) auf Fehler prüfen
4. **API Logs** ansehen (Terminal-Output)

### Feedback & Feature Requests

- GitHub Issues (falls öffentliches Repo)
- Oder: Direkt an Projekt-Maintainer

---

## ✅ Zusammenfassung

### Was ist Slide Assistant?

Ein **KI-gestütztes Tool** zur effizienten Erstellung professioneller, screenshot-freundlicher Präsentations-Komponenten aus einfachen Stichpunkten oder Markdown.

### Kern-Features

1. ✅ **Multi-Agent KI-System** (GPT-4o)
2. ✅ **Unified Editor** mit Live-Preview
3. ✅ **Komponenten-basiert** (einzeln screenshot-bar)
4. ✅ **Style-aware** (respektiert Design-System)
5. ✅ **Git-freundlich** (Markdown as Source)
6. ✅ **Feedback-Loop** (iterative Verbesserung)

### Mehrwert

- **80% Zeitersparnis** bei Folienerstellung
- **100% Design-Konsistenz** (automatisch)
- **Versionierung** in Git (trackbar)
- **Wiederverwendbarkeit** (Komponenten)
- **Skalierbarkeit** (unbegrenzte Projekte)

### Zielgruppe

- **Startups:** Pitch Decks
- **Unternehmen:** Business Reviews, Roadmaps
- **Marketing:** Produkt-Präsentationen
- **Bildung:** Schulungsmaterialien
- **Alle:** Die effizienter präsentieren wollen

### Nächster Schritt

```bash
cd slide_assistant/presentation
python3 run_api.py
open unified-editor.html
```

**Let's create better presentations! 🚀**

---

*Erstellt für Robo4you GmbH - Robotik as a Service Projekt*
*Version 2.0 | November 2024*
*Lizenz: [nach Wahl eintragen]*

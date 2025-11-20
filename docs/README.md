# Slide Assistant Dokumentation

Willkommen zur vollständigen Dokumentation des Slide Assistant - einem KI-gestützten System zur automatischen Generierung von Präsentations-Folien.

---

## 🚀 Schnellstart

Neu hier? Starte mit diesen Guides:

- **[Installation & Setup](../README.md#installation)** - System einrichten (5 Minuten)
- **[Deine erste Folie](guides/first-slide-tutorial.md)** - Erste Folie in 5 Minuten generieren
- **[Theme erstellen](guides/theme-creation/)** - Eigenes Design-Theme erstellen

---

## 📖 Guides & Tutorials

### Theme-Erstellung
- **[Theme Creation - Quick Reference](guides/theme-creation/README.md)** - Checkliste & Kurzanleitung
- **[Theme Creation - Tutorial](guides/theme-creation/tutorial.md)** - Ausführliches Walkthrough
- **[Apple Theme Beispiel](guides/theme-creation/apple-walkthrough.md)** - Apple Design nachbauen
- **[OpenAI Theme Beispiel](guides/theme-creation/openai-walkthrough.md)** - OpenAI Design nachbauen
- **[Tools & Resources](guides/theme-creation/tools.md)** - Farben, Fonts, Design-Tools
- **[Troubleshooting](guides/theme-creation/troubleshooting.md)** - Häufige Fehler & Lösungen

### Entwicklung & Testing
- **[Testing Guide](guides/testing.md)** - Test-Strategien, Mock-Tests, Integration-Tests
- **[Quality Assurance](guides/quality-assurance.md)** - Qualitätsstandards für generierte Folien
- **[First Slide Tutorial](guides/first-slide-tutorial.md)** - Schritt-für-Schritt Anleitung

---

## 🔧 API Dokumentation

### Übersicht
- **[API Overview](api/README.md)** - REST API Grundlagen
- **[Multi-Provider Support](api/multi-provider.md)** - OpenAI, Anthropic Claude, Google Gemini
- **[Endpoints](api/endpoints.md)** - Verfügbare API-Endpunkte
- **[OrchestratorV2](api/orchestrator-v2.md)** - Multi-Provider Orchestrator Details

### Provider-Spezifisch
- **OpenAI** - GPT-4o, GPT-5, GPT-5-mini (Production-ready)
- **Anthropic Claude** - Claude Sonnet 4.5, Claude 3.5 Sonnet (Implemented)
- **Google Gemini** - Gemini 3.0 Pro, 2.5 Pro, 2.0 Flash (Implemented)

---

## 📚 Referenz-Dokumentation

### Architektur
- **[System-Übersicht](reference/architecture.md)** - Wie das System funktioniert
- **[Komponenten-Referenz](reference/components.md)** - Alle 10 Component-Types
- **[V1 → V2 Migration](reference/migration-v1-v2.md)** - Upgrade-Guide (historisch)

### Features & Roadmap
- **[Remaining Features](reference/remaining-features.md)** - Geplante Features
- **[Changelog](reference/changelog.md)** - Versions-Historie

---

## 🎨 Themes & Design

### Verfügbare Themes
- **GitHub Design** (github) - Professional, clean, grüner Akzent
- **Modern** (modern) - Zeitgemäß, balanced
- **Minimal** (minimal) - Reduziert, simpel
- **Apple Design** (apple) - ✨ Clean, minimalistisch, Apple Blue
- **OpenAI Design** (openai) - ✨ Modern, warm, OpenAI Teal

### Theme-System
- **Shared Themes** - Global verfügbar (`shared-themes/`)
- **Project Themes** - Projekt-spezifisch (`projects/{name}/styles/`)
- **Fallback-Chain** - Project → Shared → Default

Siehe: [Theme Creation Guide](guides/theme-creation/)

---

## 🧩 Komponenten

Das System unterstützt **10 Component-Types:**

1. **stat-grid** - Statistiken, Metriken, KPIs
2. **bullet-list** - Listen, Aufzählungen
3. **quote** - Zitate, Testimonials
4. **text** - Fließtext, Paragraphen
5. **table** - Tabellen, Vergleiche
6. **image-frame** - Einzelbilder mit Caption
7. **image-grid** - Mehrere Bilder in Grid
8. **feature-grid** - Features mit Icons & Beschreibung
9. **process** - Prozess-Schritte (vertikal)
10. **process-horizontal** - Prozess-Schritte (horizontal)

Siehe: [Komponenten-Referenz](reference/components.md)

---

## 🔍 Hilfe & Support

### Troubleshooting
- **[Theme-Probleme](guides/theme-creation/troubleshooting.md)** - Theme wird nicht angezeigt, CSS lädt nicht
- **[API-Fehler](api/multi-provider.md#troubleshooting)** - Provider-Fehler, API-Keys
- **[Common Issues](../CLAUDE.md#common-gotchas--troubleshooting)** - Häufige Probleme

### Weitere Ressourcen
- **[CLAUDE.md](../CLAUDE.md)** - Umfassender Guide für Claude Code
- **[GitHub Issues](https://github.com/EBNSchindi/slide_assistant/issues)** - Bug-Reports & Feature-Requests
- **[Pull Requests](https://github.com/EBNSchindi/slide_assistant/pulls)** - Contributions

---

## 📖 Für Entwickler

### Architektur
- **V2 Pipeline** - 3-Agent-System (Analyzer → Strategist → Generator)
- **Deterministic Rendering** - Jinja2 Templates (kein LLM für HTML)
- **Multi-Provider** - Dynamic provider detection & switching
- **Feedback Loop** - Agent 2 kann Blueprints anpassen

### Tech-Stack
- **Backend**: FastAPI, Python 3.10+
- **Agents**: OpenAI API, Anthropic API, Google Generative AI
- **Rendering**: Jinja2 Templates
- **Frontend**: Vanilla JS, HTML/CSS
- **Testing**: pytest, Mock-Agents

---

## 🗺️ Navigation

```
docs/
├── README.md (du bist hier)
├── guides/
│   ├── theme-creation/     → Theme-Erstellung
│   ├── testing.md          → Testing-Strategien
│   └── quality-assurance.md → Qualitäts-Standards
├── api/
│   ├── README.md           → API-Übersicht
│   ├── multi-provider.md   → Multi-Provider Guide
│   └── endpoints.md        → Endpoint-Referenz
└── reference/
    ├── architecture.md     → System-Architektur
    ├── components.md       → Komponenten-Referenz
    └── migration-v1-v2.md  → V1→V2 Migration
```

---

## 📝 Lizenz & Credits

- **Projekt**: Slide Assistant
- **Repository**: [github.com/EBNSchindi/slide_assistant](https://github.com/EBNSchindi/slide_assistant)
- **Lizenz**: MIT (siehe LICENSE)

Entwickelt mit ❤️ und 🤖 Claude Code

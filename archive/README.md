# Archiv - Legacy Dateien

Dieses Archiv enthält veraltete Dateien des Slide Assistant Systems.

## Archiviert am
$(date +"%Y-%m-%d %H:%M:%S")

## Warum wurden diese Dateien archiviert?

### Legacy Editoren
- `ai-editor.html` - Alter Editor, ersetzt durch `unified-editor.html`
- `component-viewer.html` - Standalone Viewer, Funktionalität in unified-editor integriert

### Alte Templates
- `template-*.html` - Vollfolien-Templates, nicht mehr im aktuellen Workflow
- `github-presentation-example.html` - Design-Beispiele (Referenz)

### Alte Dokumentation
- `INDEX.md`, `QUICK-START.md`, `README-KOMPONENTEN.md` - Beschreiben alten Workflow
- `LLM-PROMPT.md` - Manuelle LLM-Konvertierung nicht mehr nötig

### Alte Beispiele
- `output/beispiel-*.html` - Manuell erstellte Beispiele, nicht mehr relevant

### Legacy Scripts
- `convert_word_to_markdown.py` - Word-zu-Markdown Konverter (nicht mehr verwendet)
- `markdown-to-components.py` - Python-Konverter (ersetzt durch AI-Agent-System)

## Aktuelle Hauptanwendung

Die aktuelle Anwendung ist **unified-editor.html** mit dem FastAPI Backend (`/presentation/api/`).

Siehe `/presentation/SETUP.md` für aktuelle Dokumentation.

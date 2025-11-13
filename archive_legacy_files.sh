#!/bin/bash
# Archive Legacy Files Script
# Archiviert veraltete Dateien des Slide Assistant Systems

# Note: Nicht mit set -e, damit Script weiterläuft wenn Dateien fehlen

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "================================================"
echo "  Slide Assistant - Legacy Files Archivierung"
echo "================================================"
echo ""

# Erstelle Archiv-Struktur
echo "📁 Erstelle Archiv-Ordner..."
mkdir -p archive/{legacy-editors,old-templates,old-docs,old-examples,legacy-scripts}

# Zähler für Statistik
MOVED_COUNT=0

# Funktion zum sicheren Verschieben
move_if_exists() {
    local src="$1"
    local dest="$2"

    if [ -f "$src" ]; then
        echo "  → $(basename "$src")"
        mv "$src" "$dest/"
        ((MOVED_COUNT++))
    else
        echo "  ⚠️  Nicht gefunden: $(basename "$src")"
    fi
}

echo ""
echo "🗂️  Legacy Editoren & Viewer archivieren..."
move_if_exists "presentation/ai-editor.html" "archive/legacy-editors"
move_if_exists "presentation/component-viewer.html" "archive/legacy-editors"

echo ""
echo "📄 Alte Templates archivieren..."
move_if_exists "presentation/template-1-classic.html" "archive/old-templates"
move_if_exists "presentation/template-2-modern.html" "archive/old-templates"
move_if_exists "presentation/template-3-minimal.html" "archive/old-templates"
move_if_exists "presentation/template-4-data-driven.html" "archive/old-templates"
move_if_exists "presentation/github-presentation-example.html" "archive/old-templates"

echo ""
echo "📚 Alte Dokumentation archivieren..."
move_if_exists "presentation/INDEX.md" "archive/old-docs"
move_if_exists "presentation/QUICK-START.md" "archive/old-docs"
move_if_exists "presentation/README-KOMPONENTEN.md" "archive/old-docs"
move_if_exists "presentation/LLM-PROMPT.md" "archive/old-docs"
move_if_exists "presentation/beispiel-pitch.md" "archive/old-docs"

echo ""
echo "📸 Alte Beispiele archivieren..."
if [ -d "presentation/output" ]; then
    move_if_exists "presentation/output/beispiel-01-problem.html" "archive/old-examples"
    move_if_exists "presentation/output/beispiel-02-loesung.html" "archive/old-examples"
    move_if_exists "presentation/output/beispiel-03-markt.html" "archive/old-examples"
    move_if_exists "presentation/output/timeline-example.html" "archive/old-examples"

    # Lösche output/ Ordner wenn leer
    if [ -z "$(ls -A presentation/output)" ]; then
        echo "  → Entferne leeren output/ Ordner"
        rmdir presentation/output
    fi
fi

echo ""
echo "🐍 Legacy Scripts archivieren..."
move_if_exists "convert_word_to_markdown.py" "archive/legacy-scripts"
move_if_exists "presentation/markdown-to-components.py" "archive/legacy-scripts"

echo ""
echo "✅ README für Archiv erstellen..."
cat > archive/README.md << 'EOF'
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
EOF

echo ""
echo "================================================"
echo "✅ Archivierung abgeschlossen!"
echo "================================================"
echo ""
echo "📊 Statistik:"
echo "  • $MOVED_COUNT Dateien archiviert"
echo "  • Archiv-Ordner: $SCRIPT_DIR/archive/"
echo ""
echo "💡 Hinweise:"
echo "  • Archiv kann bei Bedarf mit 'rm -rf archive/' gelöscht werden"
echo "  • Oder einzelne Dateien wiederherstellen mit 'mv archive/...'"
echo ""
echo "🚀 Hauptanwendung bleibt unverändert:"
echo "  • presentation/unified-editor.html"
echo "  • presentation/api/"
echo ""

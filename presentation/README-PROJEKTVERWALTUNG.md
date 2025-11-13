# Projektverwaltung - Anleitung

Die Projektverwaltung ermöglicht es Ihnen, Präsentationsprojekte über eine grafische Benutzeroberfläche zu erstellen, umzubenennen und zu löschen.

## Schnellstart

1. **Backend-Server starten:**
   ```bash
   cd presentation
   python3 project_manager_api.py
   ```
   Der Server läuft auf `http://localhost:5000`

2. **Projektverwaltungs-GUI öffnen:**
   - Starten Sie einen lokalen Webserver (für CORS):
     ```bash
     python3 -m http.server 8000
     ```
   - Öffnen Sie im Browser:
     - `http://localhost:8000/project-manager.html` (Projektverwaltung)
     - `http://localhost:8000/component-viewer.html` (Komponenten-Viewer)

3. **Projekte verwalten:**
   - Über die GUI können Sie nun Projekte erstellen, umbenennen und löschen
   - Jedes neue Projekt erhält automatisch die richtige Verzeichnisstruktur

## Funktionen

### Neues Projekt erstellen

1. Klicken Sie auf "➕ Neues Projekt"
2. Geben Sie einen Projektnamen ein (z.B. "Mein Pitch Deck")
3. Klicken Sie auf "Erstellen"

Das System erstellt automatisch:
```
projects/mein-pitch-deck/
├── html/                          # Generierte HTML-Komponenten
├── markdown/
│   ├── input/                     # Ihre Markdown-Quellen
│   │   └── README.md              # Anleitung
│   └── optimized/                 # Pro-Folie optimiertes Markdown
└── styles/
    ├── github/style.css           # GitHub Design (Standard)
    ├── modern/style.css           # Modern Design
    └── minimal/style.css          # Minimal Design
```

### Projekt umbenennen

1. Klicken Sie auf "✏️ Umbenennen" beim gewünschten Projekt
2. Geben Sie den neuen Namen ein
3. Klicken Sie auf "Speichern"

**Hinweis:** Das Verzeichnis und die Konfiguration werden automatisch aktualisiert.

### Projekt löschen

1. Klicken Sie auf "🗑️ Löschen" beim gewünschten Projekt
2. Bestätigen Sie die Löschung im Dialog

**⚠️ Warnung:** Diese Aktion löscht alle Dateien permanent und kann nicht rückgängig gemacht werden!

## Projektstruktur

Jedes Projekt folgt dieser Struktur:

- **html/** - Hier werden die generierten HTML-Komponenten gespeichert
- **markdown/input/** - Legen Sie hier Ihre originalen Markdown-Dateien ab
- **markdown/optimized/** - Pro-Folie optimierte Markdown-Dateien (optional)
- **styles/** - Verschiedene CSS-Themes für Ihre Präsentation

## Workflow

1. **Projekt erstellen** über die GUI
2. **Markdown-Dateien** in `projects/{name}/markdown/input/` ablegen
3. **Konvertieren** zu HTML mit:
   - LLM-Konvertierung (siehe `LLM-PROMPT.md`)
   - Python-Script: `python3 markdown-to-components.py input.md output/`
4. **Vorschau** im Component-Viewer
5. **Screenshots** von einzelnen Komponenten erstellen
6. **Einfügen** in PowerPoint/Keynote

## API-Endpunkte

Das Backend bietet folgende REST-API:

- `GET /api/projects` - Alle Projekte abrufen
- `POST /api/projects` - Neues Projekt erstellen
  ```json
  {"displayName": "Mein Projekt"}
  ```
- `PUT /api/projects/{name}` - Projekt umbenennen
  ```json
  {"displayName": "Neuer Name"}
  ```
- `DELETE /api/projects/{name}` - Projekt löschen

## Namenskonventionen

- **Display Name:** Der Name, wie er in der GUI angezeigt wird (z.B. "Mein Pitch Deck")
- **Project Name:** Der URL-freundliche Name für Verzeichnisse (z.B. "mein-pitch-deck")

Das System konvertiert automatisch:
- Großbuchstaben → Kleinbuchstaben
- Leerzeichen → Bindestriche
- Sonderzeichen → entfernt oder durch Bindestriche ersetzt

## Technische Details

### Backend
- **Framework:** Flask (Python)
- **CORS:** Aktiviert für lokale Entwicklung
- **Port:** 5000 (konfigurierbar)

### Frontend
- **Design:** GitHub Dark Theme
- **Framework:** Vanilla JavaScript
- **API-Kommunikation:** Fetch API

### Datenhaltung
- **Configuration:** `projects.json` (JSON-Datei)
- **Projektdaten:** Dateisystem (`projects/` Verzeichnis)

## Fehlerbehebung

### "API nicht erreichbar"
- Stellen Sie sicher, dass der Backend-Server läuft:
  ```bash
  python3 presentation/project_manager_api.py
  ```

### "CORS-Fehler"
- Nutzen Sie einen lokalen Webserver:
  ```bash
  python3 -m http.server 8000
  ```
- Öffnen Sie die GUI über `http://localhost:8000`

### "Projekt bereits vorhanden"
- Wählen Sie einen anderen Namen
- Oder löschen Sie das existierende Projekt zuerst

## Integration mit Component-Viewer

Der Component-Viewer wurde um einen "⚙️ Projekte" Button erweitert:
- Direkter Zugang zur Projektverwaltung
- Nahtlose Integration in den Workflow
- Gleiche visuelle Gestaltung

## Sicherheitshinweise

- **Nur für lokale Entwicklung:** Der API-Server ist nicht für Produktionsumgebungen gedacht
- **Keine Authentifizierung:** Alle API-Endpunkte sind öffentlich zugänglich
- **Backup:** Erstellen Sie regelmäßig Backups Ihrer Projekte
- **Versionskontrolle:** Nutzen Sie Git für wichtige Projekte

## Weiterführende Links

- [CLAUDE.md](../CLAUDE.md) - Gesamtübersicht des Systems
- [LLM-PROMPT.md](LLM-PROMPT.md) - Anleitung für LLM-basierte Konvertierung
- [README-KOMPONENTEN.md](README-KOMPONENTEN.md) - Komponenten-System Dokumentation

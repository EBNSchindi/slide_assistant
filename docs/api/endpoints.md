# API Endpoints Referenz

Dokumentation aller verfügbaren REST-API Endpoints für Slide-Generierung.

---

## Überblick

Die Slide Assistant API basiert auf **FastAPI** und läuft auf `http://localhost:8001`.

### Endpoints

| Endpoint | Methode | Version | Status |
|----------|---------|---------|--------|
| `/health` | GET | - | Verfügbar |
| `/api/v2/generate` | POST | 2.0 | Production |

---

## Health Check

**Endpoint:** `GET /health`

Überprüfe, ob der Server läuft.

### Request
```bash
curl http://localhost:8001/health
```

### Response (200 OK)
```json
{
  "status": "ok"
}
```

---

## Slide Generierung (V2)

**Endpoint:** `POST /api/v2/generate`

Generiert eine Präsentationsfolie basierend auf Benutzer-Input mit 3-Agent-Pipeline.

### Basis-Request

```bash
curl -X POST http://localhost:8001/api/v2/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "beispiel-projekt",
    "user_input": "Unsere Ergebnisse 2024: €42,5 Mio Umsatz (+18%), 8.500 Kunden, 145 Mitarbeiter",
    "slide_number": 46,
    "slide_title": "Geschäftsergebnisse",
    "theme": "github"
  }'
```

### Request-Schema

```json
{
  "project_name": "string (required)",
  "user_input": "string (required)",
  "slide_number": "integer (required)",
  "slide_title": "string (optional, default: 'Folie {number}')",
  "theme": "string (optional, default: 'github')",
  "language": "string (optional, default: 'de', values: 'de'|'en')",
  "model": "string (optional, default: 'gpt-4o')",
  "images": "array (optional, default: [])"
}
```

### Request-Parameter Details

#### project_name (erforderlich)
Der Name des Ziel-Projekts. Die generierten Dateien werden hier gespeichert.

```json
"project_name": "beispiel-projekt"
```

Speicherlokation:
- Markdown: `projects/beispiel-projekt/markdown/optimized/folie-{NN}-{title}.md`
- HTML: `projects/beispiel-projekt/html/folie-{NN}-{title}.html`

#### user_input (erforderlich)
Der Inhalt, der auf die Folie kommt. Kann verschiedenste Formate sein.

**Statistiken:**
```
Unser Wachstum:
- Umsatz: €12,3 Mio
- Kunden: 8.500
- Gewinn: €2,1 Mio
```

**Listen:**
```
Unsere Features:
- Cloud-Native Architektur
- Machine Learning Integration
- 99.99% Verfügbarkeit
- Enterprise Security
```

**Zitate:**
```
"Innovation unterscheidet zwischen Führerschaft und Nachfolgern"
- Steve Jobs
```

**Gemischter Inhalt:**
```
Der Markt wächst rapidely. Hauptgründe:

1. Digitale Transformation (2022-2024)
2. AI-Adoption (2024-2025)
3. Cloud Migration (2025-)

Unsere Position: #3 im Segment, schnellster Wachstum
```

#### slide_number (erforderlich)
Die Foliennummer. Wird für Datei-Naming verwendet.

```json
"slide_number": 46
```

Erzeugt: `folie-46-{title}.md` und `folie-46-{title}.html`

#### slide_title (optional)
Der Titel der Folie. Wird oben angezeigt und im Dateiname verwendet.

```json
"slide_title": "Geschäftsergebnisse 2024"
```

Default: `"Folie {slide_number}"` (z.B. "Folie 46")

#### theme (optional)
Das Design-Theme. Bestimmt Farben, Schriftarten, Styling.

```json
"theme": "github"
```

**Verfügbare Themes:**
- `github` (Standard) - Professional, grüner Akzent, GitHub Design
- `modern` - Zeitgenössisch, balanced
- `minimal` - Reduziert, minimalistisch
- `apple` - Minimalistisch, Apple Blue
- `openai` - Modern, warm, OpenAI Teal

Default: `"github"`

#### language (optional)
Die Zielsprache für die Generierung.

```json
"language": "de"
```

**Unterstützte Sprachen:**
- `de` (Deutsch) - Standard
- `en` (Englisch)

Default: `"de"`

Das System auto-detektiert auch die Sprache des `user_input` und verwendet diese, wenn nicht anders spezifiziert.

#### model (optional)
Das LLM-Modell für die Generierung. Bestimmt Provider und Qualität.

```json
"model": "gpt-4o"
```

**OpenAI Modelle:**
- `gpt-4o` - GPT-4 Turbo (schnell, zuverlässig, empfohlen)
- `gpt-5` - GPT-5 (beste Qualität, langsamere)
- `gpt-5-mini` - GPT-5 Mini (schneller, kosten-optimiert)

**Anthropic Modelle:**
- `claude-sonnet-4.5` - Claude Sonnet 4.5 (analytisch)
- `claude-sonnet-4.5-20250514` - Latest Claude version
- `claude-3-5-sonnet` - Claude 3.5 Sonnet (älter)

**Google Modelle:**
- `gemini-3.0-pro` - Gemini 3.0 Pro (latest)
- `gemini-2.5-pro` - Gemini 2.5 Pro
- `gemini-2.0-flash` - Gemini 2.0 Flash (schneller)

Default: `"gpt-4o"` (aber auto-detektiert basierend auf verfügbaren API-Keys)

**Provider Auto-Detection:**
Das System wählt den Provider automatisch basierend auf dem Model:
- OpenAI: `gpt-*` → Provider: openai
- Anthropic: `claude-*` → Provider: anthropic
- Google: `gemini-*` → Provider: google

#### images (optional)
Referenzen zu Bildern, die auf der Folie verwendet werden sollen.

```json
"images": [
  {
    "filename": "chart-sales.png",
    "description": "Sales chart für 2024"
  },
  {
    "filename": "team-photo.jpg",
    "description": "Team-Foto beim Kickoff"
  }
]
```

Bilder müssen in `projects/{project_name}/images/uploads/` vorhanden sein.

Default: `[]` (keine Bilder)

---

### Response-Schema

Erfolgreiche Antwort (HTTP 200):

```json
{
  "success": true,
  "provider": "string",
  "model": "string",
  "html_content": "string (HTML)",
  "markdown_content": "string (Markdown)",
  "feedback_iterations": integer,
  "saved_files": {
    "markdown_path": "string",
    "html_path": "string"
  },
  "metadata": {
    "slide_number": integer,
    "slide_title": string,
    "theme": string,
    "language": string,
    "generation_time_ms": integer,
    "content_type": string,
    "component_count": integer
  }
}
```

### Response-Parameter Details

#### success
Boolean-Flag ob Generierung erfolgreich war.

```json
"success": true
```

#### provider
Der verwendete LLM-Provider.

```json
"provider": "openai"
```

Mögliche Werte: `openai`, `anthropic`, `google`

#### model
Das tatsächlich verwendete Modell.

```json
"model": "gpt-4o"
```

#### html_content
Der vollständige HTML-Code der generierten Folie.

```json
"html_content": "<!DOCTYPE html>...<h2>Geschäftsergebnisse</h2>..."
```

Kann direkt in HTML-Dateien gespeichert oder angezeigt werden.

#### markdown_content
Die Folie als Markdown. Nützlich für:
- Bearbeitung
- Versionskontrolle
- Batch-Processing

```json
"markdown_content": "# Geschäftsergebnisse 2024\n## Statistiken\n..."
```

#### feedback_iterations
Wie viele Feedback-Schleifen die Agenten durchlaufen haben (0 = erste Iteration erfolgreich).

```json
"feedback_iterations": 0
```

Dies passiert, wenn Agent 3 (ContentGenerator) die Validierung nicht bestand und Agent 2 (Strategist) den Plan überarbeitet hat.

#### saved_files
Pfade zu den gespeicherten Dateien.

```json
"saved_files": {
  "markdown_path": "/home/dani/Schreibtisch/cursor_dev/slide_assistant/projects/beispiel-projekt/markdown/optimized/folie-46-geschaeftsergebnisse.md",
  "html_path": "/home/dani/Schreibtisch/cursor_dev/slide_assistant/projects/beispiel-projekt/html/folie-46-geschaeftsergebnisse.html"
}
```

#### metadata
Zusätzliche Metadaten über die generierte Folie.

```json
"metadata": {
  "slide_number": 46,
  "slide_title": "Geschäftsergebnisse",
  "theme": "github",
  "language": "de",
  "generation_time_ms": 4230,
  "content_type": "statistics",
  "component_count": 1
}
```

---

## Fehlerbehandlung

### HTTP 400 - Bad Request

Fehlende oder ungültige Parameter.

```json
{
  "detail": "Missing required fields: project_name, user_input"
}
```

**Häufige Gründe:**
- `project_name` fehlt
- `user_input` ist leer
- `slide_number` ist keine Zahl

### HTTP 404 - Not Found

Projekt oder Theme existiert nicht.

```json
{
  "detail": "Project 'nonexistent-project' not found"
}
```

**Lösung:** Stelle sicher dass das Projekt in `projects/` existiert.

### HTTP 500 - Internal Server Error

Fehler bei der Generierung.

```json
{
  "detail": "Generation failed: OpenAI API error - 401 Unauthorized"
}
```

**Häufige Gründe:**
- API-Key ungültig oder abgelaufen
- Model nicht verfügbar
- Provider-spezifischer Fehler

**Debugging:**
1. Prüfe Server-Logs: `python3 run_api.py`
2. Prüfe `.env` Datei: `cat presentation/api/.env`
3. Teste API-Key: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`

---

## Beispiel: Vollständiger Workflow

### 1. Basis-Request (einfach)

```bash
curl -X POST http://localhost:8001/api/v2/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "beispiel-projekt",
    "user_input": "Umsatz 2024: €42,5 Mio. Wachstum: +18%. Kunden: 8.500",
    "slide_number": 1
  }'
```

Response: Einfache Statistik-Folie mit Default-Title "Folie 1", Default-Theme "github"

### 2. Detaillierter Request (alle Parameter)

```bash
curl -X POST http://localhost:8001/api/v2/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "beispiel-projekt",
    "slide_number": 46,
    "slide_title": "Geschäftsergebnisse 2024",
    "user_input": "Unser erfolgreichstes Jahr:\n\n- Umsatz: €42,5 Mio (+18% YoY)\n- Gewinn: €8,7 Mio\n- Kunden: 8.500 weltweit\n- Mitarbeiter: 145\n- Marktanteile: 12 Länder",
    "theme": "apple",
    "language": "de",
    "model": "gpt-4o",
    "images": [
      {
        "filename": "revenue-chart.png",
        "description": "Umsatz-Entwicklung 2020-2024"
      }
    ]
  }'
```

### 3. Request mit Python

```python
import requests
import json

url = "http://localhost:8001/api/v2/generate"

payload = {
    "project_name": "beispiel-projekt",
    "user_input": "Wir haben 1000 Kunden gewonnen im Q4",
    "slide_number": 10,
    "slide_title": "Q4 Ergebnisse",
    "theme": "modern"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    result = response.json()
    print("Success:", result['success'])
    print("HTML-Datei:", result['saved_files']['html_path'])
    print("Markdown-Datei:", result['saved_files']['markdown_path'])
else:
    print("Error:", response.status_code)
    print(response.json())
```

### 4. Request mit JavaScript (Frontend)

```javascript
async function generateSlide() {
  const formData = {
    project_name: "beispiel-projekt",
    slide_number: 46,
    slide_title: "Geschäftsergebnisse",
    user_input: document.getElementById("content").value,
    theme: document.getElementById("theme").value,
    language: "de",
    model: "gpt-4o"
  };

  try {
    const response = await fetch("http://localhost:8001/api/v2/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData)
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const result = await response.json();

    if (result.success) {
      // Zeige HTML-Preview
      document.getElementById("preview").innerHTML = result.html_content;
      // Oder speichere Dateien
      console.log("Gespeichert unter:", result.saved_files);
    } else {
      alert("Generierung fehlgeschlagen");
    }
  } catch (error) {
    console.error("Fehler:", error);
    alert("API-Fehler: " + error.message);
  }
}
```

---

## Rate Limiting & Performance

### Limits
- **Max. Anfragen pro Minute:** 60 (global)
- **Max. Folien pro Request:** 1 (derzeit, Batch-Modus geplant)
- **Timeout:** 60 Sekunden pro Request

### Performance-Tipps

1. **Schnell:** Nutze `gpt-4o` statt `gpt-5`
   - gpt-4o: ~3-5 Sekunden
   - gpt-5: ~8-12 Sekunden

2. **Batch-Generierung (kommend)**
   - Derzeit: Eine Folie pro Request
   - Geplant: Mehrere Folien in einem Batch

3. **Caching (kommend)**
   - Ähnliche Inhalte könnten gecacht werden
   - Würde Generierungszeit sparen

---

## Authentifizierung (kommend)

Derzeit keine Authentifizierung erforderlich (localhost).

Für Production ist geplant:
- API-Key basierte Authentifizierung
- Bearer Token in `Authorization` Header
- Rate-Limiting pro API-Key

---

## Verwandte Dokumentation

- **[System-Architektur](../reference/architecture.md)** - Wie die 3-Agent-Pipeline funktioniert
- **[Komponenten-Referenz](../reference/components.md)** - Verfügbare Komponenten-Types
- **[Erste Folie Tutorial](../guides/first-slide-tutorial.md)** - Schritt-für-Schritt Anleitung
- **[Multi-Provider Support](multi-provider.md)** - Details zu verschiedenen Providern

---

**API Version:** 2.0
**Zuletzt aktualisiert:** 2025-11-20
**Status:** Production-Ready

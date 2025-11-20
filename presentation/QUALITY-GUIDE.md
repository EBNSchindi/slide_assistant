# Quality Guide - Konsistente Folienqualität sicherstellen

## Übersicht

Dieses Dokument erklärt, wie sichergestellt wird, dass alle generierten Folien die gleiche hohe Qualität wie die Beispielfolien (Folien 1-8) haben.

**V2-Architektur:** Folien werden durch deterministische Jinja2-Templates generiert, nicht durch LLM-HTML. Dies garantiert konsistente, hochwertige Ausgabe.

## Referenz: Hochwertige Beispielfolien

Die Folien 1-8 im `beispiel-projekt` dienen als Qualitätsstandard:

- **Folie 08 (folie-08-bilder.html)** - Best Practice für Bild-Komponenten
- Strukturierte Layouts mit klaren CSS-Klassen
- Semantisches HTML mit Accessibility-Attributen
- Konsistente Komponenten-Struktur

## V2 Architecture: Template-Based Generation

### Rendering-Pipeline

```
Agent 3 (ContentGeneratorV2)
  ↓ Outputs: FormattedSlide (pure data)
HTMLComponentRenderer (Jinja2)
  ↓ Uses: Templates from presentation/templates/components/
Deterministic HTML Output
```

**Wichtig:** HTML wird NICHT vom LLM generiert, sondern von Jinja2-Templates!

### Template-Verzeichnis

Alle Component-Templates befinden sich in:
`presentation/templates/components/*.html.j2`

**Verfügbare Templates:**
- `stat-grid.html.j2` - Statistik-Karten
- `bullet-list.html.j2` - Aufzählungslisten
- `quote.html.j2` - Zitate
- `text.html.j2` - Formatierter Text
- `table.html.j2` - Tabellen
- `image-frame.html.j2` - Einzelbilder
- `image-grid.html.j2` - Bild-Galerien
- `feature-grid.html.j2` - Feature-Karten
- `process.html.j2` - Vertikale Prozesse
- `process-horizontal.html.j2` - Horizontale Prozesse

## Bild-Komponenten: Template-Struktur

### ✅ RICHTIG (Jinja2 Template)

**Template:** `presentation/templates/components/image-frame.html.j2`

**Verwendung durch Agent 3:**
```python
FormattedSlide(
    components=[
        ComponentData(
            type="image-frame",
            data={
                "image_path": "projects/beispiel-projekt/images/uploads/screenshot.png",
                "alt_text": "Analytics dashboard showing real-time metrics",
                "title": "Dashboard Overview",
                "description": "Real-time analytics with graph visualizations and KPI tracking."
            }
        )
    ]
)
```

**Gerenderte Ausgabe:**
```html
<div class="component" id="slide-X-comp-Y" role="region" aria-label="Visual demonstration">
  <div class="component-label">Component Y</div>
  <h2>Dashboard Overview</h2>
  <div class="image-container">
    <div class="image-wrapper">
      <img src="projects/beispiel-projekt/images/uploads/screenshot.png"
           alt="Analytics dashboard showing real-time metrics"
           style="max-width: 100%; height: auto; border-radius: 8px;">
    </div>
    <div class="image-content">
      <h4>Dashboard Overview</h4>
      <p>Real-time analytics with graph visualizations and KPI tracking.</p>
    </div>
  </div>
</div>
```

### ❌ FALSCH (Veralteter V1-Ansatz)

```python
# V1: LLM generiert HTML direkt (NICHT MEHR VERWENDET)
html_string = agent.generate_html(...)  # ❌ Deprecated
```

**Warum falsch:**
- LLM-generiertes HTML ist inkonsistent
- Keine Garantie für korrekte Struktur
- Schwer zu warten und zu testen
- V1-Architektur wurde komplett ersetzt

## V2 Content Generator Agent

Der Generierungsprozess läuft über **3 Agenten + Renderer**:

### Agent 1: ContentAnalyzerAgentV2
`presentation/api/agents/content_analyzer_v2.py`
- Analysiert User-Input
- Erkennt Content-Typen (Bilder, Statistiken, Listen, etc.)
- Detektiert Sprache (Deutsch/English)

### Agent 2: PresentationStrategistAgentV2
`presentation/api/agents/presentation_strategist_v2.py`
- Plant Layout und Komponenten
- Referenziert design-guide.json
- Wählt passende Template-Typen

### Agent 3: ContentGeneratorAgentV2
`presentation/api/agents/content_generator_v2.py`
- Generiert **pure data** (KEIN HTML!)
- Validiert gegen Pydantic schemas
- Ausgabe: FormattedSlide mit ComponentData

### Renderer: HTMLComponentRenderer
`presentation/api/renderers/component_renderer.py`
- Lädt Jinja2-Templates
- Rendert FormattedSlide → HTML
- Wendet Theme-Tokens an
- **Deterministische Ausgabe** (immer gleich für gleiche Daten)

## Qualitätskriterien für neue Folien

### ✅ Template-Qualität

Alle Templates müssen:
- [ ] Semantisches HTML verwenden
- [ ] Accessibility-Attribute haben (`role`, `aria-label`)
- [ ] Theme-Tokens respektieren (aus design-guide.json)
- [ ] Responsive sein
- [ ] Konsistente CSS-Klassen verwenden

### ✅ Agent-3-Output

FormattedSlide muss enthalten:
- [ ] Korrekte component `type` (matcht Template-Namen)
- [ ] Vollständige `data` (alle Template-Variablen gefüllt)
- [ ] Beschreibende Alt-Texte (nicht "image" oder "screenshot")
- [ ] Korrekte Bildpfade (`projects/{project}/images/uploads/{file}`)
- [ ] Sprach-konsistente Texte

### ✅ Renderer-Output

Generiertes HTML muss haben:
- [ ] Korrekte Component-IDs (`slide-X-comp-Y`)
- [ ] Alle Theme-Tokens angewendet
- [ ] Valides HTML (keine fehlenden Tags)
- [ ] Konsistentes Styling

## Template-Entwicklung

### Neues Template erstellen

1. **Template-Datei erstellen:**
   ```bash
   touch presentation/templates/components/my-component.html.j2
   ```

2. **Jinja2-Template schreiben:**
   ```jinja2
   <div class="my-component">
     <h3>{{ title }}</h3>
     <p>{{ description }}</p>
   </div>
   ```

3. **Schema in agents/schemas.py definieren:**
   ```python
   class MyComponentData(BaseModel):
       title: str
       description: str
   ```

4. **Renderer updaten:**
   ```python
   # In component_renderer.py
   self.component_type_map["my-component"] = "my-component"
   ```

5. **design-guide.json erweitern:**
   ```json
   {
     "components": {
       "my-component": {
         "description": "Custom component",
         "slots": ["title", "description"]
       }
     }
   }
   ```

## Häufige Fehler vermeiden

### 1. LLM für HTML verwenden (V1)
❌ Agent generiert HTML direkt
✅ Agent generiert FormattedSlide, Renderer erzeugt HTML

### 2. Templates ohne Tokens
❌ Hard-coded Farben im Template
✅ CSS-Variablen aus design-guide.json verwenden

### 3. Fehlende Validierung
❌ Agent 3 gibt ungültige Daten zurück
✅ Pydantic schemas validieren alle Daten

### 4. Inkonsistente Component-IDs
❌ Manuell vergebene IDs
✅ Renderer generiert IDs automatisch

## Workflow: Neue Folien generieren

### 1. Via Unified Editor
```bash
cd presentation
python3 run_api.py
# Öffne: unified-editor.html
# Eingabe → Generate → Live Preview
```

### 2. Via API
```bash
curl -X POST http://localhost:8001/api/v2/generate \
  -H "Content-Type: application/json" \
  -d '{"project_name": "beispiel-projekt", "user_input": "..."}'
```

### 3. Qualitätskontrolle
- Visueller Vergleich mit Referenzfolien
- Template-Ausgabe validieren
- Theme-Konsistenz prüfen

## Testing

### Template Tests

```bash
cd presentation/api
export TEST_MODE=true
python3 -m pytest tests/test_template_system.py -v
```

### Renderer Tests

```bash
python3 -m pytest tests/test_renderer_fix.py -v

# Spezifisches Template testen
python3 -m pytest tests/test_renderer_fix.py::test_image_frame -v
```

### Integration Tests

```bash
python3 -m pytest tests/test_v2_integration.py -v
```

## Wartung

### Bei Template-Updates:
1. Ändere Template in `presentation/templates/components/`
2. Teste mit Renderer: `pytest tests/test_renderer_fix.py -v`
3. Regeneriere Beispielfolien zur Verifizierung

### Bei Agent-Updates:
1. Ändere Agent in `agents/*_v2.py`
2. Teste mit Mocks: `pytest tests/test_agents_v2.py -v`
3. Teste Integration: `pytest tests/test_v2_integration.py -v`

### Bei Schema-Änderungen:
1. Update `agents/schemas.py`
2. Update entsprechendes Template
3. Update Tests
4. Regression-Tests ausführen

## Referenzen

- **Beispielfolien:** `presentation/projects/beispiel-projekt/html/`
- **Templates:** `presentation/templates/components/*.html.j2`
- **Agent V2:** `presentation/api/agents/*_v2.py`
- **Renderer:** `presentation/api/renderers/component_renderer.py`
- **Schemas:** `presentation/api/agents/schemas.py`
- **Main Docs:** `CLAUDE.md`
- **API Docs:** `presentation/api/README.md`
- **Template Tests:** `presentation/api/tests/test_template_system.py`

## Zusammenfassung

**V1 (Deprecated):**
- LLM generiert HTML direkt
- Inkonsistente Ausgabe
- Schwer zu warten

**V2 (Current):**
- Agent generiert **pure data**
- Jinja2-Templates rendern HTML
- **Deterministische Ausgabe**
- Einfach zu testen und zu warten

**Kernprinzip:** Alle neuen Folien verwenden die gleichen Jinja2-Templates. Qualität wird durch Template-Design sichergestellt, nicht durch LLM-Prompting.

**Hauptmechanismus:**
1. Agent 3 → FormattedSlide (data only)
2. Renderer → Jinja2 Template + data = HTML
3. Konsistente, hochwertige Ausgabe garantiert

**Qualitätssicherung:**
- Template-basierte Konsistenz
- Pydantic-Validierung
- Automatische Tests
- Theme-Token-System

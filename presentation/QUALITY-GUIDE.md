# Quality Guide - Konsistente Folienqualität sicherstellen

## Übersicht

Dieses Dokument erklärt, wie sichergestellt wird, dass alle generierten Folien die gleiche hohe Qualität wie die Beispielfolien (Folien 1-8) haben.

## Referenz: Hochwertige Beispielfolien

Die Folien 1-8 im `beispiel-projekt` dienen als Qualitätsstandard:

- **Folie 08 (folie-08-bilder.html)** - Best Practice für Bild-Komponenten
- Strukturierte Layouts mit klaren CSS-Klassen
- Semantisches HTML mit Accessibility-Attributen
- Konsistente Komponenten-Struktur

## Bild-Komponenten: Richtige Struktur

### ✅ RICHTIG (Folie 08 Stil)

**Einzelnes Bild:**
```html
<div class="component" id="slide-X-comp-Y" role="region" aria-label="Visual demonstration">
  <div class="component-label">Component Y</div>
  <h2>Component Title</h2>
  <div class="image-container">
    <div class="image-wrapper">
      <img src="projects/PROJECT/images/uploads/FILE.png"
           alt="Descriptive alt text"
           style="max-width: 100%; height: auto; border-radius: 8px;">
    </div>
    <div class="image-content">
      <h4>Image Title</h4>
      <p>Brief description with context and significance.</p>
    </div>
  </div>
</div>
```

**Mehrere Bilder (Grid):**
```html
<div class="image-grid">
  <div class="image-card">
    <div class="image-wrapper">
      <img src="..." alt="..." style="...">
      <span class="image-badge">
        <span class="badge badge-success">Status</span>
      </span>
    </div>
    <div class="image-content">
      <h4>Title</h4>
      <p>Description</p>
    </div>
  </div>
  <!-- Weitere image-card Elemente -->
</div>
```

### ❌ FALSCH (Niedrige Qualität)

```html
<!-- NICHT verwenden: Einfache figure/figcaption Struktur -->
<figure class="image-container">
  <img src="..." alt="...">
  <figcaption>Caption</figcaption>
</figure>
```

**Warum falsch:**
- Keine strukturierte Layout-Hierarchie
- Kein separater `.image-wrapper` für Flexibilität
- Keine `.image-content` für reichhaltige Beschreibungen
- Nur einfache Caption statt Titel + Beschreibung
- Weniger CSS-Styling-Möglichkeiten

## Content Generator Agent

Der Generierungsprozess läuft über den **Content Generator Agent** in:
`presentation/api/agents/content_generator.py`

### Wichtige Abschnitte im Agent:

1. **IMAGE Component Guidelines (Zeile 139-148)**
   - Definiert Regeln für Bild-Komponenten
   - Strukturiertes Layout mit `.image-wrapper` und `.image-content`

2. **HTML Component Templates (Zeile 197-248)**
   - Template für Einzelbilder
   - Template für Bild-Grids
   - Korrekte CSS-Klassen und Struktur

3. **Examples (Zeile 360-435)**
   - Before/After Beispiele
   - Zeigen richtige vs. falsche Umsetzung

4. **Critical Reminders (Zeile 486-506)**
   - Explizite Anweisungen gegen `<figure>/<figcaption>`
   - Anforderung für strukturiertes Layout

## Qualitätskriterien für neue Folien

Wenn eine neue Folie generiert wird, überprüfe:

### ✅ Struktur
- [ ] Verwendet `.image-container` > `.image-wrapper` + `.image-content`
- [ ] Hat `<h4>` Titel in `.image-content`
- [ ] Hat `<p>` Beschreibung in `.image-content`
- [ ] Korrekte Component-IDs (`slide-X-comp-Y`)
- [ ] Accessibility-Attribute (`role`, `aria-label`)

### ✅ Styling
- [ ] `border-radius: 8px` auf `<img>`
- [ ] `max-width: 100%; height: auto` auf `<img>`
- [ ] Konsistentes Spacing
- [ ] Korrekte CSS-Klassen

### ✅ Content
- [ ] Beschreibender Alt-Text (nicht "image" oder "screenshot")
- [ ] Informativer Titel in `<h4>`
- [ ] Kontextuelle Beschreibung in `<p>`
- [ ] Korrekte Bildpfade (`projects/{project}/images/uploads/{file}`)

### ✅ Accessibility
- [ ] Alle Komponenten haben `role` Attribut
- [ ] Beschreibende `aria-label`
- [ ] Alt-Text bei Bildern
- [ ] Semantisches HTML

## Häufige Fehler vermeiden

### 1. Relative Pfade
❌ `src="../images/file.png"`
✅ `src="projects/beispiel-projekt/images/uploads/file.png"`

### 2. Generischer Alt-Text
❌ `alt="Image"` oder `alt="Screenshot"`
✅ `alt="Analytics dashboard showing real-time metrics with graph visualizations"`

### 3. Fehlende Struktur
❌ Direktes `<img>` ohne Wrapper
✅ `.image-container` > `.image-wrapper` + `.image-content`

### 4. Fehlende Beschreibung
❌ Nur `<figcaption>` mit kurzem Text
✅ `<h4>` Titel + `<p>` ausführliche Beschreibung

## Workflow: Neue Folien generieren

1. **Vor der Generierung:**
   - Stelle sicher, dass Content Generator Agent aktuell ist
   - Prüfe, dass Templates korrekt sind

2. **Während der Generierung:**
   - Agent verwendet automatisch die richtigen Templates
   - Basiert auf System-Prompt in `content_generator.py`

3. **Nach der Generierung:**
   - Vergleiche mit Folie 08
   - Prüfe Checkliste oben
   - Bei Abweichungen: Manuell korrigieren

4. **Feedback-Loop:**
   - Wenn Fehler häufig auftreten: Agent-Prompt verbessern
   - Beispiele im Agent aktualisieren

## Testing neuer Folien

Teste generierte Folien im Component Viewer:

```bash
cd presentation
python3 -m http.server 8000
# Öffne: http://localhost:8000/component-viewer.html
```

Vergleiche visuell mit Folie 08:
- Gleiche Layout-Struktur?
- Gleiche Abstände und Styling?
- Gleiche Informationsdichte?

## Wartung

### Bei Agent-Updates:
1. Prüfe, dass Image Component Templates erhalten bleiben
2. Teste mit Beispiel-Generierung
3. Vergleiche Ausgabe mit Folie 08

### Bei CSS-Updates:
1. Teste auf allen Beispielfolien
2. Stelle sicher, dass `.image-container`, `.image-wrapper`, `.image-content` funktionieren
3. Prüfe Responsiveness

## Referenzen

- **Beispielfolie:** `presentation/projects/beispiel-projekt/html/folie-08-bilder.html`
- **Agent-Code:** `presentation/api/agents/content_generator.py`
- **Projekt-Struktur:** `presentation/projects.json`
- **Main Docs:** `CLAUDE.md`

## Zusammenfassung

**Kernprinzip:** Alle neuen Folien sollten die gleiche Struktur und Qualität wie Folie 08 haben.

**Hauptmechanismus:** Content Generator Agent mit korrekten Templates im System-Prompt.

**Qualitätssicherung:** Visuelle Vergleiche + Checkliste + Testing im Viewer.

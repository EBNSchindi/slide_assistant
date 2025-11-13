# LLM Prompt für Markdown → HTML Konvertierung

Verwenden Sie diesen Prompt, um Ihr Pitch-Deck-Markdown in HTML-Komponenten zu konvertieren.

---

## Prompt für LLM (z.B. Claude, GPT-4)

```
Ich habe ein Pitch-Deck als Markdown geschrieben und möchte es in HTML-Komponenten konvertieren.

WICHTIG: 
- Jeder H1-Abschnitt (# Folie X) wird zu EINER HTML-Datei
- Jeder H2-Abschnitt (## Komponenten-Titel) wird zu EINER Komponente innerhalb dieser Datei
- Verwende die vorgegebenen CSS-Klassen (siehe unten)

STRUKTUR-TEMPLATE:

```html
<div class="slide-section">
    <div class="slide-title">Folie [X]: [Titel]</div>
    
    <div class="component" id="slide-[X]-comp-1">
        <div class="component-label">Komponente [X].1</div>
        <h2>[Komponenten-Titel]</h2>
        
        [Komponenten-Inhalt hier]
    </div>
    
    <div class="component" id="slide-[X]-comp-2">
        <div class="component-label">Komponente [X].2</div>
        <h2>[Komponenten-Titel]</h2>
        
        [Komponenten-Inhalt hier]
    </div>
    
    <!-- Weitere Komponenten... -->
</div>
```

VERFÜGBARE CSS-KLASSEN:

1. **Statistik-Grid:**
```html
<div class="stat-grid">
    <div class="stat-card">
        <span class="stat-number">83,6 Mio</span>
        <span class="stat-label">Einwohner Deutschland (2024)</span>
    </div>
    <!-- Weitere stat-cards... -->
</div>
```

2. **Aufzählungsliste:**
```html
<ul class="bullet-list">
    <li><strong>Fetter Text:</strong> Normaler Text</li>
    <li>Weiterer Punkt</li>
</ul>
```

3. **Zitat:**
```html
<div class="quote">
    "Dies ist ein wichtiges Zitat"
</div>
```

4. **Normaler Text:**
```html
<p>Text mit <strong>fetten</strong> und <code>code</code> Elementen.</p>
```

5. **Unter-Überschriften:**
```html
<h3>Sub-Titel</h3>
```

REGELN:

1. **Statistiken erkennen:** 
   - Zeilen mit Zahlen + Einheiten (Mio, Mrd, %, €, $) → `stat-grid`
   - Format: Zahl in `stat-number`, Rest in `stat-label`

2. **Aufzählungen:**
   - Normale Aufzählungen → `bullet-list`
   - **Fetter Text** → `<strong>`

3. **Zitate:**
   - Markdown `> Zitat` → `<div class="quote">`

4. **Komponenten-IDs:**
   - Format: `slide-[Foliennummer]-comp-[Komponentennummer]`
   - Beispiel: `slide-1-comp-1`, `slide-1-comp-2`, etc.

5. **Dateinamen:**
   - Format: `folie-[nummer]-[kurzer-titel].html`
   - Beispiel: `folie-01-problem.html`
   - Kleinbuchstaben, Bindestriche statt Leerzeichen

AUSGABE:

Erstelle für jede Folie (H1-Abschnitt) eine separate HTML-Datei.
Verwende KEINE <html>, <head>, <body> Tags - nur die Komponenten!

MEIN MARKDOWN:

[HIER MARKDOWN EINFÜGEN]
```

---

## Beispiel-Verwendung

### Input (Markdown):
```markdown
# Folie 1: Problem

## Demografische Daten

- 83,6 Mio Einwohner
- 5,7 Mio Pflegebedürftige

## Belastung

> "17 Millionen erwirtschaften für 90 Millionen"

- **52,9%** Belastungsquote
```

### Output (HTML) - Datei: `folie-01-problem.html`:
```html
<div class="slide-section">
    <div class="slide-title">Folie 1: Problem</div>
    
    <div class="component" id="slide-1-comp-1">
        <div class="component-label">Komponente 1.1</div>
        <h2>Demografische Daten</h2>
        
        <div class="stat-grid">
            <div class="stat-card">
                <span class="stat-number">83,6 Mio</span>
                <span class="stat-label">Einwohner</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">5,7 Mio</span>
                <span class="stat-label">Pflegebedürftige</span>
            </div>
        </div>
    </div>
    
    <div class="component" id="slide-1-comp-2">
        <div class="component-label">Komponente 1.2</div>
        <h2>Belastung</h2>
        
        <div class="quote">
            "17 Millionen erwirtschaften für 90 Millionen"
        </div>
        
        <ul class="bullet-list">
            <li><strong>52,9%</strong> Belastungsquote</li>
        </ul>
    </div>
</div>
```

---

## Workflow

### 1. Markdown vorbereiten
```bash
cd /home/ubuntudani/Projects/Robo4you/pitch
vim mein-pitch.md
```

### 2. LLM konvertieren
- Öffne Claude/ChatGPT
- Füge den Prompt oben ein
- Füge dein Markdown am Ende ein
- Lass konvertieren

### 3. HTML speichern
```bash
cd /home/ubuntudani/Projects/Robo4you/presentation/output
# Speichere jede generierte HTML-Datei einzeln
vim folie-01-problem.html
vim folie-02-loesung.html
# etc.
```

### 4. Anzeigen
```bash
cd /home/ubuntudani/Projects/Robo4you/presentation
open component-viewer.html
# Wähle Dateien im Dropdown aus
```

### 5. Screenshots erstellen
- Komponenten einzeln mit Browser-DevTools screenshotten
- Speichern als PNG
- In PowerPoint/Keynote einfügen

---

## Tipps für beste Ergebnisse

### ✅ Gutes Markdown

```markdown
# Folie 1: Klarer Titel

## Komponente mit Fokus

Kurzer erklärende Text.

- 83,6 Mio Einwohner (Statistiken mit Einheit)
- 5,7 Mio Pflegebedürftige

## Weitere Komponente

> Wichtige Zitate hervorheben

- **Fette Begriffe** für Hervorhebung
```

### ❌ Zu vermeiden

```markdown
# Zu lange Titel die über mehrere Zeilen gehen

## Komponente ohne Struktur
Alles in einem Block ohne Aufzählung oder Formatierung macht es schwer zu lesen

- Zu viel Text in einer Aufzählung die eigentlich ein ganzer Absatz ist und keine klare Aussage hat
```

---

## Automatisierung (Optional)

Falls Sie viele Folien haben, können Sie das Python-Script verwenden:

```bash
python markdown-to-components.py mein-pitch.md output/
```

Das Script generiert automatisch HTML-Dateien für alle Folien.

---

## Dateiliste aktualisieren

Nach dem Hinzufügen neuer HTML-Dateien:

1. Öffne `component-viewer.html`
2. Aktualisiere die `availableFiles` Array im Script:

```javascript
availableFiles = [
    'folie-01-problem.html',
    'folie-02-loesung.html',
    'folie-03-markt.html',
    // Ihre neuen Dateien hier
];
```

Oder: Verwenden Sie den "🔄 Neu laden" Button im Viewer (wenn automatische Erkennung implementiert ist).

---

## Support

Bei Fragen:
- Siehe `README-KOMPONENTEN.md` für Details
- Siehe `github-design-guide.md` für Styling
- Beispiele in `output/beispiel-*.html`


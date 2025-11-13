# Komponenten-basiertes Präsentationssystem

## Konzept

Statt ganzer Folien werden **einzelne Komponenten** erstellt, die Sie separat screenshotten können.

### Prinzip: 1 Markdown-Abschnitt = 1 Folie

```markdown
# Folie 1: Problem              ← Folie-Titel (H1)

## Demografischer Wandel         ← Komponente 1 (H2)
- Inhalt hier...

## Statistiken                   ← Komponente 2 (H2)
- Mehr Inhalt...

---                              ← Folie-Trenner

# Folie 2: Lösung               ← Nächste Folie
...
```

---

## Verwendung

### Methode 1: Web-Interface (Empfohlen)

1. **Datei öffnen:**
   ```bash
   open component-generator.html
   ```

2. **Markdown einfügen:**
   - Fügen Sie Ihr Markdown in das linke Textfeld ein
   - Oder klicken Sie auf "Beispiel laden"

3. **Komponenten generieren:**
   - Klick auf "✨ Komponenten generieren"
   - Rechts erscheinen die Komponenten nach Folien sortiert

4. **Screenshots erstellen:**
   - **Chrome DevTools:** Rechtsklick auf Komponente → "Untersuchen" → Screenshot des Elements
   - **Firefox:** Rechtsklick → "Screenshot des Knotens erstellen"
   - **Browser-Extension:** Nutzen Sie Tools wie "GoFullPage" für selektive Screenshots

---

### Methode 2: Python-Script (Batch-Verarbeitung)

```bash
python markdown-to-components.py input.md output/
```

---

## Markdown-Syntax

### Folie-Struktur

```markdown
# Folie-Titel (H1)            → Wird zur Folien-Überschrift

## Komponenten-Titel (H2)     → Wird zu einzelner Komponente
Inhalt der Komponente...

### Sub-Überschrift (H3)      → Innerhalb der Komponente

---                           → Trennt Folien
```

### Inhaltstypen

#### 1. Statistiken (automatisch erkannt)

```markdown
- 83,6 Mio Einwohner
- 5,7 Mio Pflegebedürftige
- 52,9% Belastungsquote
- 84.000 € Roboterpreis
```

→ Werden automatisch als **Statistik-Cards** dargestellt

#### 2. Aufzählungen

```markdown
- Normaler Punkt
- **Fettgedruckter** Text wird hervorgehoben
- `Code` in Backticks
```

→ Werden als **formatierte Liste** dargestellt

#### 3. Zitate

```markdown
> "Dies ist ein wichtiges Zitat"
```

→ Wird als **hervorgehobenes Blockquote** dargestellt

#### 4. Fließtext

```markdown
Dies ist normaler Text mit **fetten** und `code` Elementen.
```

---

## Komponenten-Typen (Automatisch)

Der Generator erkennt automatisch:

### 📊 Statistik-Komponenten
Wenn mehrere Zeilen mit Zahlen beginnen:
```markdown
## Markt-Daten
- 18.000 Einheiten (2025)
- $5 Billionen Marktvolumen
- 500.000 fehlende Pflegekräfte
```

### 📝 Text-Komponenten
Normale Absätze und Aufzählungen:
```markdown
## Problem
Der demografische Wandel stellt uns vor Herausforderungen:
- Alternde Gesellschaft
- Fachkräftemangel
```

### 💬 Zitat-Komponenten
Wichtige Aussagen hervorheben:
```markdown
## Vision
> "Die nächste industrielle Revolution hat bereits begonnen"
```

---

## Beispiel: Vollständige Folie

```markdown
# Folie 3: Markt & Opportunity

## Marktreife Modelle (2025)

Erste Roboter sind bereits verfügbar:

- **Unitree H1:** ~84.000 € (High-End)
- **1X NEO:** ~18.500 € (Service)
- **Unitree G1:** ~15.000 € (Bildung)
- **Unitree R1:** ~5.100 € (Entry)

## Marktprognosen

- 18.000 Einheiten weltweit (2025)
- >1 Mrd. Roboter bis 2050
- $5 Billionen Marktvolumen (Morgan Stanley)

> "Bank of America prognostiziert exponentielles Wachstum"

---

# Nächste Folie...
```

→ Erzeugt **2 Komponenten** für Folie 3:
1. Komponente 3.1: Marktreife Modelle (Liste)
2. Komponente 3.2: Marktprognosen (Statistiken + Zitat)

---

## Screenshot-Workflow

### 1. Chrome DevTools (Präzise)

1. `F12` oder `Strg+Shift+I` → DevTools öffnen
2. Element-Selektor aktivieren (`Strg+Shift+C`)
3. Komponente anklicken (`.component` div)
4. DevTools → 3-Punkte-Menü → "Capture node screenshot"

### 2. Browser-Extension (Schnell)

**Empfohlen:** "GoFullPage" oder "Awesome Screenshot"

1. Extension installieren
2. Extension aktivieren
3. Bereich auswählen (Komponente)
4. Screenshot speichern

### 3. System-Tool (Flexibel)

**Linux:** `gnome-screenshot -a` (Bereich auswählen)
**Windows:** `Win+Shift+S`
**Mac:** `Cmd+Shift+4`

---

## Styling-Optionen

Alle Komponenten verwenden das **GitHub-Design**:

- **Primärfarbe:** GitHub Green `#238636`
- **Schrift:** System-Font-Stack
- **Border-Radius:** 6px
- **Spacing:** 4px Grid-System

### Anpassungen

CSS-Variablen in `github-presentation-template.css`:

```css
:root {
  --github-green: #238636;
  --color-fg-default: #24292f;
  --color-border-default: #d0d7de;
}
```

---

## Vorteile dieses Systems

✅ **Flexibel:** Komponenten einzeln verwenden oder kombinieren
✅ **Effizient:** Nur benötigte Teile screenshotten
✅ **Wiederverwendbar:** Komponenten in mehreren Präsentationen nutzen
✅ **Wartbar:** Markdown als Single Source of Truth
✅ **Versionierbar:** Markdown in Git trackbar

---

## Workflow-Empfehlung

### 1. Content erstellen
```bash
vim pitch-deck.md   # Markdown schreiben
```

### 2. Komponenten generieren
```bash
open component-generator.html   # Markdown einfügen
```

### 3. Screenshots erstellen
- Komponenten einzeln screenshotten
- In `output/` Ordner speichern
- Naming: `folie-01-komponente-01.png`

### 4. In PowerPoint/Keynote einfügen
- Screenshots als Bilder einfügen
- Pro Folie: 1-3 Komponenten
- Flexibel kombinieren

---

## Ordnerstruktur

```
presentation/
├── component-generator.html        # Web-Interface (Haupttool)
├── markdown-to-components.py       # Python-Script (optional)
├── github-presentation-template.css # Styling
├── README-KOMPONENTEN.md           # Diese Anleitung
├── beispiel-pitch.md               # Beispiel-Markdown
└── output/                         # Screenshots hier speichern
    ├── folie-01-komponente-01.png
    ├── folie-01-komponente-02.png
    └── ...
```

---

## Tipps & Tricks

### ✨ Statistiken formatieren

**Gut:**
```markdown
- 83,6 Mio Einwohner
- 52,9% Belastungsquote
```

**Noch besser:**
```markdown
- 83,6 Mio Einwohner in Deutschland (2024)
- 52,9% Durchschnittliche Belastungsquote (2025)
```

→ Zusätzliche Infos werden als Label angezeigt

### 📐 Komponenten-Größe

Jede Komponente passt sich automatisch dem Inhalt an:
- **Kompakt:** Für Screenshots in Spalten
- **Weit:** Für volle Folienbreite

### 🎨 Dark Mode

Fügen Sie `.dark-mode` CSS-Klasse hinzu für dunkle Komponenten:
```html
<div class="component dark-mode">...</div>
```

---

## Nächste Schritte

1. ✅ `component-generator.html` öffnen
2. ✅ Beispiel laden und testen
3. ✅ Eigenes Markdown aus `pitch/` einfügen
4. ✅ Komponenten generieren & screenshotten
5. ✅ In PowerPoint/Keynote einfügen

---

## Support

Bei Fragen oder Problemen:
- Siehe `github-design-guide.md` für Styling-Infos
- Beispiele in `github-presentation-example.html`

**Viel Erfolg mit Ihrem Pitch! 🚀**


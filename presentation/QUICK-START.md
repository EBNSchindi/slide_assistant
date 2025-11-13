# 🚀 Quick Start - Komponenten-System

## In 5 Minuten zur ersten Komponente

### Schritt 1: Viewer öffnen

```bash
cd /home/ubuntudani/Projects/Robo4you/presentation
open component-viewer.html
```

Oder doppelklicken Sie auf `component-viewer.html` im Dateimanager.

---

### Schritt 2: Beispiel anschauen

Im Dropdown oben sehen Sie 3 Beispiel-Dateien:
- `beispiel 01 problem`
- `beispiel 02 loesung`  
- `beispiel 03 markt`

Wählen Sie eine aus und sehen Sie die Komponenten.

---

### Schritt 3: Eigenes Markdown schreiben

Erstellen Sie eine Markdown-Datei mit Ihrem Pitch-Deck:

```markdown
# Folie 1: Problem

## Demografische Krise

- 83,6 Mio Einwohner in Deutschland
- 5,7 Mio Pflegebedürftige
- 500.000 fehlende Pflegekräfte bis 2030

## Finanzielle Belastung

> "Mehr als die Hälfte des Einkommens geht an den Staat"

- **52,9%** Belastungsquote (2025)

---

# Folie 2: Lösung

## Robo4you Konzept

**Robotik as a Service** - Wir vermieten humanoide Roboter.

- 🤖 Hardware inklusive
- 🎓 Schulung & Coaching
- 🔧 Wartung & Support
```

---

### Schritt 4: LLM konvertieren

1. **Öffnen Sie Claude oder ChatGPT**

2. **Verwenden Sie diesen Prompt:**

```
Konvertiere das folgende Markdown in HTML-Komponenten.

REGELN:
- Jedes H1 (# Folie X) = 1 HTML-Datei
- Jedes H2 (## Titel) = 1 Komponente
- Statistiken (Zahlen + Einheit) in stat-grid
- Aufzählungen in bullet-list
- Zitate (> Text) in quote-div

TEMPLATE:
<div class="slide-section">
    <div class="slide-title">Folie [X]: [Titel]</div>
    
    <div class="component" id="slide-[X]-comp-1">
        <div class="component-label">Komponente [X].1</div>
        <h2>[Titel]</h2>
        [Inhalt]
    </div>
</div>

CSS-KLASSEN:
- stat-grid + stat-card (für Statistiken)
- bullet-list (für Aufzählungen)
- quote (für Zitate)

MEIN MARKDOWN:
[Hier Ihr Markdown einfügen]
```

3. **Fügen Sie Ihr Markdown am Ende ein**

4. **Lassen Sie konvertieren**

---

### Schritt 5: HTML speichern

1. Kopieren Sie die generierte HTML
2. Speichern Sie in `output/` Ordner:

```bash
cd /home/ubuntudani/Projects/Robo4you/presentation/output
vim folie-01-problem.html
# Fügen Sie HTML ein, speichern mit :wq
```

3. Dateinamen-Format: `folie-[nr]-[kurztitel].html`
   - ✅ `folie-01-problem.html`
   - ✅ `folie-02-loesung.html`
   - ❌ `Folie 1 - Problem.html` (Leerzeichen, Großbuchstaben)

---

### Schritt 6: Im Viewer anzeigen

1. **Dateiliste aktualisieren:**
   - Öffnen Sie `component-viewer.html` in einem Editor
   - Suchen Sie nach `availableFiles = [`
   - Fügen Sie Ihre Datei hinzu:

```javascript
availableFiles = [
    'beispiel-01-problem.html',
    'beispiel-02-loesung.html',
    'beispiel-03-markt.html',
    'folie-01-problem.html',  // ← Ihre neue Datei
    'folie-02-loesung.html',  // ← Ihre neue Datei
];
```

2. **Speichern und neu laden:**
   - Browser neu laden (`Strg+R` / `Cmd+R`)
   - Ihre Dateien erscheinen im Dropdown

---

### Schritt 7: Screenshots erstellen

#### Methode 1: Chrome DevTools (Empfohlen)

1. `F12` oder `Strg+Shift+I` → DevTools öffnen
2. Element-Selektor aktivieren (`Strg+Shift+C`)
3. Komponente anklicken
4. DevTools → 3-Punkte-Menü → "Capture node screenshot"
5. Screenshot wird heruntergeladen

#### Methode 2: Firefox

1. Rechtsklick auf Komponente
2. "Screenshot des Knotens erstellen"
3. Screenshot wird gespeichert

#### Methode 3: Browser-Extension

- **Awesome Screenshot** (Chrome/Firefox)
- **GoFullPage** (Chrome)

1. Extension installieren
2. Komponente auswählen
3. Screenshot erstellen

---

## Workflow-Übersicht

```
📝 Markdown schreiben
    ↓
🤖 LLM konvertieren (Claude/GPT)
    ↓
💾 HTML in output/ speichern
    ↓
📋 In Viewer-Liste eintragen
    ↓
🖥️ Im Viewer anzeigen
    ↓
📸 Komponenten screenshotten
    ↓
📊 In PowerPoint/Keynote einfügen
```

---

## Nützliche Tastenkombinationen

- `Strg+K` / `Cmd+K` - Fokus auf Datei-Dropdown
- `F12` - DevTools öffnen (für Screenshots)
- `Strg+R` / `Cmd+R` - Seite neu laden

---

## Troubleshooting

### Problem: "Datei konnte nicht geladen werden"

**Lösung:**
- Prüfen Sie den Dateipfad in `output/`
- Dateiname muss genau mit Eintrag in `availableFiles` übereinstimmen
- Browser-Cache leeren (`Strg+Shift+R`)

### Problem: "Komponenten sehen falsch aus"

**Lösung:**
- Prüfen Sie, ob CSS-Klassen korrekt verwendet wurden
- Siehe `LLM-PROMPT.md` für korrekte Struktur
- Vergleichen Sie mit Beispiel-Dateien

### Problem: "Dropdown ist leer"

**Lösung:**
- Öffnen Sie `component-viewer.html` in Editor
- Prüfen Sie `availableFiles` Array
- Fügen Sie Ihre Dateien manuell hinzu

---

## Beispiel-Dateien

Im `output/` Ordner finden Sie:
- ✅ `beispiel-01-problem.html` - Demografische Daten
- ✅ `beispiel-02-loesung.html` - Robo4you Konzept
- ✅ `beispiel-03-markt.html` - Marktanalyse

Diese können Sie als Vorlage verwenden!

---

## Weiterführende Dokumentation

- 📖 **README-KOMPONENTEN.md** - Ausführliche Anleitung
- 🎨 **github-design-guide.md** - Design-System
- 🤖 **LLM-PROMPT.md** - Detaillierter Prompt für LLM
- 📝 **beispiel-pitch.md** - Vollständiges Pitch-Deck Beispiel

---

## Nächste Schritte

1. ✅ Öffnen Sie `component-viewer.html`
2. ✅ Schauen Sie sich die Beispiele an
3. ✅ Schreiben Sie Ihr erstes Markdown
4. ✅ Lassen Sie es vom LLM konvertieren
5. ✅ Speichern und anzeigen
6. ✅ Screenshots erstellen

**Viel Erfolg! 🚀**


# 📊 Robo4you Präsentations-System

## 🎯 Übersicht

Dieses System hilft Ihnen, aus Markdown-Pitch-Decks einzelne Screenshot-bare Komponenten zu erstellen.

**Konzept:** 1 Markdown-Abschnitt = 1 Folie mit mehreren Komponenten

---

## 📁 Wichtige Dateien

### 🚀 Haupt-Tool

| Datei | Beschreibung |
|-------|--------------|
| **`component-viewer.html`** | 🎯 **HAUPTTOOL** - Zeigt generierte HTML-Komponenten an |
| `QUICK-START.md` | 📖 5-Minuten Schnellstart-Anleitung |
| `README-KOMPONENTEN.md` | 📚 Ausführliche Dokumentation |

### 🤖 LLM-Integration

| Datei | Beschreibung |
|-------|--------------|
| `LLM-PROMPT.md` | 🤖 Prompt für Claude/ChatGPT zur Markdown→HTML Konvertierung |
| `beispiel-pitch.md` | 📝 Vollständiges Beispiel-Pitch-Deck |

### 🎨 Design & Styling

| Datei | Beschreibung |
|-------|--------------|
| `github-presentation-template.css` | 🎨 Haupt-Stylesheet (GitHub-Design) |
| `github-design-guide.md` | 📐 Design-System Dokumentation |
| `github-presentation-example.html` | 💡 Design-Beispiele |

### 📂 Output-Ordner

| Ordner | Beschreibung |
|--------|--------------|
| `output/` | 💾 Hier werden generierte HTML-Komponenten gespeichert |
| `output/beispiel-*.html` | ✨ Beispiel-Komponenten (3 Folien) |

### 🛠️ Optional / Alt

| Datei | Beschreibung |
|-------|--------------|
| `markdown-to-components.py` | 🐍 Python-Script für Batch-Konvertierung (optional) |
| `template-*.html` | 📋 Alte Vollfolien-Templates (Legacy) |

---

## 🔄 Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    1. MARKDOWN SCHREIBEN                     │
│                                                              │
│   # Folie 1: Problem                                         │
│   ## Komponente 1                                            │
│   - Inhalt hier...                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              2. LLM KONVERTIEREN (Claude/GPT)                │
│                                                              │
│   → LLM-PROMPT.md verwenden                                  │
│   → Markdown einfügen                                        │
│   → HTML-Komponenten generieren lassen                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                3. HTML IN output/ SPEICHERN                  │
│                                                              │
│   output/folie-01-problem.html                               │
│   output/folie-02-loesung.html                               │
│   output/folie-03-markt.html                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            4. COMPONENT-VIEWER.HTML ÖFFNEN                   │
│                                                              │
│   → Dropdown: Datei auswählen                                │
│   → Komponenten werden angezeigt                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              5. KOMPONENTEN SCREENSHOTTEN                    │
│                                                              │
│   Chrome DevTools: Element → Screenshot                      │
│   Firefox: Rechtsklick → Screenshot des Knotens              │
│   Extension: Awesome Screenshot / GoFullPage                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│          6. IN POWERPOINT/KEYNOTE EINFÜGEN                   │
│                                                              │
│   Screenshots als Bilder einfügen                            │
│   Pro Folie: 1-3 Komponenten kombinieren                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Schnellstart

### Option 1: Mit Beispielen starten (Empfohlen)

```bash
cd /home/ubuntudani/Projects/Robo4you/presentation
open component-viewer.html
```

→ Im Dropdown: Beispiele anschauen
→ Verstehen, wie Komponenten aussehen
→ Als Vorlage verwenden

### Option 2: Eigenes Pitch-Deck erstellen

```bash
# 1. Markdown schreiben
vim mein-pitch.md

# 2. Mit LLM konvertieren (siehe LLM-PROMPT.md)

# 3. HTML speichern
vim output/folie-01-problem.html

# 4. Viewer öffnen
open component-viewer.html
```

---

## 📚 Dokumentation

### Für Einsteiger
1. 📖 **QUICK-START.md** - In 5 Minuten loslegen
2. 🤖 **LLM-PROMPT.md** - Wie man LLM zur Konvertierung nutzt
3. ✨ `output/beispiel-*.html` - Beispiele anschauen

### Für Fortgeschrittene
1. 📚 **README-KOMPONENTEN.md** - Vollständige Dokumentation
2. 🎨 **github-design-guide.md** - Design-System verstehen
3. 🐍 **markdown-to-components.py** - Automatisierung

---

## 🎨 Verfügbare Komponenten-Typen

### 📊 Statistik-Cards
```html
<div class="stat-grid">
    <div class="stat-card">
        <span class="stat-number">83,6 Mio</span>
        <span class="stat-label">Einwohner Deutschland</span>
    </div>
</div>
```

### 📝 Aufzählungen
```html
<ul class="bullet-list">
    <li><strong>Fett:</strong> Normal</li>
</ul>
```

### 💬 Zitate
```html
<div class="quote">
    "Wichtiges Zitat hier"
</div>
```

### 📄 Text
```html
<p>Text mit <strong>fett</strong> und <code>code</code></p>
```

---

## 💡 Tipps

### ✅ Best Practices

1. **Kurze Komponenten:** 1 Komponente = 1 Aussage
2. **Klare Titel:** Jede Komponente braucht einen H2-Titel
3. **Statistiken gruppieren:** 2-4 Stats pro Grid
4. **Konsistent:** Gleiches Format für ähnliche Inhalte

### ❌ Zu vermeiden

1. ❌ Zu viel Text in einer Komponente
2. ❌ Mehr als 3-4 Komponenten pro Folie
3. ❌ Inkonsistente Formatierung
4. ❌ Fehlende Komponenten-Labels

---

## 🔧 Anpassungen

### Farben ändern

Bearbeiten Sie `github-presentation-template.css`:

```css
:root {
  --github-green: #238636;  /* Ihre Primärfarbe */
  --color-fg-default: #24292f;
}
```

### Neue Komponenten-Typen

Fügen Sie CSS-Klassen in `github-presentation-template.css` hinzu.

---

## 📦 Ordnerstruktur

```
presentation/
│
├── 🚀 HAUPTTOOLS
│   ├── component-viewer.html          ← Viewer (Haupttool)
│   ├── QUICK-START.md                 ← 5-Min Anleitung
│   └── INDEX.md                       ← Diese Datei
│
├── 📖 DOKUMENTATION
│   ├── README-KOMPONENTEN.md          ← Vollständige Docs
│   ├── LLM-PROMPT.md                  ← LLM-Integration
│   └── github-design-guide.md         ← Design-System
│
├── 🎨 STYLING
│   ├── github-presentation-template.css
│   └── github-presentation-example.html
│
├── 📝 BEISPIELE
│   └── beispiel-pitch.md              ← Vollständiges Beispiel
│
├── 📂 OUTPUT
│   └── output/
│       ├── beispiel-01-problem.html
│       ├── beispiel-02-loesung.html
│       └── beispiel-03-markt.html
│
└── 🛠️ OPTIONAL
    ├── markdown-to-components.py      ← Python-Script
    └── template-*.html                ← Legacy Templates
```

---

## ❓ Häufige Fragen

### Q: Muss ich programmieren können?

**A:** Nein! Sie schreiben Markdown, ein LLM (Claude/ChatGPT) macht die Konvertierung.

### Q: Welchen LLM soll ich verwenden?

**A:** 
- ✅ **Claude 3.5 Sonnet** (Empfohlen)
- ✅ **ChatGPT-4** (Gut)
- ⚠️ **GPT-3.5** (OK, manchmal Fehler)

### Q: Kann ich das Python-Script verwenden statt LLM?

**A:** Ja! `python markdown-to-components.py input.md output/`

Aber: LLM ist flexibler und versteht Kontext besser.

### Q: Wie viele Komponenten pro Folie?

**A:** Ideal: 2-3 Komponenten. Maximum: 4-5.

### Q: Kann ich das Design anpassen?

**A:** Ja! Bearbeiten Sie `github-presentation-template.css`

### Q: Funktioniert das offline?

**A:** 
- ✅ **Viewer:** Ja (lokale HTML-Datei)
- ❌ **LLM-Konvertierung:** Nein (braucht Internet)
- ✅ **Python-Script:** Ja (wenn Python installiert)

---

## 🆘 Support

### Problem-Lösung

| Problem | Lösung | Siehe |
|---------|--------|-------|
| Viewer zeigt nichts an | Datei in `output/` speichern und in `availableFiles` eintragen | QUICK-START.md |
| Komponenten sehen falsch aus | CSS-Klassen prüfen, Beispiele vergleichen | LLM-PROMPT.md |
| LLM macht Fehler | Prompt aus LLM-PROMPT.md genau verwenden | LLM-PROMPT.md |
| Screenshots unscharf | Browser-Zoom auf 100%, DevTools verwenden | QUICK-START.md |

### Weitere Hilfe

1. 📖 Dokumentation lesen (README-KOMPONENTEN.md)
2. ✨ Beispiele anschauen (output/beispiel-*.html)
3. 🔍 Markdown mit Beispielen vergleichen (beispiel-pitch.md)

---

## 🎯 Nächste Schritte

### Für Erste Schritte:
1. ✅ Öffnen Sie `component-viewer.html`
2. ✅ Schauen Sie die Beispiele an
3. ✅ Lesen Sie `QUICK-START.md`

### Für Ihr Pitch-Deck:
1. ✅ Öffnen Sie `LLM-PROMPT.md`
2. ✅ Schreiben Sie Ihr Markdown
3. ✅ Lassen Sie es vom LLM konvertieren
4. ✅ Screenshots erstellen

---

## 📄 Lizenz

Diese Templates verwenden das GitHub Design System als Inspiration.
Für eigenen Gebrauch bestimmt.

---

**Viel Erfolg mit Ihrem Pitch! 🚀**

*Erstellt für Robo4you - Robotik as a Service*


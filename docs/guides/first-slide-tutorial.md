# Deine erste Folie in 5 Minuten

Willkommen! Diese Anleitung zeigt dir, wie du in wenigen Minuten deine erste AI-generierte Präsentationsfolie erstellst.

---

## Voraussetzungen (5 Minuten Setup)

### 1. Server starten
Öffne ein Terminal im `presentation/`-Verzeichnis:

```bash
# API-Server starten
cd presentation
python3 run_api.py
```

Du solltest sehen:
```
INFO:     Uvicorn running on http://localhost:8001
```

### 2. Editor öffnen
Öffne in deinem Browser:
```
file:///home/dani/Schreibtisch/cursor_dev/slide_assistant/presentation/unified-editor.html
```

Oder verwende einen lokalen Server um CORS-Fehler zu vermeiden:
```bash
# In einem neuen Terminal (im presentation/-Verzeichnis)
python3 -m http.server 8000
# Dann: http://localhost:8000/unified-editor.html
```

---

## Schritt 1: Projekt auswählen

![Editor Header](../assets/screenshots/editor-header.png)

Im Header-Bereich oben findest du mehrere Dropdown-Felder:

**Projekt-Auswahl:**
```
[Projekt: beispiel-projekt ▼]
```

Wähle ein vorhandenes Projekt aus. Standardmäßig ist `beispiel-projekt` verfügbar.

**Hinweis:** Das Projekt definiert, wo deine generierten Folien gespeichert werden:
- Markdown: `projects/{name}/markdown/optimized/`
- HTML: `projects/{name}/html/`

---

## Schritt 2: Theme wählen

**Theme-Auswahl:**
```
[Theme: github ▼]
```

Verfügbare Themes:
- **github** (Standard) - Professionell, sauber, grüner Akzent
- **modern** - Zeitgenössisch, balanced
- **minimal** - Reduziert, simpel
- **apple** - Minimalistisch, Apple Blue
- **openai** - Modern, warm, OpenAI Teal

Das Theme bestimmt:
- Farben & Schriftarten
- Komponenten-Styling
- Gesamteindruck der Folie

Für dieses Tutorial: **github** ist ein guter Standard-Start.

---

## Schritt 3: Modell auswählen (optional)

**Modell-Dropdown:**
```
[Modell: auto ▼]
```

Verfügbare Optionen:
- **auto** (Standard) - Auto-Erkennung basierend auf API-Keys
- **gpt-4o** - OpenAI GPT-4 Turbo (schnell, zuverlässig)
- **gpt-5** - OpenAI GPT-5 (beste Qualität)
- **claude-sonnet-4.5** - Anthropic Claude (analytisch)
- **gemini-3.0-pro** - Google Gemini (vielseitig)

Für Anfänger: **gpt-4o** ist ein guter Kompromiss zwischen Geschwindigkeit und Qualität.

---

## Schritt 4: Foliendaten eingeben

Linke Seite - Textarea mit Beschriftung:

```
Folienn: [46]
Titel: [Unsere Strategie]
```

Gib folgende Informationen ein:

### Foliennummer
```
46
```

Eine Nummer für die Datei. Hilfreich für die Sortierung.

### Folientitel
```
Unsere Strategie
```

Der Titel, der oben auf der Folie angezeigt wird.

### Inhalt (große Textarea)
Dies ist die Hauptingabe. Hier einige Beispiele:

**Beispiel 1: Statistiken**
```
Unser Wachstum 2024:
- Umsatz: €12,3 Mio (+45%)
- Kunden: 8.500 (+120%)
- Mitarbeiter: 145 (+35%)
- Märkte: 12 Länder
```

**Beispiel 2: Aufzählung**
```
Kernkompetenzen:
- Cloud-Native Architektur
- Machine Learning & AI
- Agile Development
- Enterprise Security
- 24/7 Support
```

**Beispiel 3: Zitat**
```
"Die beste Technologie ist unsichtbar"
- Steve Jobs
```

**Beispiel 4: Gemischter Inhalt**
```
Unsere Vision:

Wir bauen die zukunftssichere Lösung für digitale Transformation.

Schlüsselmetriken:
- 99.99% Verfügbarkeit
- < 100ms Latenz
- ISO 27001 zertifiziert

Nächste Meilensteine:
1. AI-Integration (Q1 2025)
2. Europäische Expansion (Q2 2025)
3. Fortune 500 Partnerschaften (Q3 2025)
```

---

## Schritt 5: Folie generieren

Große grüne Button unten:
```
[✨ Folie generieren]
```

Klicke drauf. Du solltest sehen:
1. Kurzer Ladebalken
2. "Generiere Folie..." Status
3. Nach 3-5 Sekunden: Die generierte Folie auf der rechten Seite

**Was passiert im Hintergrund:**
1. **ContentAnalyzerV2** - Versteht deinen Input (Statistiken? Liste? Zitat?)
2. **PresentationStrategistV2** - Plant das Layout (1-3 Komponenten)
3. **ContentGeneratorV2** - Generiert formatierten Text
4. **Jinja2 Renderer** - Rendert HTML aus Template
5. **FileService** - Speichert Dateien

---

## Schritt 6: Vorschau & Export

### Vorschau (rechte Seite)
- Live-Preview der generierten Folie
- Zeigt wie sie in PowerPoint/Keynote aussieht
- Kann mehrmals generiert werden

### Speichern & Export
Die Folie wird automatisch gespeichert in:

```
projects/beispiel-projekt/
├── markdown/optimized/
│   └── folie-46-unsere-strategie.md
└── html/
    └── folie-46-unsere-strategie.html
```

### Screenshots für PowerPoint/Keynote
1. Rechts-Klick auf Preview → "Screenshot speichern"
2. Oder: Browser DevTools (F12) → Element Inspector
3. Oder: Zoom zu 100% → Print-Screen → In PowerPoint einfügen

---

## Praktische Beispiele

### Beispiel 1: KPI-Slide (2 Min)

**Input:**
```
Geschäftstätigkeitsbericht Q4 2024

Gesamtumsatz: €42,5 Mio
Wachstum YoY: +18%
EBITDA: €8,7 Mio
Gewinnmarge: 20,5%
Kundenanzahl: 12.340
Kundenakquisitionskosten: €320
```

**Output:**
- Komponente 1: `stat-grid` mit 6 Karten
- Clean, professionell, leicht zu lesen

---

### Beispiel 2: Prozess-Slide (2 Min)

**Input:**
```
Unser Projektmanagement-Prozess:

Phase 1: Discovery (Woche 1-2)
- Anforderungsaufnahme
- Stakeholder-Interviews
- Risikoanalyse

Phase 2: Design (Woche 3-4)
- Wireframes & Prototypen
- Design-Reviews
- Kundenfreigabe

Phase 3: Entwicklung (Woche 5-10)
- Agile Sprints (2 Wochen)
- Daily Standups
- Kontinuierliches Testing

Phase 4: Launch (Woche 11)
- Performance-Tests
- Security-Audit
- Go-Live
```

**Output:**
- Komponente 1: `text` mit Phasen
- Strukturiert, chronologisch, leicht zu folgen

---

### Beispiel 3: Feature-Slide (2 Min)

**Input:**
```
Was macht unsere Lösung einzigartig?

1. Echtzeitverarbeitung
Verarbeite Millionen von Datenpunkten pro Sekunde ohne Latenz. Unsere proprietäre Engine garantiert < 100ms Latenz.

2. AI-gestützte Insights
Automatische Anomalien-Erkennung und prädiktive Analysen. Machine Learning Modelle trainieren sich selbst.

3. Enterprise-Grade Sicherheit
ISO 27001, SOC2, GDPR-konform. End-to-End Verschlüsselung. Reguläre Sicherheitsaudits.
```

**Output:**
- Komponente 1: `bullet-list` mit Features
- Professionell, feature-fokussiert

---

## Troubleshooting

### Problem: "API-Fehler" beim Generieren

**Lösung 1:** Prüfe, ob Server läuft
```bash
curl http://localhost:8001/health
# Sollte: {"status": "ok"} zurückgeben
```

**Lösung 2:** Prüfe API-Key in `.env`
```bash
cd presentation/api
cat .env | grep OPENAI_API_KEY
# Sollte nicht leer sein
```

**Lösung 3:** Browser-Konsole öffnen (F12)
Sehe nach roten Fehlern in der Konsole.

---

### Problem: Folie sieht falsch aus

**Lösung 1:** Versuche verschiedene Themes
Manchmal funktioniert ein anderes Theme besser.

**Lösung 2:** Vereinfache deinen Input
Zu viel Text? Teile in mehrere Folien auf.

**Lösung 3:** Nutze Schlüsselwörter
"Statistiken:", "Schritte:", "Features:" helfen dem System.

---

### Problem: CORS-Fehler

**Lösung:** Verwende lokalen Server:
```bash
cd presentation
python3 -m http.server 8000
# Dann: http://localhost:8000/unified-editor.html
```

---

## Nächste Schritte

1. **Weitere Folien generieren** - Probiere verschiedene Inhaltstypen
2. **Themes erkunden** - Schau dir die anderen Themes an
3. **Themes anpassen** - [Theme Creation Guide](theme-creation/)
4. **Batch-Generierung** - [API-Dokumentation](../api/endpoints.md)

---

## Checkliste: Deine erste Folie

- [ ] Server läuft auf http://localhost:8001
- [ ] Editor geöffnet: `unified-editor.html`
- [ ] Projekt ausgewählt: `beispiel-projekt`
- [ ] Theme ausgewählt: `github` (oder favorit)
- [ ] Foliendaten eingegeben (Nummer, Titel, Inhalt)
- [ ] ✨ Folie generiert" angeklickt
- [ ] Folie angezeigt auf rechter Seite
- [ ] Gegrübelt: Looks gut! Oder: "Regeneriere mit anderem Input"
- [ ] Datei exportiert: `.md` und `.html` in `projects/`

---

## Tipps & Tricks

### Schnelles Iterieren
```
Input schreiben → Generieren → Nicht zufrieden? → Input anpassen → Generieren
```

Nutze den gleichen Input mehrfach. Das System generiert jedes Mal anders.

### Langsamer Input
"Sehr wichtig für die Folie: Zunächst das Problem, dann die Lösung"
→ System verstehts besser

### Bilder einbinden
Speichere Bilder in `projects/beispiel-projekt/images/uploads/`
Dann im Input: `Bild: bild-name.png` oder `Foto: team.jpg`

### Markdown manuell anpassen
Die generierten `.md` Dateien kannst du manuell bearbeiten und dann regenerieren.

---

## Weitere Ressourcen

- **[API-Dokumentation](../api/endpoints.md)** - Vollständige Endpoint-Referenz
- **[Komponenten-Referenz](../reference/components.md)** - Alle 10 Komponenten erklärt
- **[System-Architektur](../reference/architecture.md)** - Wie das System intern funktioniert
- **[Theme-Erstellung](theme-creation/)** - Eigene Themes bauen

---

**Viel Spaß beim Erstellen deiner ersten Folien! 🚀**

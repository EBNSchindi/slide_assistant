# GitHub Design Pitch Deck Templates

Vier verschiedene Startup-Pitch-Deck-Templates im GitHub-Design-Stil, optimiert für 16:9 Format (1920x1080px) zum Screenshoten.

## Templates

### Template 1: Classic (`template-1-classic.html`)
**Stil:** Klassisches Pitch-Deck mit Cards und Grid-Layouts
**Besonderheiten:**
- Strukturierte Card-basierte Layouts
- Klare Grid-Systeme für Inhalte
- Traditionelle Pitch-Deck-Struktur
- Ideal für: Standard-Pitch-Präsentationen

**Slides:**
1. Titel
2. Problem (3 Cards)
3. Lösung (Split Layout)
4. Markt & Opportunity (4 Statistik-Cards)
5. Geschäftsmodell (3 Revenue Streams)
6. Traction & Metrics (Charts & Progress Bars)
7. Wettbewerb & Differenzierung (Vergleichstabelle)
8. Team (3 Team-Mitglieder)
9. Roadmap (Timeline)
10. Investment Opportunity

---

### Template 2: Modern (`template-2-modern.html`)
**Stil:** Modern mit großen visuellen Elementen
**Besonderheiten:**
- Große Hero-Sections
- Visuelle Elemente im Fokus
- Gradient-Hintergründe
- Moderne Typografie
- Ideal für: Visuell ansprechende Präsentationen

**Slides:**
1. Hero Titel mit Badges
2. Problem mit großem Impact
3. Lösung mit visueller Darstellung
4. Markt mit großen Zahlen
5. Geschäftsmodell visuell (3 Pricing-Tiers)
6. Traction mit visuellen Elementen
7. Wettbewerb visuell
8. Team modern (4 Team-Mitglieder)
9. Roadmap visuell (4 Quartale)
10. Ask modern

---

### Template 3: Minimal (`template-3-minimal.html`)
**Stil:** Minimalistisch mit viel Whitespace
**Besonderheiten:**
- Viel Whitespace
- Fokus auf Typografie
- Minimalistische Designelemente
- Klare Linien und Divider
- Ideal für: Elegante, reduzierte Präsentationen

**Slides:**
1. Titel minimal
2. Problem minimal
3. Lösung minimal (3 Features)
4. Markt minimal (2 große Zahlen)
5. Geschäftsmodell minimal (Liste)
6. Traction minimal (4 Metriken)
7. Wettbewerbsvorteil (Vergleich)
8. Team minimal (3 Team-Mitglieder)
9. Roadmap minimal (Liste)
10. Investment minimal

---

### Template 4: Data Driven (`template-4-data-driven.html`)
**Stil:** Datengetrieben mit vielen Statistiken
**Besonderheiten:**
- Viele Charts und Diagramme
- Detaillierte Metriken
- Tabellen und Vergleichsdaten
- Unit Economics
- Ideal für: Datenfokussierte Präsentationen

**Slides:**
1. Titel mit Zahlen (4 Key Metrics)
2. Problem in Zahlen (Charts & Daten)
3. Lösung mit Metriken (ROI Berechnung)
4. Geschäftsmodell & Unit Economics
5. Traction & Wachstum (detailliert)
6. Wettbewerbsanalyse (Tabelle)
7. Team & Expertise (mit Metriken)
8. Roadmap & Meilensteine (mit Progress Bars)
9. Investment Opportunity (detaillierte Zahlen)

---

## Verwendung

### 1. Template auswählen
Öffnen Sie die gewünschte HTML-Datei in einem Browser:
- `template-1-classic.html`
- `template-2-modern.html`
- `template-3-minimal.html`
- `template-4-data-driven.html`

### 2. Inhalte anpassen
Bearbeiten Sie die HTML-Datei und passen Sie die Platzhaltertexte an:
- Startup Name
- Problem-Beschreibungen
- Lösung-Details
- Zahlen und Statistiken
- Team-Informationen
- etc.

### 3. Screenshots erstellen
Da jedes Slide genau 1920x1080px groß ist, können Sie:
- **Browser DevTools:** F12 → Device Toolbar → Custom → 1920x1080
- **Screenshot-Tools:** Verwenden Sie Tools wie:
  - Browser-Erweiterungen für Full-Page Screenshots
  - Screenshot-Software mit festen Dimensionen
  - Browser DevTools Screenshot-Funktion

### 4. Anpassungen
Alle Templates verwenden die gemeinsame CSS-Datei `github-presentation-template.css`. Sie können:
- Farben über CSS-Variablen ändern
- Schriftgrößen anpassen
- Layouts modifizieren
- Neue Slides hinzufügen

---

## Design-System

### Farben
- **Primär:** GitHub Green `#238636`
- **Text:** `#24292f` (Light) / `#c9d1d9` (Dark)
- **Akzent:** Blau `#0969da`
- **Hintergrund:** `#ffffff` (Light) / `#0d1117` (Dark)

### Typografie
- **Font Stack:** System Fonts (-apple-system, BlinkMacSystemFont, Segoe UI, etc.)
- **Titel:** 48-72px, Bold (700)
- **Überschriften:** 24-32px, SemiBold (600)
- **Text:** 16-20px, Regular (400)

### Spacing
- Basis-Einheit: 4px
- Kleine Abstände: 4px, 8px
- Mittlere Abstände: 16px, 24px
- Große Abstände: 32px, 48px

### Border Radius
- Klein: 3px
- Mittel: 6px
- Groß: 12px

---

## Tipps für Screenshots

1. **Browser-Zoom:** Stellen Sie sicher, dass der Browser-Zoom auf 100% steht
2. **Viewport:** Verwenden Sie Browser DevTools, um den Viewport auf 1920x1080px einzustellen
3. **Full-Page Screenshot:** Nutzen Sie Browser-Erweiterungen für Full-Page Screenshots
4. **Einzelne Slides:** Jedes `<section class="slide">` ist ein einzelnes Slide

---

## Anpassungen

### Farben ändern
Bearbeiten Sie die CSS-Variablen in `github-presentation-template.css`:
```css
:root {
  --github-green: #238636; /* Ihre Farbe */
  --color-fg-default: #24292f; /* Textfarbe */
  /* etc. */
}
```

### Neue Slides hinzufügen
Kopieren Sie ein bestehendes `<section class="slide">` und passen Sie den Inhalt an.

### Layout ändern
Verwenden Sie die vorhandenen Utility-Klassen:
- `.grid` - Grid-Layout
- `.grid-2`, `.grid-3`, `.grid-4` - Spaltenanzahl
- `.card` - Card-Container
- `.split-layout` - Zwei-Spalten-Layout

---

## Dateien

- `github-presentation-template.css` - Gemeinsame Stylesheet
- `github-design-guide.md` - Design-Dokumentation
- `template-1-classic.html` - Klassisches Template
- `template-2-modern.html` - Modernes Template
- `template-3-minimal.html` - Minimalistisches Template
- `template-4-data-driven.html` - Datengetriebenes Template

---

## Lizenz

Diese Templates verwenden das GitHub Design System als Inspiration und sind für den eigenen Gebrauch bestimmt.



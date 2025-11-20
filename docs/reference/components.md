# Komponenten-Referenz

Vollständige Dokumentation aller 10 verfügbaren Slide-Komponenten mit Beschreibungen, Anwendungsfällen, Slots, CSS-Klassen und Beispielen.

---

## Übersicht

Das System unterstützt 10 spezialisierte Komponenten-Typen für verschiedene Inhaltstypen:

| Komponente | Typ | Verwendung | Max. Items |
|------------|-----|-----------|-----------|
| **stat-grid** | Statistiken | KPIs, Metriken, Zahlen | 4-6 |
| **bullet-list** | Listen | Aufzählungen, Features | 5-7 |
| **quote** | Text | Zitate, Testimonials | 1 |
| **text** | Text | Fließtext, Paragraphen | 3-5 |
| **table** | Daten | Vergleiche, Tabellen | - |
| **image-frame** | Medien | Einzelbild mit Caption | 1 |
| **image-grid** | Medien | Multi-Bilder Grid | 4-6 |
| **feature-grid** | Content | Features mit Icons | 3-4 |
| **process** | Struktur | Schritte vertikal | 3-5 |
| **process-horizontal** | Struktur | Schritte horizontal | 3-5 |

---

## 1. Stat-Grid

**Type:** `stat-grid`

Zeigt Statistiken und Kennzahlen in einer Grid-Layout (Karten-Format).

### Verwendung

Ideal für:
- **KPI-Displays** (Umsatz, Gewinn, Wachstum)
- **Metriken** (Kundenzahl, Mitarbeiter, Märkte)
- **Vergleiche** (Aktuell vs. Vorjahr)
- **Finanzielle Daten** (€, %, Mio, Mrd)

### Slots

```
{
  "type": "stat-grid",
  "title": "string (optional)",
  "subtitle": "string (optional)",
  "stats": [
    {
      "value": "string (required)",
      "unit": "string (optional)",
      "label": "string (required)",
      "source": "string (optional)"
    }
  ]
}
```

### Slot-Details

**title**: Überschrift der Komponente
```
"Geschäftsergebnisse 2024"
```

**subtitle**: Zusätzliche Erklärung
```
"Alle Zahlen in EUR"
```

**stats**: Array mit Statistiken

**value**: Die Zahl oder Metrik
```
"€42,5 Mio" oder "12.340" oder "+18%"
```

**unit**: Einheit (optional, wenn in value nicht enthalten)
```
"EUR", "Kunden", "%"
```

**label**: Beschriftung der Statistik
```
"Gesamtumsatz 2024"
```

**source**: Datenquelle (optional)
```
"(Bank of America Daten)"
```

### CSS-Klassen

```css
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: var(--component-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 20px;
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-color);
  display: block;
  margin-bottom: 8px;
}

.stat-number .unit {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}
```

### Beispiel-JSON

```json
{
  "type": "stat-grid",
  "title": "Geschäftsergebnisse 2024",
  "subtitle": "Alle Zahlen in EUR",
  "stats": [
    {
      "value": "€42,5",
      "unit": "Mio",
      "label": "Gesamtumsatz",
      "source": "Jahresbericht 2024"
    },
    {
      "value": "+18",
      "unit": "%",
      "label": "Wachstum YoY"
    },
    {
      "value": "8.500",
      "label": "Kunden weltweit"
    },
    {
      "value": "145",
      "label": "Mitarbeiter"
    },
    {
      "value": "€2,1",
      "unit": "Mio",
      "label": "EBITDA"
    },
    {
      "value": "20,5",
      "unit": "%",
      "label": "Gewinnmarge"
    }
  ]
}
```

### Beispiel-HTML

```html
<h2>Geschäftsergebnisse 2024</h2>
<p>Alle Zahlen in EUR</p>
<div class="stat-grid">
  <div class="stat-card">
    <span class="stat-number">€42,5<span class="unit">Mio</span></span>
    <span class="stat-label">Gesamtumsatz (Jahresbericht 2024)</span>
  </div>
  <div class="stat-card">
    <span class="stat-number">+18<span class="unit">%</span></span>
    <span class="stat-label">Wachstum YoY</span>
  </div>
  <!-- weitere Karten ... -->
</div>
```

---

## 2. Bullet-List

**Type:** `bullet-list`

Zeigt Aufzählungen und Listen mit Bullet-Punkten.

### Verwendung

Ideal für:
- **Features-Listen** (Unsere Features: ...)
- **Aufzählungen** (Schritte, Punkte)
- **Best-Practices** (Top 5 Tipps)
- **Anforderungen** (Must-Haves, Nice-to-Haves)

### Slots

```
{
  "type": "bullet-list",
  "title": "string (optional)",
  "subtitle": "string (optional)",
  "bullets": [
    "string"
  ]
}
```

### Slot-Details

**title**: Überschrift
```
"Unsere Kernkompetenzen"
```

**subtitle**: Zusätzliche Erklärung
```
"Das zeichnet uns aus"
```

**bullets**: Array von Bullet-Points (Strings)
```
[
  "Cloud-Native Architektur",
  "Machine Learning Integration",
  "99.99% Verfügbarkeit",
  "Enterprise-Grade Sicherheit"
]
```

### CSS-Klassen

```css
.bullet-list {
  list-style: disc;
  margin-left: 20px;
  line-height: 1.8;
}

.bullet-list li {
  margin-bottom: 12px;
  font-size: 15px;
  color: var(--text-color);
}

.bullet-list li::marker {
  color: var(--primary-color);
  font-weight: 600;
}
```

### Beispiel-JSON

```json
{
  "type": "bullet-list",
  "title": "Unsere Kernkompetenzen",
  "subtitle": "Das zeichnet uns aus",
  "bullets": [
    "Cloud-Native Architektur",
    "Machine Learning Integration",
    "99.99% Verfügbarkeit",
    "Enterprise-Grade Sicherheit",
    "24/7 Support",
    "ISO 27001 zertifiziert"
  ]
}
```

### Beispiel-HTML

```html
<h2>Unsere Kernkompetenzen</h2>
<p>Das zeichnet uns aus</p>
<ul class="bullet-list">
  <li>Cloud-Native Architektur</li>
  <li>Machine Learning Integration</li>
  <li>99.99% Verfügbarkeit</li>
  <li>Enterprise-Grade Sicherheit</li>
  <li>24/7 Support</li>
  <li>ISO 27001 zertifiziert</li>
</ul>
```

---

## 3. Quote

**Type:** `quote`

Zeigt Zitate oder Testimonials mit optionalem Author.

### Verwendung

Ideal für:
- **Zitate** (Kundenmeinungen, Expert-Quotes)
- **Testimonials** (Erfolgsstories)
- **Motivational Statements** (Vision, Mission)
- **Callout-Boxen** (Wichtige Aussagen)

### Slots

```
{
  "type": "quote",
  "quote_text": "string (required)",
  "quote_author": "string (optional)"
}
```

### Slot-Details

**quote_text**: Das Zitat (ohne Anführungszeichen)
```
"Die beste Technologie ist unsichtbar"
```

**quote_author**: Autor oder Quelle (optional)
```
"Steve Jobs" oder "CEO von Apple"
```

### CSS-Klassen

```css
blockquote {
  border-left: 4px solid var(--primary-color);
  padding-left: 20px;
  margin: 20px 0;
  font-size: 18px;
  font-style: italic;
  color: var(--text-color);
  line-height: 1.6;
}

blockquote::before {
  content: '"';
  font-size: 32px;
  color: var(--primary-color);
  margin-right: 8px;
}

.quote-author {
  font-size: 13px;
  font-style: normal;
  color: var(--text-secondary);
  margin-top: 12px;
  padding-left: 20px;
}
```

### Beispiel-JSON

```json
{
  "type": "quote",
  "quote_text": "Innovation unterscheidet zwischen Führerschaft und Nachfolgern",
  "quote_author": "Steve Jobs, Apple"
}
```

### Beispiel-HTML

```html
<blockquote>
  "Innovation unterscheidet zwischen Führerschaft und Nachfolgern"
</blockquote>
<div class="quote-author">— Steve Jobs, Apple</div>
```

---

## 4. Text

**Type:** `text`

Zeigt Fließtext und Paragraphen mit optionaler Überschrift.

### Verwendung

Ideal für:
- **Narrative Inhalte** (Geschichten, Erklärungen)
- **Beschreibungen** (Was tun wir, warum)
- **Hintergrund-Infos** (Context, Details)
- **Multi-Paragraph Inhalte** (Artikel, Blog-Posts)

### Slots

```
{
  "type": "text",
  "title": "string (optional)",
  "subtitle": "string (optional)",
  "paragraphs": [
    "string"
  ]
}
```

### Slot-Details

**title**: Überschrift
```
"Unsere Vision"
```

**subtitle**: Zusätzliche Erklärung
```
"Wo wir hin wollen"
```

**paragraphs**: Array von Paragraphen (Strings)
```
[
  "Wir bauen die zukunftssichere Lösung für digitale Transformation.",
  "Unser Fokus liegt auf Skalierbarkeit, Sicherheit und Developer Experience.",
  "Über 10.000 Unternehmen vertrauen uns bereits."
]
```

### CSS-Klassen

```css
.text-component {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-color);
}

.text-component p {
  margin-bottom: 16px;
}

.text-component p:last-child {
  margin-bottom: 0;
}

.text-component strong {
  color: var(--text-color);
  font-weight: 600;
}

.text-component em {
  color: var(--text-secondary);
  font-style: italic;
}
```

### Beispiel-JSON

```json
{
  "type": "text",
  "title": "Unsere Vision",
  "subtitle": "Wo wir hin wollen",
  "paragraphs": [
    "Wir bauen die zukunftssichere Lösung für digitale Transformation.",
    "Unser Fokus liegt auf Skalierbarkeit, Sicherheit und Developer Experience.",
    "Über 10.000 Unternehmen vertrauen uns bereits."
  ]
}
```

### Beispiel-HTML

```html
<h2>Unsere Vision</h2>
<p>Wo wir hin wollen</p>
<div class="text-component">
  <p>Wir bauen die zukunftssichere Lösung für digitale Transformation.</p>
  <p>Unser Fokus liegt auf Skalierbarkeit, Sicherheit und Developer Experience.</p>
  <p>Über 10.000 Unternehmen vertrauen uns bereits.</p>
</div>
```

---

## 5. Table

**Type:** `table`

Zeigt tabellarische Daten in strukturiertem Format.

### Verwendung

Ideal für:
- **Vergleiche** (Produkt A vs. B)
- **Daten-Ansicht** (Tabellen aus Excel)
- **Übersichten** (Features-Matrix, Preislisten)
- **Zeitreihen** (Monatliche/Jährliche Daten)

### Slots

```
{
  "type": "table",
  "title": "string (optional)",
  "headers": ["string"],
  "rows": [
    ["string"]
  ]
}
```

### Slot-Details

**title**: Überschrift
```
"Leistungs-Vergleich"
```

**headers**: Spalten-Header (Array von Strings)
```
["Feature", "Starter", "Pro", "Enterprise"]
```

**rows**: Zeilen-Daten (Array von Arrays)
```
[
  ["API Access", "Nein", "Ja", "Ja"],
  ["Custom Domain", "Nein", "Ja", "Ja"],
  ["Priority Support", "Nein", "Nein", "Ja"]
]
```

### CSS-Klassen

```css
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

thead {
  background: var(--component-bg);
  border-bottom: 2px solid var(--primary-color);
}

th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: var(--text-color);
}

td {
  padding: 12px;
  border-bottom: 1px solid var(--border-color);
}

tbody tr:hover {
  background: var(--hover-bg);
}
```

### Beispiel-JSON

```json
{
  "type": "table",
  "title": "Leistungs-Vergleich",
  "headers": ["Feature", "Starter", "Pro", "Enterprise"],
  "rows": [
    ["API Access", "Nein", "Ja", "Ja"],
    ["Custom Domain", "Nein", "Ja", "Ja"],
    ["Priority Support", "Nein", "Nein", "Ja"],
    ["SLA Guarantee", "99%", "99.9%", "99.99%"]
  ]
}
```

### Beispiel-HTML

```html
<h2>Leistungs-Vergleich</h2>
<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Starter</th>
      <th>Pro</th>
      <th>Enterprise</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>API Access</td>
      <td>Nein</td>
      <td>Ja</td>
      <td>Ja</td>
    </tr>
    <!-- weitere Zeilen ... -->
  </tbody>
</table>
```

---

## 6. Image-Frame

**Type:** `image-frame`

Zeigt ein einzelnes Bild mit optionaler Caption.

### Verwendung

Ideal für:
- **Einzelne Bilder** (Produkt-Foto, Screenshot)
- **Illustrationen** (Diagramme, Grafiken)
- **Team-Fotos** (Mit Beschreibung)
- **Artwork** (Mit Quellenangabe)

### Slots

```
{
  "type": "image-frame",
  "title": "string (optional)",
  "image_path": "string (required)",
  "image_alt_text": "string (optional)",
  "image_caption": "string (optional)"
}
```

### Slot-Details

**title**: Überschrift der Komponente
```
"Unser Produkt"
```

**image_path**: Pfad zum Bild (relativ zu project)
```
"images/uploads/product-screenshot.png"
```

**image_alt_text**: Alt-Text für Accessibility
```
"Screenshot der Dashboard-Ansicht"
```

**image_caption**: Caption unter dem Bild
```
"Dashboard mit Real-Time Analytics"
```

### CSS-Klassen

```css
.image-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.image-wrapper {
  width: 100%;
  max-width: 600px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
  background: var(--component-bg);
}

.image-wrapper img {
  width: 100%;
  height: auto;
  display: block;
}

.image-content {
  font-size: 13px;
  color: var(--text-secondary);
  font-style: italic;
}
```

### Beispiel-JSON

```json
{
  "type": "image-frame",
  "title": "Unser Produkt in Aktion",
  "image_path": "images/uploads/dashboard.png",
  "image_alt_text": "Dashboard-Screenshot",
  "image_caption": "Real-Time Analytics Dashboard mit KPI-Überblick"
}
```

### Beispiel-HTML

```html
<h2>Unser Produkt in Aktion</h2>
<div class="image-container">
  <div class="image-wrapper">
    <img src="images/uploads/dashboard.png"
         alt="Dashboard-Screenshot" />
  </div>
  <div class="image-content">
    Real-Time Analytics Dashboard mit KPI-Überblick
  </div>
</div>
```

---

## 7. Image-Grid

**Type:** `image-grid`

Zeigt mehrere Bilder in einem Grid-Layout.

### Verwendung

Ideal für:
- **Galerie** (Produkt-Variations, Portfolio)
- **Multiple Screenshots** (Feature-Showcase)
- **Team-Fotos** (Mehrere Personen)
- **Case Studies** (Vorher/Nachher Grid)

### Slots

```
{
  "type": "image-grid",
  "title": "string (optional)",
  "images": [
    {
      "path": "string (required)",
      "alt": "string (optional)",
      "caption": "string (optional)"
    }
  ]
}
```

### Slot-Details

**title**: Überschrift der Galerie
```
"Unsere Lösungen"
```

**images**: Array von Bild-Objekten

**path**: Pfad zum Bild
```
"images/uploads/solution-1.png"
```

**alt**: Alt-Text
```
"E-Commerce Lösung"
```

**caption**: Caption unter jedem Bild
```
"Online-Shop mit 50+ Templates"
```

### CSS-Klassen

```css
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.image-grid-item {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
  background: var(--component-bg);
}

.image-grid-item img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  display: block;
}

.image-grid-caption {
  padding: 12px;
  font-size: 13px;
  color: var(--text-secondary);
  text-align: center;
}
```

### Beispiel-JSON

```json
{
  "type": "image-grid",
  "title": "Unsere Lösungen",
  "images": [
    {
      "path": "images/uploads/ecommerce.png",
      "alt": "E-Commerce Lösung",
      "caption": "Online-Shop"
    },
    {
      "path": "images/uploads/crm.png",
      "alt": "CRM System",
      "caption": "Customer Management"
    },
    {
      "path": "images/uploads/analytics.png",
      "alt": "Analytics Platform",
      "caption": "Daten-Analyse"
    }
  ]
}
```

---

## 8. Feature-Grid

**Type:** `feature-grid`

Zeigt Features oder Vorteile mit Icons und Beschreibungen.

### Verwendung

Ideal für:
- **Feature-Listen** (Mit Icons)
- **Benefits** (Warum wir besser sind)
- **Highlights** (Top 3-4 Punkte)
- **Differentiators** (Was uns unterscheidet)

### Slots

```
{
  "type": "feature-grid",
  "title": "string (optional)",
  "features": [
    {
      "icon": "string (emoji/icon)",
      "title": "string (required)",
      "description": "string (required)"
    }
  ]
}
```

### Slot-Details

**title**: Überschrift
```
"Unsere Stärken"
```

**features**: Array von Features

**icon**: Emoji oder Icon (1-2 Zeichen)
```
"⚡", "🔒", "🚀", "💡"
```

**title**: Feature-Name
```
"Blazing Fast"
```

**description**: Kurze Beschreibung
```
"Sub-100ms Latency für alle Operationen"
```

### CSS-Klassen

```css
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.feature-item {
  text-align: center;
}

.feature-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.feature-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-color);
}

.feature-description {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}
```

### Beispiel-JSON

```json
{
  "type": "feature-grid",
  "title": "Unsere Stärken",
  "features": [
    {
      "icon": "⚡",
      "title": "Blazing Fast",
      "description": "Sub-100ms Latency für alle Operationen"
    },
    {
      "icon": "🔒",
      "title": "Enterprise Security",
      "description": "ISO 27001 zertifiziert, End-to-End Verschlüsselung"
    },
    {
      "icon": "📈",
      "title": "Skalierbar",
      "description": "Von 1 bis 1 Million Transaktionen pro Sekunde"
    },
    {
      "icon": "🌍",
      "title": "Global",
      "description": "Verfügbar in 50+ Ländern, mehrsprachig"
    }
  ]
}
```

---

## 9. Process

**Type:** `process`

Zeigt Prozess-Schritte in vertikaler Timeline.

### Verwendung

Ideal für:
- **Workflows** (Schritt 1, 2, 3)
- **Timelines** (Phasen, Meilensteine)
- **Customer Journey** (Awareness → Conversion)
- **Entwicklungs-Phasen** (Requirements → Launch)

### Slots

```
{
  "type": "process",
  "title": "string (optional)",
  "steps": [
    {
      "number": "string|integer",
      "title": "string (required)",
      "description": "string (optional)",
      "timeframe": "string (optional)"
    }
  ]
}
```

### Slot-Details

**title**: Überschrift des Prozesses
```
"Unser Projektmanagement"
```

**steps**: Array von Schritt-Objekten

**number**: Schritt-Nummer (1, 2, 3 oder I, II, III)
```
"1" oder "Phase 1" oder "Discovery"
```

**title**: Schritt-Titel
```
"Discovery"
```

**description**: Detaillierte Beschreibung
```
"Anforderungsaufnahme, Stakeholder-Interviews, Risikoanalyse"
```

**timeframe**: Zeitrahmen (optional)
```
"Woche 1-2"
```

### CSS-Klassen

```css
.process-timeline {
  position: relative;
  padding: 20px 0;
}

.process-step {
  display: flex;
  margin-bottom: 30px;
  position: relative;
  padding-left: 60px;
}

.process-step::before {
  content: attr(data-number);
  position: absolute;
  left: 0;
  top: 0;
  width: 40px;
  height: 40px;
  background: var(--primary-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 16px;
}

.process-step::after {
  content: '';
  position: absolute;
  left: 19px;
  top: 40px;
  width: 2px;
  height: 30px;
  background: var(--border-color);
}

.process-step:last-child::after {
  display: none;
}

.process-content {
  flex: 1;
}

.process-title {
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 4px;
}

.process-description {
  font-size: 13px;
  color: var(--text-secondary);
}
```

### Beispiel-JSON

```json
{
  "type": "process",
  "title": "Unser Projektmanagement",
  "steps": [
    {
      "number": "1",
      "title": "Discovery",
      "description": "Anforderungsaufnahme, Stakeholder-Interviews, Risikoanalyse",
      "timeframe": "Woche 1-2"
    },
    {
      "number": "2",
      "title": "Design",
      "description": "Wireframes, Prototypen, Design-Reviews",
      "timeframe": "Woche 3-4"
    },
    {
      "number": "3",
      "title": "Entwicklung",
      "description": "Agile Sprints, Daily Standups, Continuous Testing",
      "timeframe": "Woche 5-10"
    },
    {
      "number": "4",
      "title": "Launch",
      "description": "Performance-Tests, Security-Audit, Go-Live",
      "timeframe": "Woche 11"
    }
  ]
}
```

---

## 10. Process-Horizontal

**Type:** `process-horizontal`

Zeigt Prozess-Schritte in horizontaler Timeline.

### Verwendung

Ideal für:
- **Kurze Prozesse** (3-4 Schritte)
- **Horizontale Timelines** (Geldfluss, Datenfluss)
- **Kunden-Reise** (Click → View → Buy → Review)
- **Zahlungs-Prozess** (Warenkob → Checkout → Zahlung → Bestätigung)

### Slots

```
{
  "type": "process-horizontal",
  "title": "string (optional)",
  "steps": [
    {
      "title": "string (required)",
      "description": "string (optional)"
    }
  ]
}
```

### Slot-Details

**title**: Überschrift
```
"Kunden-Reise"
```

**steps**: Array von Schritten (max. 5)

**title**: Schritt-Titel
```
"Awareness"
```

**description**: Kurze Beschreibung
```
"Kunde entdeckt unser Produkt"
```

### CSS-Klassen

```css
.process-horizontal {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-top: 20px;
}

.process-h-step {
  flex: 1;
  text-align: center;
  position: relative;
}

.process-h-step::before {
  content: '';
  position: absolute;
  top: 20px;
  left: -10px;
  width: calc(100% + 20px);
  height: 2px;
  background: var(--border-color);
  z-index: 0;
}

.process-h-step:first-child::before {
  left: 50%;
  width: 50%;
}

.process-h-step:last-child::before {
  right: 50%;
  width: 50%;
}

.process-h-number {
  width: 40px;
  height: 40px;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin: 0 auto 12px;
  position: relative;
  z-index: 1;
}

.process-h-title {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 4px;
}

.process-h-description {
  font-size: 12px;
  color: var(--text-secondary);
}
```

### Beispiel-JSON

```json
{
  "type": "process-horizontal",
  "title": "Kunden-Reise",
  "steps": [
    {
      "title": "Awareness",
      "description": "Kunde entdeckt unser Produkt"
    },
    {
      "title": "Consideration",
      "description": "Vergleicht mit Alternativen"
    },
    {
      "title": "Decision",
      "description": "Trifft Kaufentscheidung"
    },
    {
      "title": "Retention",
      "description": "Langfristige Bindung"
    }
  ]
}
```

---

## Komponenten-Kombinationen

### Single-Component Slides
- Statistik-heavy: 1x `stat-grid`
- Feature-heavy: 1x `feature-grid` oder 2x `bullet-list`
- Story-based: 1x `text` mit mehreren Paragraphen

### Zwei-Komponenten Slides
- Oben: Title + `stat-grid`
- Unten: `bullet-list` oder `text`

Beispiel:
```json
[
  {
    "type": "stat-grid",
    "stats": [...]
  },
  {
    "type": "bullet-list",
    "title": "Treiber für Wachstum",
    "bullets": [...]
  }
]
```

### Drei-Komponenten Slides (Maximales Layout)
- Oben: Title (auto-gen)
- Mitte: Hauptkomponente (`stat-grid`, `text`, `quote`)
- Unten: Unterstützende Komponente (`bullet-list`, `image-frame`)

**Best Practice:** Halte Slides fokussiert. Zu viele Komponenten überlasten den Viewer.

---

## Design-System Integration

Alle Komponenten respektieren das Theme-System:

```css
:root {
  /* Farben */
  --primary-color: #238636;        /* GitHub Green */
  --text-color: #c9d1d9;
  --text-secondary: #8b949e;
  --component-bg: #0d1117;
  --border-color: #30363d;

  /* Spacing */
  --spacing-unit: 8px;

  /* Typografie */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-size-base: 15px;
  --line-height: 1.6;

  /* Border Radius */
  --border-radius: 6px;
}
```

Für andere Themes (apple, openai, modern, minimal) werden diese Variablen überschrieben.

---

## Best Practices

1. **Fokus halten** - Max. 1-2 primäre Komponenten pro Slide
2. **Visuelle Hierarchie** - Titel → Primäre Komponente → Sekundär
3. **Weiße Fläche** - Nutze Spacing großzügig
4. **Konsistenz** - Nutze gleiche Component-Types für ähnliche Inhalte
5. **Barrierefreiheit** - Verwende `alt`-Text für Bilder, aussagekräftige Labels
6. **Mobile-First** - Components sind responsive, aber für Präsentationen meist Desktop

---

## Verwandte Dokumentation

- **[Erste Folie Tutorial](../guides/first-slide-tutorial.md)** - Praktische Beispiele
- **[API Endpoints](endpoints.md)** - Wie Komponenten generiert werden
- **[System-Architektur](architecture.md)** - Wie Templates rendern
- **[Theme Creation](../guides/theme-creation/)** - Custom Komponenten stylen

---

**Version:** 2.0
**Zuletzt aktualisiert:** 2025-11-20
**Components:** 10

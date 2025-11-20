# Theme Creation - Vollständiges Tutorial

**Erstelle dein eigenes Design-Theme in 30 Minuten.**

Dieses Tutorial führt dich Schritt-für-Schritt durch die Erstellung eines komplett neuen Themes mit Erklärungen zu jedem Schritt.

---

## 🎯 Was du lernst

- Design-Tokens definieren (Farben, Typography, Spacing)
- CSS-Variablen strukturieren
- Alle 10 Component-Types stylen
- Theme registrieren und testen
- Accessibility sicherstellen

---

## 📋 Voraussetzungen

- Slide Assistant läuft lokal
- Grundkenntnisse in CSS
- Text-Editor deiner Wahl

**Zeit**: ~30 Minuten

---

## Teil 1: Konzept & Planung (5 min)

### Schritt 1: Design-Richtung festlegen

Bevor du Code schreibst, definiere dein Theme-Konzept:

**Beispiel-Theme: "Nordic Minimal"**
- **Style**: Minimalistisch, skandinavisch
- **Farben**: Hellblau, Weiß, Grau
- **Typography**: Clean Sans-Serif
- **Border-Radius**: Groß (12-16px) für weiche Ecken
- **Shadows**: Sehr subtil

### Schritt 2: Farb-Palette erstellen

Nutze [Coolors.co](https://coolors.co/) oder [Adobe Color](https://color.adobe.com/):

**Nordic Minimal Palette:**
```
Primary:    #5E9BD1  (Soft Blue)
Secondary:  #7AA5CC  (Light Blue)
Background: #F8F9FA  (Off-White)
Text:       #2C3E50  (Dark Blue-Gray)
Accent:     #95B8D1  (Very Light Blue)
```

### Schritt 3: Kontrast prüfen

**WICHTIG**: Accessibility first!

Teste mit [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/):

- Text (#2C3E50) auf Background (#F8F9FA): **10.9:1** ✅ (AAA)
- Primary (#5E9BD1) auf White: **2.8:1** ⚠️ (zu niedrig)
  → Lösung: Dunkleres Blau für Text auf Weiß: #3A7BB8

---

## Teil 2: Struktur erstellen (5 min)

### Schritt 4: Theme-Verzeichnis anlegen

```bash
cd presentation/shared-themes
mkdir nordic-minimal
cd nordic-minimal
```

**Warum shared-themes/?**
- Global verfügbar für alle Projekte
- Einfacher zu teilen
- Fallback-System (project → shared → default)

**Alternative**: Project-specific Theme
```bash
cd presentation/projects/mein-projekt/styles
mkdir nordic-minimal
```

### Schritt 5: Dateien erstellen

```bash
touch design-guide.json
touch design-guide.md
touch variables.css
touch style.css
```

**Datei-Struktur:**
```
nordic-minimal/
├── design-guide.json    # Strukturierte Design-Definition
├── design-guide.md      # Human-readable Dokumentation
├── variables.css        # CSS Custom Properties
└── style.css           # Component-Styles
```

---

## Teil 3: Design-Guide definieren (10 min)

### Schritt 6: design-guide.json erstellen

**Was ist design-guide.json?**
- Zentrale Quelle der Wahrheit für dein Theme
- Wird von Agents gelesen
- Definiert alle Tokens & Components

**Vollständiges Beispiel:**

```json
{
  "theme": "nordic-minimal",
  "name": "Nordic Minimal Design",
  "description": "Minimalistisches skandinavisches Design mit weichen Farben",
  "version": "1.0.0",

  "tokens": {
    "colors": {
      "primary": {
        "main": "#5E9BD1",
        "light": "#95B8D1",
        "dark": "#3A7BB8",
        "name": "Soft Blue",
        "usage": "Primary accent, highlights, CTAs"
      },
      "background": {
        "main": "#F8F9FA",
        "subtle": "#E9ECEF",
        "component": "#FFFFFF",
        "overlay": "#F1F3F5"
      },
      "text": {
        "primary": "#2C3E50",
        "secondary": "#6C757D",
        "muted": "#ADB5BD",
        "onPrimary": "#FFFFFF"
      },
      "border": {
        "main": "#DEE2E6",
        "muted": "#E9ECEF",
        "hover": "#5E9BD1"
      },
      "semantic": {
        "success": {
          "bg": "#D4EDDA",
          "text": "#155724",
          "border": "#28A745"
        },
        "warning": {
          "bg": "#FFF3CD",
          "text": "#856404",
          "border": "#FFC107"
        },
        "danger": {
          "bg": "#F8D7DA",
          "text": "#721C24",
          "border": "#DC3545"
        }
      }
    },

    "typography": {
      "fontFamily": {
        "default": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
      },
      "fontWeights": {
        "light": 300,
        "normal": 400,
        "semibold": 600,
        "bold": 700
      },
      "headings": {
        "h1": {"fontSize": "52px", "fontWeight": 700, "lineHeight": 1.2},
        "h2": {"fontSize": "36px", "fontWeight": 600, "lineHeight": 1.3}
      },
      "body": {
        "fontSize": "17px",
        "fontWeight": 400,
        "lineHeight": 1.6
      }
    },

    "spacing": {
      "xs": "4px",
      "sm": "8px",
      "md": "16px",
      "lg": "24px",
      "xl": "32px",
      "2xl": "48px",
      "3xl": "64px"
    },

    "borderRadius": {
      "sm": "8px",
      "md": "12px",
      "lg": "16px",
      "full": "9999px"
    },

    "shadows": {
      "sm": "0 1px 2px rgba(0,0,0,0.05)",
      "md": "0 4px 6px rgba(0,0,0,0.07)",
      "lg": "0 10px 15px rgba(0,0,0,0.1)"
    }
  },

  "components": [
    {
      "id": "stat-grid",
      "name": "Statistic Grid",
      "description": "Display statistics in grid layout",
      "gridColumns": "repeat(auto-fit, minmax(200px, 1fr))"
    },
    {
      "id": "bullet-list",
      "name": "Bullet List",
      "description": "Formatted bullet points"
    },
    {
      "id": "quote",
      "name": "Quote",
      "description": "Highlighted quote or testimonial"
    },
    {
      "id": "text",
      "name": "Text",
      "description": "Paragraphs with formatting"
    },
    {
      "id": "table",
      "name": "Table",
      "description": "Structured data table"
    },
    {
      "id": "image-frame",
      "name": "Image Frame",
      "description": "Single image with caption"
    },
    {
      "id": "image-grid",
      "name": "Image Grid",
      "description": "Multiple images in grid"
    },
    {
      "id": "feature-grid",
      "name": "Feature Grid",
      "description": "Features with icons and descriptions"
    },
    {
      "id": "process",
      "name": "Process Steps",
      "description": "Sequential steps (vertical)"
    },
    {
      "id": "process-horizontal",
      "name": "Process Horizontal",
      "description": "Sequential workflow (horizontal)"
    }
  ]
}
```

**Erklärung der Sections:**

- **tokens.colors**: Farb-Palette mit semantic naming
- **tokens.typography**: Schriftarten, Größen, Gewichte
- **tokens.spacing**: Konsistente Abstände (4px-Raster)
- **tokens.borderRadius**: Ecken-Rundung
- **tokens.shadows**: Schatten-Definitionen
- **components**: Alle 10 Component-Types registrieren

---

## Teil 4: CSS Variables definieren (5 min)

### Schritt 7: variables.css erstellen

**Warum CSS Variables?**
- Zentrale Wartung
- Einfaches Überschreiben
- Browser-native Unterstützung

**Vollständiges Beispiel:**

```css
/* Nordic Minimal - CSS Variablen */

:root {
  /* === FARBEN === */

  /* Primary */
  --color-primary: #5E9BD1;
  --color-primary-light: #95B8D1;
  --color-primary-dark: #3A7BB8;

  /* Background */
  --color-bg-main: #F8F9FA;
  --color-bg-subtle: #E9ECEF;
  --color-bg-component: #FFFFFF;
  --color-bg-overlay: #F1F3F5;

  /* Text */
  --color-text-primary: #2C3E50;
  --color-text-secondary: #6C757D;
  --color-text-muted: #ADB5BD;
  --color-text-on-primary: #FFFFFF;

  /* Border */
  --color-border: #DEE2E6;
  --color-border-muted: #E9ECEF;
  --color-border-hover: #5E9BD1;

  /* Semantic */
  --color-success: #28A745;
  --color-success-bg: #D4EDDA;
  --color-warning: #FFC107;
  --color-warning-bg: #FFF3CD;
  --color-danger: #DC3545;
  --color-danger-bg: #F8D7DA;

  /* === TYPOGRAPHY === */

  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --font-size-body: 17px;
  --line-height-body: 1.6;

  --font-size-h1: 52px;
  --font-size-h2: 36px;

  /* === SPACING === */

  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  --spacing-3xl: 64px;

  /* === BORDER RADIUS === */

  --border-radius-sm: 8px;
  --border-radius-md: 12px;
  --border-radius-lg: 16px;
  --border-radius-full: 9999px;

  /* === SHADOWS === */

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);

  /* === KOMPONENTEN === */

  --component-padding: 48px;
  --component-border-width: 1px;
  --component-border-radius: var(--border-radius-md);
  --component-shadow: var(--shadow-sm);
}
```

**Best Practices:**
- Verwende semantic naming (`--color-text-primary`, nicht `--color-gray-900`)
- Gruppiere zusammenhängende Werte
- Kommentiere Sections
- Vermeide Magic Numbers - nutze Tokens aus design-guide.json

---

## Teil 5: Component-Styles erstellen (10 min)

### Schritt 8: style.css erstellen

**Basis-Struktur:**

```css
/* Nordic Minimal - Component Styles */

@import url('variables.css');

/* === GLOBAL STYLES === */

body {
  font-family: var(--font-family);
  font-size: var(--font-size-body);
  line-height: var(--line-height-body);
  color: var(--color-text-primary);
  background: var(--color-bg-main);
}

/* === COMPONENT BASE === */

.component {
  background: var(--color-bg-component);
  border: var(--component-border-width) solid var(--color-border);
  border-radius: var(--component-border-radius);
  padding: var(--component-padding);
  box-shadow: var(--component-shadow);
  margin-bottom: var(--spacing-xl);
}

/* === 1. STAT-GRID === */

.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
  padding: var(--spacing-2xl);
}

.stat-card {
  text-align: center;
  padding: var(--spacing-xl);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-md);
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-value {
  font-size: 48px;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  line-height: 1.2;
  margin-bottom: var(--spacing-sm);
}

.stat-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* === 2. BULLET-LIST === */

.bullet-list {
  padding: var(--spacing-2xl);
}

.bullet-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.bullet-list li {
  position: relative;
  padding-left: var(--spacing-xl);
  margin-bottom: var(--spacing-md);
  font-size: 18px;
  line-height: 1.6;
}

.bullet-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--color-primary);
  font-size: 24px;
  font-weight: bold;
}

/* === 3. QUOTE === */

.quote {
  padding: var(--spacing-3xl);
  background: linear-gradient(135deg, var(--color-bg-subtle) 0%, var(--color-bg-component) 100%);
  border-left: 4px solid var(--color-primary);
}

.quote-text {
  font-size: 24px;
  font-style: italic;
  color: var(--color-text-primary);
  line-height: 1.6;
  margin-bottom: var(--spacing-lg);
}

.quote-author {
  font-size: 16px;
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-semibold);
}

/* === 4. TEXT === */

.text {
  padding: var(--spacing-2xl);
}

.text p {
  font-size: 18px;
  line-height: 1.7;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.text h2 {
  font-size: var(--font-size-h2);
  font-weight: var(--font-weight-semibold);
  color: var(--color-primary);
  margin-bottom: var(--spacing-lg);
}

/* === 5. TABLE === */

.table-component {
  padding: var(--spacing-2xl);
  overflow-x: auto;
}

.table-component table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.table-component th {
  background: var(--color-primary);
  color: var(--color-text-on-primary);
  padding: var(--spacing-md);
  text-align: left;
  font-weight: var(--font-weight-semibold);
  border-radius: var(--border-radius-sm) var(--border-radius-sm) 0 0;
}

.table-component td {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
}

.table-component tr:hover {
  background: var(--color-bg-subtle);
}

/* === 6-10: Weitere Components ... === */

/* Kopiere die restlichen Component-Styles von einem Referenz-Theme
   Siehe: shared-themes/apple/style.css oder shared-themes/openai/style.css */
```

**Tipp**: Kopiere die restlichen Component-Styles (image-frame, image-grid, feature-grid, process, process-horizontal) von einem existierenden Theme und passe nur Farben/Spacing an.

---

## Teil 6: Registrierung & Testing (5 min)

### Schritt 9: Theme registrieren

**Datei**: `presentation/projects.json`

```json
{
  "defaultStyle": "github",
  "sharedThemes": [
    {
      "name": "github",
      "displayName": "GitHub Design",
      "cssPath": "shared-themes/github/style.css",
      "default": true
    },
    {
      "name": "nordic-minimal",
      "displayName": "Nordic Minimal",
      "cssPath": "shared-themes/nordic-minimal/style.css",
      "default": false
    }
  ],
  "projects": [...]
}
```

### Schritt 10: Testen

**1. Server starten:**
```bash
cd presentation
python3 run_api.py
```

**2. Frontend öffnen:**
```bash
open unified-editor.html
# oder: http://localhost:8000/unified-editor.html
```

**3. Theme auswählen:**
- Project: "beispiel-projekt"
- Theme: "Nordic Minimal" (unter "Shared Themes")

**4. Test-Folie generieren:**
```
User Input: "Unser Team: 5 Experten, 20 Jahre Erfahrung, 3 Standorte"
Slide Title: "Team"
Model: GPT-4o
```

**5. Visuell prüfen:**
- Farben korrekt?
- Spacing harmonisch?
- Kontraste lesbar?
- Components gut proportioniert?

---

## Validierung & Quality Check

### Accessibility Checklist

- [ ] **Kontrast-Ratios** (WebAIM Checker):
  - Text/Background: ≥4.5:1 (WCAG AA)
  - Primary/White: ≥3:1
- [ ] **Fokus-Indikatoren** sichtbar
- [ ] **Semantic Colors** haben ausreichenden Kontrast

### Technical Checklist

- [ ] Alle 10 Component-Types haben CSS-Styles
- [ ] CSS-Variablen matchen design-guide.json
- [ ] Keine hard-coded Farben (nur CSS-Variablen)
- [ ] `@import url('variables.css');` in style.css
- [ ] projects.json Syntax korrekt

### Browser Compatibility

- [ ] Chrome/Edge getestet
- [ ] Firefox getestet
- [ ] Safari getestet (falls macOS)

---

## Next Steps

**✅ Geschafft!** Du hast dein erstes Theme erstellt.

**Weitere Schritte:**

1. **Dokumentieren**: Erstelle `design-guide.md`
2. **Screenshots**: Erstelle `reference.html` mit Beispielen
3. **Teilen**: Push to GitHub, PR erstellen
4. **Verfeinern**: Feedback sammeln, iterieren

**Weiterführende Guides:**
- [Apple Theme Walkthrough](apple-walkthrough.md) - Real-World Beispiel
- [Tools & Resources](tools.md) - Design-Tools
- [Troubleshooting](troubleshooting.md) - Häufige Probleme

---

## 💡 Tipps

**Schneller Start:**
```bash
# Kopiere ein existierendes Theme als Basis
cp -r shared-themes/apple shared-themes/my-theme

# Passe nur Farben & Fonts an
# Ändere: design-guide.json, variables.css
```

**Design-Entscheidungen:**
- **Minimalistisch**: Kleine border-radius (4-8px), subtile Schatten
- **Modern**: Mittlere border-radius (8-12px), weiche Schatten
- **Verspielt**: Große border-radius (12-16px), mehrschichtige Schatten

**Font-Pairing:**
- Sans-Serif + Sans-Serif: Inter + Roboto
- Serif + Sans-Serif: Merriweather + Open Sans
- System-Fonts: `-apple-system, BlinkMacSystemFont, 'Segoe UI'`

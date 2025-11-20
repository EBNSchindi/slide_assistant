# Theme Creation Guide

Anleitung zur Erstellung neuer Design-Themes für den Slide Assistant.

## Übersicht

Das System unterstützt zwei Arten von Themes:
1. **Project-Specific Themes**: Themes die nur für ein bestimmtes Projekt verfügbar sind
2. **Shared Themes**: Global verfügbare Themes für alle Projekte (empfohlen für Produktiv-Designs)

## Shared Themes (Empfohlen)

Shared Themes befinden sich in `presentation/shared-themes/` und sind automatisch für alle Projekte verfügbar.

### Schritt 1: Theme-Verzeichnis erstellen

```bash
cd presentation/shared-themes
mkdir my-theme
cd my-theme
```

### Schritt 2: design-guide.json erstellen

Die `design-guide.json` ist die zentrale Konfigurationsdatei für dein Theme. Sie definiert:
- Farben (Primary, Background, Text, Semantic)
- Typografie (Fonts, Sizes, Weights)
- Spacing-Scale
- Border Radius
- Shadows
- Component-Definitionen (alle 10 Component-Typen)

**Template:**
```json
{
  "theme": "my-theme",
  "name": "My Theme Name",
  "description": "Theme description",
  "version": "1.0.0",

  "tokens": {
    "colors": {
      "primary": {
        "main": "#0071E3",
        "light": "#4DA3FF",
        "dark": "#0051B3",
        "name": "Primary Color",
        "usage": "Primary accent for highlights"
      },
      "background": {
        "main": "#ffffff",
        "subtle": "#f5f5f7",
        "component": "#ffffff",
        "overlay": "#fafafa"
      },
      "text": {
        "primary": "#1d1d1d",
        "secondary": "#555555",
        "muted": "#888888",
        "onPrimary": "#ffffff"
      },
      "border": {
        "main": "#e5e5e7",
        "muted": "#f0f0f2",
        "hover": "#0071E3"
      },
      "semantic": {
        "success": {
          "bg": "#D1F1D1",
          "text": "#0A6F08",
          "border": "#34C759"
        },
        "warning": {
          "bg": "#FFE8CC",
          "text": "#8B5000",
          "border": "#FF9500"
        },
        "danger": {
          "bg": "#FFCCCC",
          "text": "#B91F1F",
          "border": "#FF3B30"
        }
      }
    },

    "typography": {
      "fontFamily": {
        "default": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
      },
      "fontWeights": {
        "light": 300,
        "normal": 400,
        "semibold": 600,
        "bold": 700
      },
      "headings": {
        "h1": {"fontSize": "56px", "fontWeight": 700},
        "h2": {"fontSize": "40px", "fontWeight": 600}
      },
      "body": {
        "fontSize": "17px",
        "fontWeight": 400,
        "lineHeight": 1.5
      }
    },

    "spacing": {
      "xs": "4px",
      "sm": "8px",
      "md": "16px",
      "lg": "24px",
      "xl": "32px",
      "2xl": "48px"
    },

    "borderRadius": {
      "sm": "4px",
      "md": "8px",
      "lg": "12px"
    },

    "shadows": {
      "sm": "0 1px 3px rgba(0,0,0,0.07)",
      "md": "0 2px 8px rgba(0,0,0,0.08)"
    }
  },

  "components": [
    {
      "id": "stat-grid",
      "name": "Statistic Grid",
      "description": "Display statistics in grid",
      "gridColumns": "auto-fit, minmax(220px, 1fr)"
    }
    // ... weitere 9 Component-Typen
  ]
}
```

**Vollständige Beispiele:**
- `shared-themes/apple/design-guide.json`
- `shared-themes/openai/design-guide.json`
- `projects/beispiel-projekt/styles/github/design-guide.json`

### Schritt 3: variables.css erstellen

Die `variables.css` definiert CSS Custom Properties (CSS-Variablen), die von `style.css` verwendet werden.

**Template:**
```css
/* My Theme - CSS Variablen */

:root {
  /* Primärfarben */
  --color-primary: #0071E3;
  --color-primary-light: #4DA3FF;
  --color-primary-dark: #0051B3;

  /* Komponenten-Hintergrund */
  --color-bg-component: #ffffff;
  --color-bg-subtle: #f5f5f7;

  /* Text-Farben */
  --color-text-primary: #1d1d1d;
  --color-text-secondary: #555555;
  --color-text-muted: #888888;
  --color-text-on-primary: #ffffff;

  /* Rahmen-Farben */
  --color-border: #e5e5e7;
  --color-border-hover: #0071E3;

  /* Semantic Colors */
  --color-success: #34C759;
  --color-warning: #FF9500;
  --color-danger: #FF3B30;

  /* Schatten */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.07);
  --shadow-md: 0 2px 8px rgba(0,0,0,0.08);

  /* Border Radius */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;

  /* Schriftart */
  --font-family: -apple-system, BlinkMacSystemFont, sans-serif;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;

  /* Komponenten-spezifisch */
  --component-padding: 48px;
  --component-border-width: 1px;
  --component-border-radius: var(--border-radius-md);
  --component-shadow: var(--shadow-sm);
}
```

### Schritt 4: style.css erstellen

Die `style.css` definiert das eigentliche Styling für alle Komponenten. Sie importiert `variables.css` und verwendet die CSS-Variablen.

**Empfehlung:** Kopiere eine existierende `style.css` als Ausgangspunkt:

```bash
cp shared-themes/apple/style.css shared-themes/my-theme/style.css
```

Passe dann nur den Header-Kommentar an:

```css
/* My Theme - Komponenten Styles */

@import url('variables.css');

/* Theme-specific notes here */

/* Komponenten-Basis */
.component {
    background: var(--color-bg-component);
    border: var(--component-border-width) solid var(--color-border);
    border-radius: var(--component-border-radius);
    padding: var(--component-padding);
    /* ... */
}

/* Stat Grid */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    /* ... */
}

/* ... weitere Komponenten ... */
```

### Schritt 5: design-guide.md erstellen (Optional aber empfohlen)

Human-readable Markdown-Version deines Design Guides für Dokumentationszwecke.

**Template:**
```markdown
# My Theme Design System

Description of your theme.

## Colors

### Primary
- **Main**: `#0071E3` - Primary accent
- **Light**: `#4DA3FF`
- **Dark**: `#0051B3`

### Background
- **Main**: `#ffffff` - Pure white
- **Subtle**: `#f5f5f7` - Light gray

## Typography

- **Font Family**: -apple-system, BlinkMacSystemFont
- **Body Size**: 17px
- **Line Height**: 1.5

## Spacing

- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px

## Components

### Stat Grid
Display statistics in clean cards...

### Bullet List
Formatted lists with emphasis...

...
```

### Schritt 6: In projects.json registrieren

Öffne `presentation/projects.json` und füge dein Theme zum `sharedThemes` Array hinzu:

```json
{
  "defaultStyle": "github",
  "sharedThemes": [
    {
      "name": "apple",
      "displayName": "Apple Design",
      "cssPath": "shared-themes/apple/style.css",
      "default": false
    },
    {
      "name": "my-theme",
      "displayName": "My Custom Theme",
      "cssPath": "shared-themes/my-theme/style.css",
      "default": false
    }
  ],
  "projects": [...]
}
```

### Schritt 7: Testen

1. **Start API Server:**
   ```bash
   cd presentation
   python3 run_api.py
   ```

2. **Öffne unified-editor.html:**
   ```bash
   # Option 1: File-Protokoll
   open unified-editor.html

   # Option 2: Mit lokalem Server (empfohlen)
   python3 -m http.server 8000
   # Dann: http://localhost:8000/unified-editor.html
   ```

3. **Teste Theme:**
   - Wähle Projekt "beispiel-projekt"
   - Im Theme-Dropdown sollte unter "Shared Themes" dein Theme erscheinen
   - Wähle dein Theme aus
   - Generiere eine Test-Folie
   - Prüfe, ob das Styling korrekt angewendet wird

### Schritt 8: Validierung

Checklist für Qualitätssicherung:

#### CSS-Validierung
- [ ] Alle 10 Component-Typen haben CSS-Styles
- [ ] CSS-Variablen matchen design-guide.json tokens
- [ ] Keine hard-coded Farben (verwende CSS-Variablen)
- [ ] Responsive breakpoints funktionieren

#### design-guide.json Validierung
- [ ] Valides JSON (keine Syntax-Fehler)
- [ ] Alle 10 Component-Typen definiert:
  - stat-grid
  - bullet-list
  - quote
  - text
  - table
  - image-frame
  - image-grid
  - feature-grid
  - process
  - process-horizontal
- [ ] Tokens vollständig (colors, typography, spacing, borderRadius, shadows)

#### Accessibility
- [ ] Kontrast-Ratios erfüllen WCAG AA (mindestens)
  - Text/Background: ≥4.5:1
  - Primary/White: ≥4.5:1
- [ ] Empfohlen: WCAG AAA (7:1)
- [ ] Semantic colors haben ausreichenden Kontrast

#### Browser-Kompatibilität
- [ ] Chrome/Edge getestet
- [ ] Firefox getestet
- [ ] Safari getestet (falls macOS vorhanden)

## Project-Specific Themes

Falls du ein Theme nur für ein bestimmtes Projekt erstellen möchtest:

### Struktur

```
presentation/projects/my-project/
└── styles/
    └── my-theme/
        ├── design-guide.json
        ├── design-guide.md
        ├── style.css
        ├── variables.css
        └── reference.html (optional)
```

### Registrierung

Themes werden automatisch aus dem `styles/` Verzeichnis des Projekts geladen. Keine manuelle Registrierung nötig.

## Troubleshooting

### Theme wird nicht angezeigt

**Problem:** Theme erscheint nicht im Dropdown

**Lösungen:**
1. Prüfe `projects.json` Syntax (valides JSON?)
2. Prüfe Pfad in `cssPath` (korrekt?)
3. Browser-Cache leeren
4. API Server neu starten

### CSS wird nicht geladen

**Problem:** Theme ist ausgewählt, aber Styling fehlt

**Lösungen:**
1. Öffne Browser DevTools → Network Tab
2. Prüfe, ob `style.css` erfolgreich geladen wird (Status 200)
3. Prüfe Pfad: `shared-themes/{theme}/style.css`
4. Prüfe, ob `@import url('variables.css');` in style.css korrekt ist

### Components sehen falsch aus

**Problem:** Components werden gerendert, aber sehen nicht wie erwartet aus

**Lösungen:**
1. Prüfe CSS-Variablen in `variables.css`
2. Vergleiche mit Referenz-Theme (apple, openai, github)
3. Prüfe Browser DevTools → Elements → Computed Styles
4. Prüfe, ob CSS-Klassen korrekt sind (`.component`, `.stat-grid`, etc.)

### design-guide.json wird nicht gelesen

**Problem:** Agents verwenden nicht deine design-guide.json

**Lösungen:**
1. Prüfe JSON-Syntax (valides JSON?)
2. Prüfe API-Logs für Fehler
3. Prüfe Pfad: `shared-themes/{theme}/design-guide.json`
4. Fallback-Chain: projekt → shared → default

## Best Practices

### 1. Konsistente Benennung

- Theme-Namen: lowercase, hyphen-separated (`my-theme`, nicht `MyTheme`)
- CSS-Variablen: kebab-case (`--color-primary`, nicht `--colorPrimary`)
- Component-IDs: kebab-case (`stat-grid`, nicht `statGrid`)

### 2. Design Tokens verwenden

Definiere alle Werte in `variables.css` und verwende sie in `style.css`:

```css
/* ❌ Hard-coded */
.component {
    background: #ffffff;
    border: 1px solid #e5e5e7;
}

/* ✅ Mit Variablen */
.component {
    background: var(--color-bg-component);
    border: var(--component-border-width) solid var(--color-border);
}
```

### 3. Accessibility First

- Teste Kontrast-Ratios: https://webaim.org/resources/contrastchecker/
- Verwende semantische Farben konsistent
- Teste mit Screen-Reader (optional)

### 4. Mobile-First Responsive Design

- Definiere mobile Styles zuerst
- Verwende `@media (min-width: ...)` für größere Screens
- Teste auf verschiedenen Bildschirmgrößen

### 5. Dokumentation

- Füge Kommentare in `style.css` hinzu
- Erstelle `design-guide.md` mit Beispielen
- Dokumentiere Theme-spezifische Besonderheiten

## Referenzen

### Beispiel-Themes

**Apple Design:**
- `shared-themes/apple/design-guide.json`
- Clean, minimalistisch
- Subtile Schatten
- Kleine Border-Radius (4-12px)

**OpenAI Design:**
- `shared-themes/openai/design-guide.json`
- Modern, warm
- Weiche Schatten (mehrschichtig)
- Mittlere Border-Radius (6-16px)

**GitHub Design:**
- `projects/beispiel-projekt/styles/github/design-guide.json`
- Professional, clean
- GitHub-typische Farben
- Standard Border-Radius (3-12px)

### Weitere Dokumentation

- **QUALITY-GUIDE.md** - Qualitätsstandards für generierte Folien
- **presentation/SETUP.md** - Setup-Anleitung
- **CLAUDE.md** - Vollständige Projekt-Dokumentation
- **presentation/api/README.md** - API-Dokumentation

## Support

Bei Fragen oder Problemen:
1. Prüfe diese Dokumentation
2. Vergleiche mit Beispiel-Themes
3. Prüfe API-Logs für Fehler
4. Öffne GitHub Issue mit Reproduktionsschritten

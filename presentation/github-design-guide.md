# GitHub Design Guide für Präsentationen

## Farben

### Primärfarbe
- **GitHub Green**: Die charakteristische Hauptfarbe von GitHub
  - Hex: `#238636` (Standard)
  - Alternativ: `#2ea043` (Heller)
  - RGB: `rgb(35, 134, 54)`

### Farbschema (Light Mode)
- **Hintergrund**: `#ffffff` (Weiß)
- **Text Primär**: `#24292f` (Dunkelgrau)
- **Text Sekundär**: `#57606a` (Mittelgrau)
- **Border**: `#d0d7de` (Hellgrau)
- **Hover Background**: `#f6f8fa` (Sehr helles Grau)

### Farbschema (Dark Mode)
- **Hintergrund**: `#0d1117` (Sehr dunkel)
- **Text Primär**: `#c9d1d9` (Hellgrau)
- **Text Sekundär**: `#8b949e` (Mittelgrau)
- **Border**: `#30363d` (Dunkelgrau)
- **Hover Background**: `#161b22` (Dunkelgrau)

### Akzentfarben
- **Blau**: `#0969da` (Links, Links)
- **Rot**: `#cf222e` (Fehler, Warnungen)
- **Orange**: `#d1242f` (Warnungen)
- **Gelb**: `#bf8700` (Hinweise)
- **Lila**: `#8250df` (Features)

## Typografie

### Marketing & Branding Fonts
- **Mona Sans SemiBold**: Für Überschriften und Titel
- **Monaspace Neon Medium**: Für Code und technische Inhalte

### UI Font Stack (System Fonts)
GitHub verwendet einen System-Font-Stack für die Benutzeroberfläche:
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
```

### Typografische Skala

#### Titel
- Größe: 32-48px
- Gewicht: 600-700 (SemiBold bis Bold)
- Zeilenhöhe: 1.25

#### Überschriften
- H1: 32px, Gewicht 600
- H2: 24px, Gewicht 600
- H3: 20px, Gewicht 600
- H4: 16px, Gewicht 600
- Zeilenhöhe: 1.25-1.5

#### Fließtext
- Größe: 14-16px
- Gewicht: 400 (Regular)
- Zeilenhöhe: 1.5-1.75

## Stilelemente

### Buttons
- **Primär Button**: GitHub Green Hintergrund, weißer Text
- **Sekundär Button**: Weißer Hintergrund, GitHub Green Text, Border
- **Border Radius**: 6px
- **Padding**: 8px 16px
- **Font Size**: 14px
- **Font Weight**: 500-600

### Cards & Container
- **Border Radius**: 6px
- **Border**: 1px solid `#d0d7de` (Light) / `#30363d` (Dark)
- **Background**: `#ffffff` (Light) / `#161b22` (Dark)
- **Box Shadow**: Subtile Schatten für Tiefe

### Spacing
- **Base Unit**: 4px
- **Kleine Abstände**: 4px, 8px
- **Mittlere Abstände**: 16px, 24px
- **Große Abstände**: 32px, 48px

### Icons
- **Größe**: 16px, 20px, 24px
- **Farbe**: Folgt Text-Farben
- **Style**: Outline/Icons mit 1.5-2px Stroke

## CSS Implementierung

### CSS Variablen (Light Mode)
```css
:root {
  --color-fg-default: #24292f;
  --color-fg-muted: #57606a;
  --color-canvas-default: #ffffff;
  --color-border-default: #d0d7de;
  --color-btn-primary-bg: #238636;
  --color-btn-primary-hover-bg: #2ea043;
  --color-accent-fg: #0969da;
}
```

### CSS Variablen (Dark Mode)
```css
[data-theme="dark"] {
  --color-fg-default: #c9d1d9;
  --color-fg-muted: #8b949e;
  --color-canvas-default: #0d1117;
  --color-border-default: #30363d;
  --color-btn-primary-bg: #238636;
  --color-btn-primary-hover-bg: #2ea043;
  --color-accent-fg: #58a6ff;
}
```

## Präsentations-Tipps

1. **Konsistente Farbverwendung**: Verwenden Sie GitHub Green sparsam als Akzentfarbe
2. **Klare Typografie-Hierarchie**: Nutzen Sie die definierten Größen für Titel, Überschriften und Text
3. **Ausreichend Whitespace**: GitHub legt Wert auf klare, luftige Layouts
4. **Subtile Schatten**: Verwenden Sie leichte Schatten für Tiefe
5. **Runde Ecken**: 6px Border Radius für moderne, freundliche Optik

## Ressourcen

- GitHub Brand Toolkit: https://brand.github.com/foundations
- GitHub Primer Design System: https://primer.style
- Mona Sans Font: https://github.com/github/mona-sans
- Monaspace Font: https://github.com/github/monaspace


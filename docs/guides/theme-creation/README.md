# Theme Creation - Quick Reference

**Schnell-Anleitung:** Erstelle ein neues Theme in 10 Schritten.

Für ausführliches Tutorial siehe: [tutorial.md](tutorial.md)

---

## ✅ Checkliste: Theme in 10 Schritten

### 1. Verzeichnis erstellen
```bash
cd presentation/shared-themes
mkdir my-theme
cd my-theme
```

### 2. design-guide.json erstellen
```json
{
  "theme": "my-theme",
  "name": "My Custom Theme",
  "version": "1.0.0",
  "tokens": {
    "colors": {
      "primary": {"main": "#0071E3"},
      "background": {"main": "#ffffff"},
      "text": {"primary": "#1d1d1d"}
    },
    "typography": {
      "fontFamily": {"default": "-apple-system, sans-serif"},
      "fontWeights": {"normal": 400, "bold": 700}
    },
    "spacing": {"md": "16px", "lg": "24px"},
    "borderRadius": {"md": "8px"},
    "shadows": {"sm": "0 1px 3px rgba(0,0,0,0.07)"}
  },
  "components": [
    {"id": "stat-grid", "name": "Statistic Grid"},
    {"id": "bullet-list", "name": "Bullet List"}
  ]
}
```

### 3. variables.css erstellen
```css
:root {
  --color-primary: #0071E3;
  --color-bg-main: #ffffff;
  --color-text-primary: #1d1d1d;
  --font-family: -apple-system, sans-serif;
  --spacing-md: 16px;
  --border-radius-md: 8px;
}
```

### 4. style.css erstellen
```css
@import url('variables.css');

.component {
  background: var(--color-bg-main);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--spacing-md);
}
```

### 5. In projects.json registrieren
```json
{
  "sharedThemes": [
    {
      "name": "my-theme",
      "displayName": "My Custom Theme",
      "cssPath": "shared-themes/my-theme/style.css",
      "default": false
    }
  ]
}
```

### 6. Server starten
```bash
cd presentation
python3 run_api.py
```

### 7. Frontend öffnen
```bash
open unified-editor.html
```

### 8. Theme testen
- Select Project: "beispiel-projekt"
- Select Theme: "my-theme" (unter "Shared Themes")
- Generate test slide

### 9. Validierung
- [ ] Alle 10 Component-Types haben CSS
- [ ] CSS-Variablen matchen design-guide.json
- [ ] Kontrast-Ratios ≥4.5:1 (WCAG AA)
- [ ] Responsive Design funktioniert

### 10. Optional: design-guide.md erstellen
Human-readable Dokumentation des Themes.

---

## 📦 Vollständige Beispiele

**Referenz-Themes:**
- [Apple Design](../../../presentation/shared-themes/apple/)
- [OpenAI Design](../../../presentation/shared-themes/openai/)
- [GitHub Design](../../../presentation/projects/beispiel-projekt/styles/github/)

---

## 🎨 Design Tokens

### Pflicht-Felder

**colors:**
- `primary.main` - Haupt-Akzentfarbe
- `background.main` - Haupt-Hintergrund
- `text.primary` - Haupt-Textfarbe

**typography:**
- `fontFamily.default` - Standard-Schriftart
- `fontWeights.normal` - Normales Gewicht

**spacing:**
- `md` - Standard-Abstand (16px empfohlen)
- `lg` - Großer Abstand (24px empfohlen)

**borderRadius:**
- `md` - Standard-Radius (8px empfohlen)

**shadows:**
- `sm` - Kleiner Schatten

### Alle Component-Types

Mindestens diese 10 Components definieren:

1. `stat-grid` - Statistiken
2. `bullet-list` - Listen
3. `quote` - Zitate
4. `text` - Fließtext
5. `table` - Tabellen
6. `image-frame` - Einzelbild
7. `image-grid` - Bild-Grid
8. `feature-grid` - Feature-Cards
9. `process` - Prozess vertikal
10. `process-horizontal` - Prozess horizontal

---

## 🔧 Tools

### Farben & Kontrast
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) ⭐
- [Coolors.co](https://coolors.co/) - Palette Generator

### Fonts
- [Google Fonts](https://fonts.google.com/)
- [Font Pair](https://fontpair.co/)

Siehe: [tools.md](tools.md) für vollständige Liste

---

## ❌ Häufige Fehler

### Theme erscheint nicht im Dropdown
→ Siehe: [troubleshooting.md](troubleshooting.md#theme-wird-nicht-angezeigt)

### CSS wird nicht geladen
→ Siehe: [troubleshooting.md](troubleshooting.md#css-wird-nicht-geladen)

### Komponenten sehen falsch aus
→ Siehe: [troubleshooting.md](troubleshooting.md#komponenten-sehen-falsch-aus)

---

## 📖 Weiterführende Docs

- **[Ausführliches Tutorial](tutorial.md)** - Schritt-für-Schritt mit Erklärungen
- **[Apple Theme Walkthrough](apple-walkthrough.md)** - Komplettes Beispiel
- **[OpenAI Theme Walkthrough](openai-walkthrough.md)** - Komplettes Beispiel
- **[Tools & Resources](tools.md)** - Design-Tools, Farben, Fonts
- **[Troubleshooting](troubleshooting.md)** - Probleme & Lösungen

---

## 🎯 Next Steps

1. **Einfacher Start**: Kopiere ein existierendes Theme und passe Farben an
   ```bash
   cp -r shared-themes/apple shared-themes/my-theme
   # Passe design-guide.json + variables.css an
   ```

2. **Vollständiges Tutorial**: [tutorial.md](tutorial.md)

3. **Real-World Beispiel**: [apple-walkthrough.md](apple-walkthrough.md)

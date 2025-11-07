# Output Ordner - Screenshot-Vorlagen

Dieser Ordner enthält einzelne Slide-Vorlagen mit klarer Screenshot-Border für die finale Präsentation.

## Verwendung

1. **Vorlage öffnen:** Öffnen Sie eine der HTML-Dateien im Browser
2. **Inhalte anpassen:** Bearbeiten Sie die Platzhaltertexte mit Ihren eigenen Inhalten
3. **Screenshot erstellen:** Die grüne Border zeigt genau den Screenshot-Bereich (1920x1080px)
4. **Info-Banner entfernen:** Für finale Screenshots können Sie das Info-Banner im Code entfernen

## Screenshot-Border

- **Grüne Border:** Zeigt den exakten Screenshot-Bereich
- **Größe:** 1920x1080px (16:9 Format)
- **Ecken-Marker:** Zusätzliche Markierungen in den Ecken

## Verfügbare Vorlagen

### `timeline-example.html`
Beispiel-Timeline-Folie mit Roadmap-Darstellung.

**Anpassungen:**
- Überschrift ändern
- Quartale/Zeitpunkte anpassen
- Meilensteine und Ziele anpassen
- Styling über CSS-Variablen ändern

## Tipps für Screenshots

1. **Browser DevTools:** F12 → Device Toolbar → Custom → 1920x1080px
2. **Zoom:** Stellen Sie sicher, dass der Browser-Zoom auf 100% steht
3. **Border entfernen:** Für finale Screenshots können Sie die Border im CSS entfernen:
   ```css
   .screenshot-area {
       border: none; /* Border entfernen */
   }
   ```
4. **Info-Banner:** Entfernen Sie das `.screenshot-info` Element für finale Screenshots

## Neue Slides erstellen

Kopieren Sie eine bestehende Vorlage und passen Sie den Inhalt an. Die Struktur sollte sein:

```html
<div class="screenshot-area">
    <section class="slide">
        <!-- Ihr Inhalt hier -->
    </section>
</div>
```

## Design-System

Alle Vorlagen verwenden das GitHub Design System aus `../github-presentation-template.css`.

**Verfügbare CSS-Klassen:**
- `.card` - Card-Container
- `.grid`, `.grid-2`, `.grid-3` - Grid-Layouts
- `.timeline` - Timeline-Darstellung
- `.stat-number` - Große Zahlen
- `.badge` - Badges/Labels
- `.btn`, `.btn-primary` - Buttons
- Und viele mehr...

Siehe `../github-design-guide.md` für Details.



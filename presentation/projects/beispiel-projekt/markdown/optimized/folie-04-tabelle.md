# Folie 4: Vergleichstabelle - Roboter-Modelle

## Komponente 4.1: Roboter-Modell Vergleich

**Hinweis für LLM:** Diese Komponente enthält eine Vergleichstabelle mit Badges für Verfügbarkeit. Die Tabelle sollte die CSS-Klasse `comparison-table` haben.

| Modell | Preis | Einsatzbereich | Verfügbarkeit |
|--------|-------|----------------|---------------|
| Unitree H1 | ~84.000 € | Industrie, Forschung | Verfügbar |
| 1X NEO | ~18.500 € | Service, Haushalt | 2026 |
| Unitree G1 | ~15.000 € | Bildung, Forschung | Verfügbar |
| Unitree R1 | ~5.100 € | Entry-Level, Entwicklung | Verfügbar |
| Neura 4NE-1 | <50.000 € | Industrie, Service | Ende 2025 |

**Erwartetes HTML:**
- `<table class="comparison-table">` mit `<thead>` und `<tbody>`
- Verfügbarkeit-Spalte sollte `<span class="badge badge-success">` oder `<span class="badge badge-warning">` enthalten
- "Verfügbar" → `badge-success`
- Jahreszahlen → `badge-warning`

---

## Komponente 4.2: Geschäftsmodell Vergleich

| Kriterium | Kauf | Miete (Robo4you) |
|-----------|------|------------------|
| Anschaffungskosten | 50.000 - 150.000 € | 0 € |
| Monatliche Kosten | Wartung: ~500 € | 2.500 - 4.500 € (alles inkl.) |
| Updates & Upgrades | Zusätzliche Kosten | Inklusive |
| Risiko | Beim Kunden | Bei Robo4you |
| Flexibilität | Gering | Hoch (kündbar) |

**Erwartetes HTML:**
- Standard `<table>` ohne spezielle CSS-Klasse
- `<thead>` mit Spaltenüberschriften
- `<tbody>` mit den Vergleichsdaten


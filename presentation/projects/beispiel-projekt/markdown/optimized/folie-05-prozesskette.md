# Folie 5: Prozesskette - Deployment-Workflow

## Komponente 5.1: Vertikale Prozesskette

**Hinweis für LLM:** Diese Komponente zeigt eine vertikale Prozesskette mit nummerierten Schritten. Jeder Schritt hat eine Nummer in einem Kreis und einen Titel mit Beschreibung.

1. **Bedarfserhebung**
   Analyse der Anforderungen und Einsatzbereiche beim Kunden

2. **Roboter-Auswahl**
   Passendes Modell basierend auf Anforderungen und Budget

3. **Installation & Setup**
   Vor-Ort Installation und erste Konfiguration durch unsere Techniker

4. **Schulung & Training**
   Umfassende Schulung der Mitarbeiter durch Robotik-Coaches

5. **Betrieb & Support**
   Kontinuierlicher Support, Wartung und Updates während der Laufzeit

**Erwartetes HTML:**
- `<div class="process-chain">` als Container
- Für jeden Schritt: `<div class="process-step">`
  - `<div class="process-number">` für die Nummer (1, 2, 3, etc.)
  - `<div class="process-content">` mit `<h4>` für Titel und `<p>` für Beschreibung
- Die Verbindungslinie zwischen Schritten wird automatisch durch CSS erzeugt (`::after` Pseudo-Element)

---

## Komponente 5.2: Horizontale Prozesskette

**Hinweis für LLM:** Diese Komponente zeigt eine horizontale Prozesskette mit kompakter Darstellung.

1. Kontakt - Erstgespräch
2. Analyse - Bedarf prüfen
3. Angebot - Kosten kalkulieren
4. Deployment - Installation
5. Betrieb - Support & Wartung

**Erwartetes HTML:**
- `<div class="process-horizontal">` als Container
- Für jeden Schritt: `<div class="process-item">`
  - `<div class="process-item-circle">` für die Nummer
  - `<div class="process-item-title">` für den Titel
  - `<div class="process-item-desc">` für die Beschreibung
- Die Verbindungslinie wird automatisch durch CSS erzeugt (`::before` Pseudo-Element)


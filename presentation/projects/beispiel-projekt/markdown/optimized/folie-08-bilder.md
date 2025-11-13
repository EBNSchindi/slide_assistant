# Folie 8: Bilder & Visualisierungen

## Komponente 8.1: Einzelnes Bild mit Rahmen

**Hinweis für LLM:** Diese Komponente zeigt ein einzelnes Bild mit Rahmen, Überschrift und Beschreibung darunter.

![Unitree H1 - High-End Roboter](images/unitree-h1.jpg)

**Unitree H1 - High-End Roboter**

Der Unitree H1 ist ein humanoider Roboter für industrielle Anwendungen. Mit einer Höhe von 1,80m und 47 kg Gewicht bietet er beeindruckende Bewegungsfähigkeiten und kann Lasten bis zu 30 kg tragen.

**Erwartetes HTML:**
- `<div class="image-container">` als äußerer Rahmen
- `<div class="image-wrapper">` für das Bild
  - `<img src="..." alt="...">` für echte Bilder ODER
  - `<div class="image-placeholder">Bild Platzhalter</div>` als Fallback
- `<div class="image-content">` für Text-Bereich
  - `<h4>` für Überschrift
  - `<p>` für Beschreibung

---

## Komponente 8.2: Bild-Grid (mehrere Bilder)

**Hinweis für LLM:** Diese Komponente zeigt mehrere Bilder in einem Grid-Layout mit Badges.

![Unitree H1](images/unitree-h1.jpg) - **Unitree H1** - High-End Industrie-Roboter [Status: Verfügbar]

![1X NEO](images/1x-neo.jpg) - **1X NEO** - Service-Roboter für Haushalt [Status: 2026]

![Unitree G1](images/unitree-g1.jpg) - **Unitree G1** - Bildung & Forschung [Status: Verfügbar]

**Erwartetes HTML:**
- `<div class="image-grid">` als Container
- Für jedes Bild: `<div class="image-card">`
  - `<div class="image-wrapper">` mit Bild oder Platzhalter
    - `<span class="image-badge">` mit `<span class="badge badge-success">` oder `badge-warning`
  - `<div class="image-content">` mit `<h4>` und `<p>`

---

## Komponente 8.3: Referenz-Deployment

![GXO × Agility Robotics Deployment](images/gxo-agility.jpg)

**Erster kommerzieller Dauerbetrieb**

GXO Logistics und Agility Robotics haben im Juni 2024 den ersten kommerziellen Dauerbetrieb von humanoiden Robotern in einem Lager nahe Atlanta gestartet. Die Digit-Roboter unterstützen bei der Materialhandhabung und Logistik.

**Standort:** Atlanta, USA | **Start:** Juni 2024 | **Status:** Aktiv

**Erwartetes HTML:**
- `<div class="image-container">` mit Bild und Text
- Zusätzliche Metadaten als `<p>` mit `<strong>` Tags
- Status als `<span class="badge badge-success">Aktiv</span>`

---

## Komponente 8.4: Roboter im Einsatz

![Roboter in Pflegeeinrichtung](images/roboter-pflege.jpg)

**Einsatz in Pflegeheimen**

Humanoide Roboter unterstützen Pflegekräfte bei alltäglichen Aufgaben wie Materialtransport, Patientenbetreuung und Dokumentation. Dies entlastet das Personal und ermöglicht mehr Zeit für die direkte Pflege.

- Materialtransport zwischen Stationen
- Unterstützung bei der Patientenbetreuung
- Dokumentationshilfe
- 24/7 Verfügbarkeit

**Erwartetes HTML:**
- `<div class="image-container">` mit größerem Bild (`style="min-height: 250px;"`)
- `<div class="image-content">` mit `<h4>`, `<p>` und `<ul class="bullet-list">`


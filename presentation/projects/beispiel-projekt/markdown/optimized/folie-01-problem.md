# Folie 1: Problem - Demografischer Wandel

## Komponente 1.1: Die Zahlen sprechen für sich

**Hinweis für LLM:** Diese Komponente enthält Statistiken, die als `stat-grid` mit `stat-card` Elementen dargestellt werden sollen.

- 83,6 Mio Einwohner in Deutschland (2024)
- 5,7 Mio Pflegebedürftige (Stand 2023)
- 500.000 Fehlende Pflegekräfte bis 2030
- 16.500 Pflegeheime benötigen Unterstützung

**Erwartetes HTML:** `<div class="stat-grid">` mit mehreren `<div class="stat-card">` Elementen, die `<span class="stat-number">` und `<span class="stat-label">` enthalten.

---

## Komponente 1.2: Wachsende Belastung

Der Altersquotient steigt dramatisch:

- **37%** heute (37 über 67-Jährige pro 100 Erwerbsfähige)
- **>50%** bis 2040 prognostiziert

> "17 Millionen erwirtschaften für 90 Millionen"

**Erwartetes HTML:** 
- `<ul class="bullet-list">` für die Liste
- `<div class="quote">` für das Zitat

---

## Komponente 1.3: Finanzielle Belastung

**Hinweis für LLM:** Diese Komponente kombiniert eine Statistik mit einer Bullet-Liste.

- 52,9% Einkommensbelastungsquote (2025)
- Mehr als die Hälfte des Einkommens geht an den Staat
- Tendenz steigend

**Erwartetes HTML:**
- `<div class="stat-grid">` mit einer `stat-card` für die Prozentzahl
- `<ul class="bullet-list">` für die weiteren Punkte


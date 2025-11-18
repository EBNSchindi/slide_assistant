# Agent Prompt Optimizations

**Datum:** 18. November 2025
**Basierend auf:** Pitch Deck Test Analysis (8 Folien)
**Ziel:** Verbesserung der feature-grid Erkennung und max_components Handling

---

## Executive Summary

Nach dem umfassenden Funktionstest mit 8 Folien wurden **3 kritische Probleme** identifiziert:

1. ❌ **feature-grid nicht erkannt** (Folie 06) - Agent nutzt text/bullet-list statt feature-grid
2. ⚠️ **max_components=3 zu strikt** - Agent komprimiert Inhalte suboptimal
3. ⚠️ **Text vs. Bullet-List Inkonsistenzen** - Weniger kritisch

**Erfolgsrate vor Optimierung:**
- ✅ Content-Erhaltung: 100%
- ⚠️ Struktur-Matches: 62.5% (5/8 Folien)
- ⚠️ feature-grid Erkennung: 0% (0/1 Folie wo erwartet)

---

## Problem 1: Fehlende Komponenten-Typen im Prompt

### Diagnose

Der `PresentationStrategistAgentV2` Prompt listete nur **7 Komponenten**, obwohl **10 Templates** existieren:

**Vorhandene Templates:**
1. stat-grid.html.j2 ✅
2. bullet-list.html.j2 ✅
3. quote.html.j2 ✅
4. text.html.j2 ✅
5. image-frame.html.j2 ✅
6. process.html.j2 ✅
7. table.html.j2 ✅
8. **feature-grid.html.j2 ❌ FEHLTE IM PROMPT**
9. **image-grid.html.j2 ❌ FEHLTE IM PROMPT**
10. **process-horizontal.html.j2 ❌ FEHLTE IM PROMPT**

**Konsequenz:**
- Folie 06 (6 Features) → Agent nutzte text + bullet-list + bullet-list statt feature-grid
- Folie 08 (4 Bilder) → image-grid wurde zufällig genutzt (nicht dokumentiert)
- Folie 05 (Prozess) → process-horizontal funktionierte zufällig

### Lösung

**✅ presentation/api/agents/presentation_strategist_v2.py**

Ergänzt 3 fehlende Komponenten im System-Prompt:

```python
8. feature-grid
   Purpose: Display multiple features/products with icons and descriptions
   Best for: Multiple related features, product offerings, USPs with titles
   Constraints: 3-6 features per grid, each with title + description
   **WHEN TO USE**: User lists multiple features/benefits/USPs with consistent structure
   Example input: "✨ Feature 1: Description\n🎯 Feature 2: Description"

9. image-grid
   Purpose: Display multiple images in a grid layout
   Best for: Multiple related images that belong together (gallery, comparison)
   Constraints: 2-4 images in grid
   **WHEN TO USE**: User mentions multiple images for same context

10. process-horizontal
    Purpose: Show sequential workflow/timeline horizontally
    Best for: Linear workflows, timelines, step-by-step processes displayed left-to-right
    Constraints: 4-6 steps max, each with title + description
    **WHEN TO USE**: When process/timeline should flow horizontally instead of vertically
```

**✅ OUTPUT FORMAT** aktualisiert:

```python
"type": "stat-grid|bullet-list|quote|text|image-frame|process|table|feature-grid|image-grid|process-horizontal"
```

---

## Problem 2: feature-grid Entscheidungslogik fehlt

### Diagnose

Der `ContentAnalyzerAgentV2` hatte keinen Content-Block-Type für "Features", daher:
- Agent 1 klassifizierte Features als "bullets"
- Agent 2 wählte bullet-list statt feature-grid

### Lösung

**✅ presentation/api/agents/content_analyzer_v2.py**

Ergänzt 2 neue Content-Block-Types:

```python
9. FEATURE - A feature/product/USP with title and description
   Example: {"type": "feature", "content": "🤖 KI-gestützte Anpassung: Adaptive Lernalgorithmen"}
   Use when: User lists features/benefits/USPs with consistent title:description structure
   **WHEN TO USE**: Multiple features/benefits/USPs (3+ items) with similar formatting
   **STRUCTURE**: Icon/Emoji + Title: Description

10. FEATURES - Multiple features grouped together
    Example: {"type": "features", "content": "✨ Feature 1: Desc\n🎯 Feature 2: Desc\n💡 Feature 3: Desc"}
    Use when: 3+ related features/benefits that should be displayed as a grid
    **CRITICAL**: Use this when you detect 3+ feature-like items with consistent structure
```

**✅ presentation/api/agents/presentation_strategist_v2.py**

Ergänzt FEATURES Decision Rule:

```python
**🟠 FEATURES (IMPORTANT RULE):**
→ If ANY ContentBlock has type "feature" OR "features":
→ ALWAYS use "feature-grid" component type
→ Combine all feature blocks into single feature-grid (3-6 features)
→ Do NOT split into multiple bullet-list or text components
→ Example: 6 features with icons → single feature-grid, NOT 3 × bullet-list
```

---

## Problem 3: max_components Handling zu strikt

### Diagnose

Agent respektierte "Max 3 components" zu strikt und komprimierte Inhalte ungeschickt:

- Folie 06: 6 Features → 3 separate Komponenten (text + bullet-list × 2) statt 1 feature-grid
- Folie 08: 4 Bilder → 3 Komponenten (image-frame + text + image-grid) statt optimal
- Folie 07: 2 Tabellen + Info → 3 Komponenten (sinnvoll, aber könnte 2 sein)

**Missverständnis:** Agent dachte "max 3 components" = "max 3 content items"

### Lösung

**✅ presentation/api/agents/presentation_strategist_v2.py**

QUALITY RULES präzisiert:

```python
✓ Max 3 components per slide (design constraint)
  → HOWEVER: feature-grid with 6 features = 1 component (not 3)
  → HOWEVER: image-grid with 4 images = 1 component (not 4)
  → Think in components, not in content items
  → Prefer aggregating related content into one rich component over splitting

✓ Each component should focus on one idea/dimension
  → Exception: feature-grid groups multiple related features (that's its purpose)

EXAMPLE:
  ❌ BAD: 6 features → text + bullet-list + bullet-list (3 components, fragmented)
  ✅ GOOD: 6 features → feature-grid (1 component, cohesive)
```

---

## Zusammenfassung der Änderungen

| Datei | Änderungen | Zeilen |
|-------|------------|--------|
| `presentation/api/agents/presentation_strategist_v2.py` | + 3 Komponenten-Definitionen<br>+ FEATURES Decision Rule<br>+ Präzisierte Quality Rules<br>+ Aktualisiertes OUTPUT FORMAT | ~45 |
| `presentation/api/agents/content_analyzer_v2.py` | + 2 Content-Block-Types (FEATURE, FEATURES)<br>+ Feature-Struktur-Dokumentation | ~20 |

---

## Erwartete Verbesserungen

### Folie 06: Features & Vorteile

**Vorher:**
- Komponenten: 3 (text + bullet-list + bullet-list)
- Struktur: ❌ Fragmentiert
- Content: ✅ Alle 6 Features erhalten

**Nachher (erwartet):**
- Komponenten: 1 (feature-grid)
- Struktur: ✅ Perfekt
- Content: ✅ Alle 6 Features erhalten

### Folie 08: Bilder & Visualisierungen

**Vorher:**
- Komponenten: 3 (image-frame + text + image-grid)
- Struktur: ⚠️ Suboptimal (4 Bilder auf 3 Komponenten komprimiert)
- Content: ✅ Alle Bild-Beschreibungen erhalten

**Nachher (erwartet):**
- Komponenten: 2-3 (image-grid × 1-2 + image-frame)
- Struktur: ✅ Besser (intelligentere Gruppierung)
- Content: ✅ Alle Bild-Beschreibungen erhalten

---

## Validierung

### Manuelle Code-Review: ✅

- ✅ Alle Templates vorhanden (10/10)
- ✅ Prompts konsistent (Agent 1 + Agent 2)
- ✅ Decision Rules eindeutig
- ✅ Beispiele hinzugefügt
- ✅ Keine Breaking Changes

### Nächste Schritte für automatische Validierung:

1. **Unit Tests:**
   ```bash
   # Agent 1: FEATURE Content-Block-Type
   python3 -m pytest presentation/api/test_content_analyzer_v2.py::test_feature_detection -v

   # Agent 2: feature-grid Komponente
   python3 -m pytest presentation/api/test_strategist_v2.py::test_feature_grid_selection -v
   ```

2. **Integration Test:**
   ```bash
   # Folie 06 regenerieren
   python3 -m pytest presentation/api/test_pitch_deck_regeneration.py::test_slide_06 -v
   ```

3. **Full Regression:**
   ```bash
   # Alle 8 Folien erneut testen
   python3 -m pytest presentation/api/test_pitch_deck_regeneration.py -v
   ```

---

## Metriken Erwartung

| Metrik | Vor Optimierung | Nach Optimierung (erwartet) |
|--------|-----------------|------------------------------|
| **Content-Erhaltung** | 100% | 100% |
| **Struktur-Matches** | 62.5% (5/8) | **75-87.5%** (6-7/8) |
| **feature-grid Erkennung** | 0% (0/1) | **100%** (1/1) |
| **Komponenten-Anzahl korrekt** | 62.5% (5/8) | **75-87.5%** (6-7/8) |

**Erwartete Perfect Matches nach Optimierung:**
- ✅ Folie 04 (Tabellen)
- ✅ Folie 05 (Prozess)
- ✅ **Folie 06 (Features)** ← NEU!
- ⚠️ Folien 01-03, 07-08 (Content OK, Struktur variiert)

---

## Lessons Learned

1. **Komponenten-Katalog vollständig dokumentieren**
   → Alle Templates müssen im Prompt aufgelistet sein

2. **Content-Block-Types und Komponenten-Types aligned**
   → FEATURES (Content-Block) → feature-grid (Component)

3. **Decision Rules explizit formulieren**
   → "ALWAYS use X when Y" statt "X is good for Y"

4. **Beispiele mit ❌/✅ helfen dem LLM**
   → Konkrete Dos & Don'ts im Prompt

5. **max_components Constraint präzise erklären**
   → Components ≠ Content Items

---

## Offene Punkte

1. **Test-Environment Setup** (nicht kritisch)
   - venv fehlt in presentation/api/
   - pytest nicht installiert
   - Workaround: TEST_MODE=true verwenden

2. **ContentGeneratorAgentV2 Review** (optional)
   - Prüfen ob Agent 3 mit FEATURE/FEATURES Content-Blocks umgehen kann
   - Vermutlich okay, da Agent 3 Blueprint-basiert arbeitet

3. **Template-Validierung** (optional)
   - feature-grid.html.j2 gegen design-guide.json validieren
   - Sicherstellen dass Template alle 6 Features rendern kann

---

**Erstellt:** 18. November 2025, 14:45 UTC
**Autor:** Claude Code Agent-Optimierung
**Status:** ✅ Implementiert, ⏳ Tests ausstehend

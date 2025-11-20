# Teleport Multi-Session Workflow - Ausführliche Anleitung

## 📖 Übersicht

Dieses Dokument erklärt, wie Sie **2 oder mehr parallele Web-Entwicklungen** (claude.ai/code Sessions) effizient lokal testen und mergen.

**Problem:** Sie haben mehrere Features parallel im Web entwickelt und müssen diese in die lokale Codebasis integrieren.

**Lösung:** Teleport + Agent + Strategische Merge-Reihenfolge

---

## 🎯 Kernkonzepte

### Session vs. Branch

**Session (Web):**
- Eine Konversation in claude.ai/code
- Enthält Code-Änderungen, Commits, Kontext
- Identifiziert durch Session-ID: `session_xxx`

**Branch (Git):**
- Feature-Branch auf GitHub
- Enthält die Commits aus der Session
- Beispiel: `claude/multi-provider-abc`

**Zusammenhang:**
```
Session (claude.ai/code)
    ↓ (pusht zu)
Branch (GitHub: claude/xyz)
    ↓ (teleport + agent testet)
Local Branch (nach Merge)
    ↓ (push zu)
Master (GitHub)
```

---

## 🔄 Die 4 Merge-Strategien

### Strategie 1: Sequential (Nacheinander)

**Wann nutzen:** Standard-Fall, unterschiedlich große Features

```
Session 1 → Teleport → Agent → Merge → Master Update
    ↓
Session 2 → Teleport → Agent → Merge → Master Update
    ↓
Session 3 → Teleport → Agent → Merge → Master Update
```

**Vorteile:**
- ✅ Einfach zu verfolgen
- ✅ Jeder Merge auf aktuellem Master
- ✅ Konflikte isoliert
- ✅ Bei Problemen nur eine Session betroffen

**Nachteile:**
- ⏱️ Langsamer (sequential)
- 🔄 Viele Master-Updates

---

### Strategie 2: Parallel (Alle testen, dann mergen)

**Wann nutzen:** Viele kleine, unabhängige Features

```
Session 1 → Teleport → Agent (Test Only)
Session 2 → Teleport → Agent (Test Only)
Session 3 → Teleport → Agent (Test Only)
    ↓ (Alle Tests OK?)
Merge Session 1 → Merge Session 2 → Merge Session 3
```

**Vorteile:**
- ⚡ Schneller (parallel testen)
- 🎯 Übersicht über alle Features
- 📊 Vergleich möglich

**Nachteile:**
- ⚠️ Konflikte erst beim Merge sichtbar
- 🔄 Master-State ändert sich während Merges
- 🧪 Tests basieren auf altem Master

---

### Strategie 3: Grouped (Gruppiert nach Abhängigkeiten)

**Wann nutzen:** Features mit Abhängigkeiten

```
Gruppe 1 (Foundation):
    Session A (API-Changes) → Merge
    ↓ (Master Update)

Gruppe 2 (Dependent Features):
    Session B (Uses API) → Merge
    Session C (Uses API) → Merge
    ↓ (Master Update)

Gruppe 3 (Independent):
    Session D (Frontend-Only) → Merge
```

**Vorteile:**
- 🏗️ Respektiert Abhängigkeiten
- ✅ Foundation zuerst
- 🎯 Logische Gruppierung

**Nachteile:**
- 🧠 Erfordert Analyse der Abhängigkeiten
- ⏱️ Langsamer durch Gruppierung

---

### Strategie 4: Hybrid (Kombiniert)

**Wann nutzen:** Mix aus großen und kleinen Features

```
Session 1 (Groß, 50 Files) → Sofort: Teleport → Agent → Merge
    ↓ (Master Update)

Sessions 2-5 (Klein) → Parallel testen
    ↓ (Alle Tests OK)
    → Sequential Merge
```

**Vorteile:**
- ⚡ Beste Balance
- 🎯 Flexibel
- ✅ Große Features isoliert

**Nachteile:**
- 🧠 Erfordert Entscheidung welche Strategie pro Feature

---

## 📊 Branch-Priorisierung: Welcher zuerst?

### Entscheidungsmatrix

| Kriterium | Gewichtung | Beschreibung |
|-----------|-----------|--------------|
| **Größe** | ⭐⭐⭐⭐⭐ | Files geändert, Lines added |
| **Abhängigkeiten** | ⭐⭐⭐⭐ | Andere Features bauen darauf |
| **Konfliktpotenzial** | ⭐⭐⭐ | Ändert kritische Files |
| **Kritikalität** | ⭐⭐ | Business-Wert |

### Regel 1: Größe

**Prinzip:** Größter Branch zuerst

**Grund:** Kleine Branches sind leichter anzupassen wenn Konflikte auftreten.

**Beispiel:**
```
Branch A: 42 Files, +5000 Lines
Branch B: 1 File, +50 Lines
Branch C: 8 Files, +800 Lines

Reihenfolge: A → C → B
```

---

### Regel 2: Abhängigkeiten

**Prinzip:** Foundation vor Features

**Beispiel:**
```
Branch A: API Agents (new endpoints)
Branch B: Frontend (uses new endpoints)

Reihenfolge: A → B (auch wenn B größer!)
```

**Abhängigkeits-Typen:**
- **Harte Abhängigkeit:** B kann ohne A nicht funktionieren
- **Weiche Abhängigkeit:** B nutzt A, aber funktioniert auch allein
- **Keine Abhängigkeit:** Unabhängige Features

---

### Regel 3: Konfliktpotenzial

**Prinzip:** Unabhängige Features vor konfliktträchtigen

**Konflikt-Indikatoren:**
```
⚠️ Hohe Konflikt-Wahrscheinlichkeit:
- Beide ändern unified-editor.html
- Beide ändern config.py
- Beide ändern orchestrator.py

✅ Niedrige Konflikt-Wahrscheinlichkeit:
- Ein Branch nur API, anderer nur Frontend
- Verschiedene Komponenten
- Komplett neue Files
```

**Strategie:**
1. Unabhängige Features zuerst mergen
2. Konfliktträchtige Features einzeln mit frischem Master testen

---

### Regel 4: Kritikalität

**Prinzip:** Wichtigste Features zuerst (aber untergeordnet zu Größe/Abhängigkeiten)

**Kritikalitäts-Level:**
- 🔴 **Critical:** Production-Bugfix, Security
- 🟡 **High:** Wichtiges neues Feature
- 🟢 **Normal:** Erweiterung, Verbesserung
- ⚪ **Low:** Nice-to-have, Experimental

---

## 🛠️ Praktische Szenarien

### Szenario 1: 2 Sessions (einfach)

**Situation:**
```
Session 1: claude/multi-provider-abc (API + Frontend, 42 Files)
Session 2: claude/fullscreen-xyz (Frontend only, 1 File)
```

**Analyse:**
- Session 1: Größer, ändert mehr
- Session 2: Kleiner, nur Frontend
- Konflikt-Potenzial: Mittel (beide ändern unified-editor.html)

**Entscheidung:** Sequential, Session 1 zuerst

**Workflow:**
```bash
# === Session 1 ===
claude --teleport session_1

# In Desktop:
@agent web-to-local-sync-tester {
  "remote_branch": "claude/multi-provider-abc",
  "test_scope": "full"
}
# → ✅ Merge-Ready

git checkout master
git merge claude/multi-provider-abc
git push origin master

# === Session 2 ===
git checkout master
git pull origin master  # Holt Session 1 Merge

claude --teleport session_2

# In Desktop:
@agent web-to-local-sync-tester {
  "remote_branch": "claude/fullscreen-xyz",
  "local_branch": "master",  # Aktualisiert!
  "test_scope": "full"
}
# → ⚠️ Konflikt in unified-editor.html
# → Agent zeigt: Kombinieren Sie Model Selector (Session 1) + Fullscreen (Session 2)

# Konflikt manuell lösen (siehe GIT_WORKFLOW_GUIDE.md)
git checkout claude/fullscreen-xyz
git merge master
# ... Konflikt in unified-editor.html lösen ...
git add unified-editor.html
git commit -m "Merge master: Combine multi-provider + fullscreen"
git push origin claude/fullscreen-xyz

# PR erstellen & mergen
gh pr create --title "Fullscreen Mode" --base master
# → Auf GitHub mergen
```

---

### Szenario 2: 3 Sessions (komplex)

**Situation:**
```
Session 1: claude/api-redesign (API only, 25 Files)
Session 2: claude/frontend-update (Frontend only, 15 Files)
Session 3: claude/docs-update (Docs only, 10 Files)
```

**Analyse:**
- Session 1: API (Foundation)
- Session 2: Frontend (nutzt Session 1 potentiell)
- Session 3: Docs (unabhängig)
- Konflikt-Potenzial: Niedrig (verschiedene Bereiche)

**Entscheidung:** Grouped Strategy

**Workflow:**
```bash
# === Gruppe 1: Foundation (API) ===
claude --teleport session_1
@agent web-to-local-sync-tester {
  "remote_branch": "claude/api-redesign",
  "test_scope": "api-only"
}
# → ✅ Merge
git merge claude/api-redesign

# === Gruppe 2: Dependent Features (parallel testen) ===
git checkout master && git pull

# Test Frontend (uses updated API)
claude --teleport session_2
@agent web-to-local-sync-tester {
  "remote_branch": "claude/frontend-update",
  "test_scope": "full"  # Full weil API sich geändert hat
}
# → ✅ Merge

# Test Docs (independent)
claude --teleport session_3
@agent web-to-local-sync-tester {
  "remote_branch": "claude/docs-update",
  "test_scope": "quick"  # Quick weil nur Docs
}
# → ✅ Merge

# Merges durchführen
git merge claude/frontend-update
git push origin master
git checkout master && git pull
git merge claude/docs-update
git push origin master
```

---

### Szenario 3: 5+ Sessions (sehr komplex)

**Situation:**
```
Session 1: claude/anthropic-agents (20 Files, API)
Session 2: claude/google-agents (18 Files, API)
Session 3: claude/orchestrator-v2 (5 Files, API)
Session 4: claude/model-selector (1 File, Frontend)
Session 5: claude/shared-themes (12 Files, Styles)
Session 6: claude/docs-reorg (30 Files, Docs)
```

**Analyse:**

| Session | Files | Bereich | Abhängigkeiten | Konflikt | Priorität |
|---------|-------|---------|----------------|----------|-----------|
| 1 | 20 | API | Foundation | Mittel | 1 |
| 2 | 18 | API | Foundation | Mittel | 2 |
| 3 | 5 | API | Nutzt 1+2 | Niedrig | 3 |
| 4 | 1 | Frontend | Nutzt 3 | Niedrig | 4 |
| 5 | 12 | Styles | Unabhängig | Niedrig | 5 |
| 6 | 30 | Docs | Unabhängig | Niedrig | 6 |

**Entscheidung:** Hybrid Strategy (Foundation Sequential, Rest Parallel)

**Workflow:**
```bash
# === Phase 1: Foundation (Sequential) ===

# Session 1 (Anthropic Agents)
claude --teleport session_1
@agent web-to-local-sync-tester {...}
# → ✅ Merge

# Session 2 (Google Agents)
git checkout master && git pull
claude --teleport session_2
@agent web-to-local-sync-tester {...}
# → ✅ Merge

# Session 3 (Orchestrator - depends on 1+2)
git checkout master && git pull
claude --teleport session_3
@agent web-to-local-sync-tester {...}
# → ✅ Merge

# === Phase 2: Dependent Features (Parallel Test) ===

# Session 4 (Model Selector - depends on Orchestrator)
git checkout master && git pull
claude --teleport session_4
@agent web-to-local-sync-tester {...}
# → ✅

# === Phase 3: Independent (Parallel Test) ===

# Session 5 (Shared Themes)
claude --teleport session_5
@agent web-to-local-sync-tester {...}
# → ✅

# Session 6 (Docs)
claude --teleport session_6
@agent web-to-local-sync-tester {...}
# → ✅

# === Phase 4: Sequential Merge ===
git merge claude/model-selector
git push && git pull
git merge claude/shared-themes
git push && git pull
git merge claude/docs-reorg
git push
```

**Zeitersparnis:**
- Sequenti (ohne Parallel-Test): ~60 Minuten
- Hybrid (mit Parallel-Test): ~35 Minuten
- **Ersparnis: 40%**

---

## 🚨 Konflikt-Minimierung

### Strategie 1: File-basierte Analyse

**Vor Teleport:** Analysieren Sie welche Files geändert wurden

```bash
# Für jeden Branch:
git fetch origin
git diff master origin/claude/branch-name --name-only

# Output für Session 1:
# presentation/unified-editor.html
# presentation/api/config.py

# Output für Session 2:
# presentation/unified-editor.html
# presentation/api/main.py
```

**⚠️ Konflikt-Indikator:** Beide ändern `unified-editor.html`

**Lösung:**
1. Größeren Branch zuerst mergen
2. Kleineren Branch gegen neuen Master testen
3. Konflikt manuell lösen (Agent zeigt Details)

---

### Strategie 2: Component-Isolation

**Prinzip:** Features die verschiedene Components ändern → unabhängig

**Beispiel:**
```
Session 1: Ändert stat-grid.html.j2
Session 2: Ändert bullet-list.html.j2
Session 3: Ändert table.html.j2

→ Kein Konflikt! Parallel mergebar
```

---

### Strategie 3: Master-First Policy

**Regel:** Immer gegen aktuellsten Master testen

```bash
# ❌ FALSCH:
@agent web-to-local-sync-tester {
  "local_branch": "master"  # Alter Master!
}

# ✅ RICHTIG:
git checkout master
git pull origin master  # Aktualisieren!
@agent web-to-local-sync-tester {
  "local_branch": "master"  # Frischer Master
}
```

---

## 📋 Checklisten

### Vor Multi-Session Merge

- [ ] Alle Web-Sessions fertig entwickelt
- [ ] Alle Branches gepusht zu GitHub
- [ ] Session-IDs notiert
- [ ] Branch-Namen dokumentiert
- [ ] Master lokal aktuell (`git pull origin master`)

---

### Pro Session

- [ ] Session teleportiert
- [ ] Agent aufgerufen (mit aktuellem local_branch)
- [ ] Report gelesen
- [ ] Entscheidung getroffen (Merge/Fix/Resolve)
- [ ] Bei ✅: Gemerged
- [ ] Bei ❌: Fixes implementiert
- [ ] Bei ⚠️: Konflikte gelöst
- [ ] Master aktualisiert (`git checkout master && git pull`)

---

### Nach allen Merges

- [ ] Alle Features auf Master
- [ ] Alle Branches gelöscht (lokal & remote)
- [ ] Tests laufen (`pytest presentation/api/tests/`)
- [ ] Frontend funktioniert (unified-editor.html)
- [ ] Dokumentation aktualisiert

---

## 🎓 Best Practices

### 1. Session-Tracking Sheet

**Problem:** Bei 5+ Sessions den Überblick verlieren

**Lösung:** Einfaches Tracking-Sheet

```markdown
# Multi-Session Merge - 2025-01-20

| # | Session ID | Branch | Files | Status | Notes |
|---|-----------|--------|-------|--------|-------|
| 1 | session_aaa | claude/multi-provider | 42 | ✅ Merged | No conflicts |
| 2 | session_bbb | claude/fullscreen | 1 | ⚠️ Conflict | unified-editor.html |
| 3 | session_ccc | claude/docs | 30 | ⏳ Pending | Test after #2 |
```

---

### 2. Batch-Testing Script

**Problem:** Gleichen Agent-Befehl mehrmals tippen

**Lösung:** Agent-Aufrufe dokumentieren

```markdown
# Agent-Calls für heute:

## Session 1
@agent web-to-local-sync-tester {
  "remote_branch": "claude/multi-provider-abc",
  "test_scope": "full"
}

## Session 2
@agent web-to-local-sync-tester {
  "remote_branch": "claude/fullscreen-xyz",
  "test_scope": "full"
}

## Session 3
@agent web-to-local-sync-tester {
  "remote_branch": "claude/docs-update",
  "test_scope": "quick"
}
```

**→ Copy-Paste in Desktop nach jedem Teleport**

---

### 3. Master-State Documentation

**Problem:** Nach mehreren Merges vergessen, was schon drin ist

**Lösung:** Commit-Message als Referenz

```bash
git log --oneline -10

# Shows:
# abc123 Merge claude/multi-provider ← Session 1
# def456 Merge claude/fullscreen ← Session 2
# ghi789 Merge claude/docs ← Session 3
```

---

## 🔧 Troubleshooting

### Problem 1: Session teleportiert, aber Branch nicht gefunden

**Symptom:**
```
@agent web-to-local-sync-tester {
  "remote_branch": "claude/xyz"
}
→ ❌ Error: Branch not found
```

**Ursache:** Branch noch nicht gepusht von Web-Session

**Lösung:**
```bash
# Check ob Branch existiert
git fetch origin
git branch -r | grep claude/xyz

# Falls nicht: Zurück zu Web-Session, pushen
# Dann erneut teleportieren
```

---

### Problem 2: Tests schlagen nach Teleport fehl

**Symptom:**
```
@agent → ❌ Tests: 15 failed
```

**Ursache:** Lokale Dependencies unterschiedlich zu Web

**Lösung:**
```bash
cd presentation/api
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Dann Agent erneut aufrufen
@agent web-to-local-sync-tester {...}
```

---

### Problem 3: Zu viele Sessions, keine klare Reihenfolge

**Symptom:** Unsicher, welche Session zuerst

**Lösung:** Entscheidungsmatrix nutzen

```
1. Größe zählen:
   git diff master origin/branch --shortstat

2. Dependencies prüfen:
   - Ändert Branch API? → Foundation
   - Nutzt Branch andere Features? → Later

3. Konflikte checken:
   git diff master origin/branch-a | grep "+++" > a.txt
   git diff master origin/branch-b | grep "+++" > b.txt
   comm -12 a.txt b.txt  # Gemeinsame Files

4. Entscheidung dokumentieren (siehe Tracking Sheet)
```

---

## 📊 Metriken & Optimierung

### Zeitaufwand messen

```
Session Count | Sequential | Parallel Test | Hybrid | Savings
    2         |  15 min    |  12 min       | 12 min | 20%
    3         |  25 min    |  18 min       | 15 min | 40%
    5         |  50 min    |  35 min       | 25 min | 50%
   10         | 100 min    |  70 min       | 40 min | 60%
```

**Empfehlung:**
- 2-3 Sessions: Sequential OK
- 4-6 Sessions: Hybrid empfohlen
- 7+ Sessions: Grouped + Parallel

---

## ✅ Zusammenfassung

### Kern-Workflow

1. **Priorisieren:** Größe → Abhängigkeiten → Konflikte → Kritikalität
2. **Teleportieren:** Session für Session
3. **Testen:** Agent mit aktuellem Master
4. **Mergen:** Sequential oder Grouped
5. **Aktualisieren:** Master zwischen Sessions

### Die 4 Strategien

- **Sequential:** Standard, einfach, sicher
- **Parallel:** Schnell, viele kleine Features
- **Grouped:** Respektiert Abhängigkeiten
- **Hybrid:** Beste Balance, Mix aus groß/klein

### Best Practices

✅ Session-Tracking Sheet nutzen
✅ Master zwischen Sessions aktualisieren
✅ Größte Features zuerst
✅ Konflikte früh erkennen (File-Analyse)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

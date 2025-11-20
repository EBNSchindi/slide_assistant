# Web-zu-Lokal Integration & Testing Agent

## Übersicht

Dieser Agent automatisiert den Workflow für das Zusammenführen von Web-Entwicklung (claude.ai/code) mit der lokalen Entwicklungsumgebung.

**Zweck:** Synchronisiere, teste und validiere Web-entwickelte Features vor dem Merge in den lokalen Branch.

---

## Agent-Funktionen

### Phase 1: Sync & Analyse 🔍
- Remote-Branch von GitHub fetchen
- Commit-Historie analysieren
- Geänderte Dateien auflisten
- Diffs anzeigen (mit Konflikt-Erkennung)
- Branch-Divergenz berechnen

### Phase 2: Lokales Testing 🧪
- **API-Tests:** pytest mit allen relevanten Tests
- **Frontend-Tests:** unified-editor.html Funktionalität prüfen
- **Integration-Tests:** Beide Features zusammen testen
- **Fehler dokumentieren:** Alle Fehler mit Stack-Traces

### Phase 3: Merge-Entscheidung 🎯
- ✅ **Tests erfolgreich** → Merge-Empfehlung mit Schritten
- ❌ **Tests fehlgeschlagen** → Fehler auflisten + Fix-Vorschläge
- ⚠️ **Konflikte erkannt** → Konfliktbereiche zeigen + Lösungsansätze

### Phase 4: Report 📊
- Änderungen zusammenfassen (Files, Lines, Commits)
- Test-Status (Passed/Failed/Skipped)
- Nächste Schritte (Merge-Befehle oder Fix-Anweisungen)
- Empfehlung: Merge-Ready oder Fixes benötigt

---

## Agent-Aufruf in Claude Code

### Syntax

```
@agent web-to-local-sync-tester {
  "remote_branch": "claude/feature-name-xyz",
  "local_branch": "master",
  "test_scope": "full"
}
```

### Parameter

| Parameter | Typ | Default | Beschreibung |
|-----------|-----|---------|--------------|
| `remote_branch` | string | **REQUIRED** | Name des Remote-Branches (z.B. `claude/multi-provider-xyz`) |
| `local_branch` | string | `master` | Ziel-Branch für Merge (meist `master`) |
| `test_scope` | string | `full` | Test-Umfang: `full`, `quick`, `api-only`, `frontend-only` |

### Test Scopes

#### `full` (Standard)
- Alle API-Tests (`pytest presentation/api/tests/`)
- Frontend-Validierung (unified-editor.html prüfen)
- Integration-Tests
- Konflikt-Analyse
- **Dauer:** ~5-10 Minuten

#### `quick`
- Nur kritische Tests
- Syntax-Check
- Import-Validierung
- **Dauer:** ~1-2 Minuten

#### `api-only`
- Nur Backend-Tests
- pytest mit relevanten Test-Files
- Keine Frontend-Prüfung
- **Dauer:** ~3-5 Minuten

#### `frontend-only`
- Nur HTML/CSS/JS Validierung
- unified-editor.html Syntax-Check
- Keine API-Tests
- **Dauer:** ~1-2 Minuten

---

## Beispiele

### Beispiel 1: Vollständiger Test eines Features

**Szenario:** Web-entwickeltes Multi-Provider Feature lokal testen

```
Ich habe im Web an Branch "claude/attempt-n-013a8hfTz3c5TBaWGAezwxDR"
entwickelt. Teste diesen Branch vollständig bevor ich merge.

@agent web-to-local-sync-tester {
  "remote_branch": "claude/attempt-n-013a8hfTz3c5TBaWGAezwxDR",
  "local_branch": "master",
  "test_scope": "full"
}
```

**Agent-Ablauf:**
1. ✅ Fetcht Remote-Branch
2. 📊 Zeigt 12 Commits, 43 Files geändert
3. 🧪 Führt alle Tests aus (pytest + Frontend)
4. ✅ Tests erfolgreich (35 passed, 0 failed)
5. 📝 Empfiehlt: "Merge-Ready! Nutzen Sie diese Befehle..."

---

### Beispiel 2: Quick Check vor dem Merge

**Szenario:** Schnelle Validierung eines kleinen Features

```
Schneller Check für Fullscreen-Feature bevor ich merge.

@agent web-to-local-sync-tester {
  "remote_branch": "claude/fullscreen-display-window-xyz",
  "local_branch": "master",
  "test_scope": "quick"
}
```

**Agent-Ablauf:**
1. ✅ Fetcht Branch
2. 📊 Zeigt 2 Commits, 1 File geändert
3. 🧪 Quick-Tests (Syntax, Imports)
4. ✅ Keine Fehler gefunden
5. 📝 Empfiehlt: "Sieht gut aus, aber full Test empfohlen für Production"

---

### Beispiel 3: Nur API-Tests (Backend-Änderungen)

**Szenario:** Neue Agents hinzugefügt, nur Backend testen

```
Teste neue Anthropic Agents, Frontend ist unverändert.

@agent web-to-local-sync-tester {
  "remote_branch": "claude/anthropic-agents-abc",
  "test_scope": "api-only"
}
```

**Agent-Ablauf:**
1. ✅ Fetcht Branch
2. 📊 Zeigt 6 neue .py Files in agents/
3. 🧪 pytest auf presentation/api/tests/
4. ❌ 2 Tests fehlgeschlagen (test_anthropic_agents.py)
5. 📝 Listet Fehler auf + schlägt Fixes vor

---

### Beispiel 4: Konflikt-Erkennung

**Szenario:** Zwei parallele Features, Konflikte erwartet

```
Beide Branches ändern unified-editor.html. Analysiere Konflikte.

@agent web-to-local-sync-tester {
  "remote_branch": "claude/model-selector-xyz",
  "local_branch": "claude/fullscreen-feature-abc",
  "test_scope": "full"
}
```

**Agent-Ablauf:**
1. ✅ Fetcht beide Branches
2. ⚠️ Konflikt erkannt in unified-editor.html (Zeile 1200-1350)
3. 📊 Zeigt Konfliktbereiche mit Diff
4. 💡 Schlägt vor: "Beide Features kombinieren - Model Selector + Fullscreen"
5. 📝 Gibt Schritt-für-Schritt Konflikt-Resolution

---

## Agent-Output-Format

### Erfolgreicher Test (✅ Merge-Ready)

```markdown
# 🎯 Web-to-Local Sync Report

## Branch Info
- **Remote Branch:** claude/feature-xyz
- **Local Branch:** master
- **Test Scope:** full

## Changes Summary
- **Commits:** 8 ahead of master
- **Files Changed:** 23 (15 new, 7 modified, 1 deleted)
- **Lines:** +1,234 / -156

## Test Results
✅ API Tests: 28 passed, 0 failed
✅ Frontend Tests: Syntax OK, no errors
✅ Integration Tests: All passed

## Conflict Analysis
✅ No conflicts detected

## Recommendation: ✅ MERGE READY

### Merge Commands:
```bash
git checkout master
git pull origin master
git merge claude/feature-xyz
# Auto-merge successful (no conflicts expected)
git push origin master
```

### Post-Merge Verification:
- [ ] Run API server: `python3 run_api.py`
- [ ] Open unified-editor.html
- [ ] Test new feature manually
```

---

### Fehlgeschlagener Test (❌ Fixes Needed)

```markdown
# 🎯 Web-to-Local Sync Report

## Branch Info
- **Remote Branch:** claude/new-feature-xyz
- **Local Branch:** master
- **Test Scope:** full

## Changes Summary
- **Commits:** 5 ahead of master
- **Files Changed:** 12

## Test Results
❌ API Tests: 18 passed, 3 failed
✅ Frontend Tests: OK

## Failed Tests

### 1. test_anthropic_agents.py::test_content_analyzer
**Error:** `ModuleNotFoundError: No module named 'anthropic'`
**Fix:** Add `anthropic>=0.40.0` to presentation/api/requirements.txt

### 2. test_orchestrator_v2.py::test_provider_detection
**Error:** `AssertionError: Expected 'anthropic', got 'openai'`
**Fix:** Update model-to-provider mapping in config.py

### 3. test_v2_integration.py::test_full_pipeline
**Error:** `KeyError: 'model'`
**Fix:** Add model parameter to GenerateRequest schema

## Recommendation: ❌ FIXES NEEDED

### Required Actions:
1. Install missing dependency: `pip install anthropic>=0.40.0`
2. Fix provider detection logic in config.py
3. Update request schema in models/requests.py
4. Re-run tests: `pytest presentation/api/tests/ -v`
5. Then merge when tests pass
```

---

### Konflikt erkannt (⚠️ Manual Resolution)

```markdown
# 🎯 Web-to-Local Sync Report

## Branch Info
- **Remote Branch:** claude/feature-a
- **Local Branch:** claude/feature-b
- **Test Scope:** full

## Changes Summary
- **Branch A:** 3 commits, 1 file (unified-editor.html)
- **Branch B:** 2 commits, 1 file (unified-editor.html)

## Conflict Analysis
⚠️ **CONFLICT DETECTED** in presentation/unified-editor.html

### Conflict Areas:

#### Conflict 1: Lines 1200-1250 (Header Controls)
**Feature A adds:** Model Selector Dropdown
**Feature B adds:** Fullscreen Button

**Resolution Strategy:** COMBINE both (dropdown + button)

```html
<!-- Combine both features -->
<select id="modelSelect">...</select>  <!-- From Feature A -->
<button id="fullscreenBtn">...</button>  <!-- From Feature B -->
```

#### Conflict 2: Lines 1300-1350 (Preview Panel)
**Feature A adds:** Provider Badge
**Feature B adds:** Fullscreen Controls

**Resolution Strategy:** COMBINE both in same panel

## Recommendation: ⚠️ MANUAL MERGE REQUIRED

### Manual Resolution Steps:
1. Merge Feature A first (larger changeset)
   ```bash
   git checkout master
   git merge claude/feature-a
   git push origin master
   ```

2. Then merge Feature B (will conflict)
   ```bash
   git checkout claude/feature-b
   git merge master
   # CONFLICT in unified-editor.html
   ```

3. Resolve conflicts manually:
   - Open presentation/unified-editor.html
   - Find conflict markers (<<<<<<<, =======, >>>>>>>)
   - Combine both features (see examples above)
   - Test combined version

4. Complete merge:
   ```bash
   git add presentation/unified-editor.html
   git commit -m "Merge master: Combine feature-a + feature-b"
   git push origin claude/feature-b
   ```

See GIT_WORKFLOW_GUIDE.md section "Konflikt-Resolution" for details.
```

---

## Integration mit Ihrem Workflow

### Typischer Workflow

```
┌─────────────────────────────────────────────────────┐
│ 1. Web-Entwicklung (claude.ai/code)                │
│    → Feature entwickelt                             │
│    → Branch: claude/feature-xyz                     │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 2. Lokal: Agent testen lassen                       │
│    @agent web-to-local-sync-tester {                │
│      "remote_branch": "claude/feature-xyz",         │
│      "test_scope": "full"                           │
│    }                                                │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ 3a. Tests OK ✅                                      │
│     → Agent gibt Merge-Befehle                      │
│     → Befehle ausführen                             │
│     → PR erstellen                                  │
└─────────────────────────────────────────────────────┘
                    OR
┌─────────────────────────────────────────────────────┐
│ 3b. Tests Failed ❌                                  │
│     → Agent listet Fehler auf                       │
│     → Fixes lokal implementieren                    │
│     → Tests erneut laufen lassen                    │
└─────────────────────────────────────────────────────┘
                    OR
┌─────────────────────────────────────────────────────┐
│ 3c. Konflikte ⚠️                                     │
│     → Agent zeigt Konfliktbereiche                  │
│     → Manuelle Resolution (siehe Guide)             │
│     → Tests nach Resolution                         │
└─────────────────────────────────────────────────────┘
```

---

## Erweiterte Features

### Auto-Fix Vorschläge

Wenn Tests fehlschlagen, schlägt der Agent automatisch Fixes vor:

**Beispiel:** Missing Dependency
```
❌ ModuleNotFoundError: No module named 'anthropic'

💡 Auto-Fix Suggestion:
1. Add to presentation/api/requirements.txt:
   anthropic>=0.40.0

2. Install:
   cd presentation/api
   source venv/bin/activate
   pip install -r requirements.txt

3. Re-test:
   @agent web-to-local-sync-tester {
     "remote_branch": "claude/feature-xyz",
     "test_scope": "api-only"
   }
```

---

### Parallel-Branch Testing

Teste mehrere Web-Branches gleichzeitig:

```
Ich habe 3 Features im Web entwickelt. Teste alle:

@agent web-to-local-sync-tester {
  "remote_branch": "claude/feature-1",
  "test_scope": "quick"
}

@agent web-to-local-sync-tester {
  "remote_branch": "claude/feature-2",
  "test_scope": "quick"
}

@agent web-to-local-sync-tester {
  "remote_branch": "claude/feature-3",
  "test_scope": "quick"
}
```

**Agent erstellt Vergleichstabelle:**

| Branch | Commits | Files | Tests | Conflicts | Status |
|--------|---------|-------|-------|-----------|--------|
| feature-1 | 5 | 12 | ✅ All Pass | ✅ None | Merge-Ready |
| feature-2 | 3 | 6 | ⚠️ 1 Skip | ✅ None | Check skipped test |
| feature-3 | 8 | 23 | ❌ 2 Fail | ⚠️ Yes | Needs fixes |

**Empfehlung:** Merge feature-1 zuerst, dann feature-2, dann feature-3 nach Fixes.

---

## Teleport Integration (Bevorzugte Methode) 🚀

### Was ist Teleport?

**Teleport** überträgt Ihre Web-Session (claude.ai/code) nahtlos zu Claude Code Desktop.

**Workflow:**
1. Feature in claude.ai/code entwickeln
2. **Teleport-Befehl** erhalten: `claude --teleport session_xxx`
3. Session in Desktop laden (mit vollständigem Kontext!)
4. Agent direkt aufrufen (kein Kontext-Verlust)

### Warum Teleport + Agent?

**Ohne Teleport:**
```
Web-Entwicklung → Lokal: Branch manuell fetchen
→ Kontext fehlt → Tests manuell → Merge unsicher
```

**Mit Teleport + Agent:** ✅
```
Web-Entwicklung → Teleport (Kontext erhalten!)
→ Agent automatisch testen → Klare Empfehlung
```

### Teleport-Workflow

#### Schritt 1: Im Web entwickeln

```
In claude.ai/code:
1. Feature entwickeln
2. Branch pushen: git push origin claude/feature-xyz
3. Teleport-Befehl kopieren:
   claude --teleport session_014KZZLRj1jWZvTfp2HMt6rq
```

#### Schritt 2: Session teleportieren

```bash
# Lokales Terminal
cd /path/to/slide_assistant
claude --teleport session_014KZZLRj1jWZvTfp2HMt6rq
```

**→ Claude Code Desktop öffnet sich mit Session**

#### Schritt 3: Agent aufrufen

```
In Desktop-Session (nach Teleport):

@agent web-to-local-sync-tester {
  "remote_branch": "claude/feature-xyz",
  "test_scope": "full"
}
```

**→ Agent testet Branch mit vollem Kontext**

### Multi-Session Management (2+ Web-Entwicklungen)

**Problem:** Sie haben 3+ Features parallel im Web entwickelt.

**Lösung:** Sequential Teleport + Agent

```
Session 1 (Größter Branch)
    ↓ Teleport
    → Agent testet
    → ✅ Merge
    → Master Update

Session 2 (Mittlerer Branch)
    ↓ Teleport
    → Agent testet (gegen NEUEN Master!)
    → ✅ Merge
    → Master Update

Session 3 (Kleinster Branch)
    ↓ Teleport
    → Agent testet
    → ✅ Merge
```

**Wichtig:**
- ✅ **Größtes Feature zuerst** (weniger Konflikte später)
- ✅ **Master zwischen Sessions aktualisieren**
- ✅ **Agent gegen aktuellen Master** testen

### Priorisierung (2+ Sessions)

**Welche Session zuerst teleportieren?**

1. **Größe:** Größter Branch zuerst (42 Files vor 1 File)
2. **Abhängigkeiten:** Foundation vor Features (API vor Frontend)
3. **Konflikte:** Unabhängige vor konfliktträchtigen
4. **Kritikalität:** Wichtigste Features bevorzugen

**Beispiel:**
```
Session A: 42 Files (API + Frontend) → ZUERST
Session B: 1 File (Frontend only) → DANACH
Session C: 8 Files (Docs only) → ZULETZT
```

### Teleport + Agent: Vollständiges Beispiel

```
# === Web-Entwicklung (claude.ai/code) ===
# Feature: Multi-Provider LLM Support
# Branch: claude/multi-provider-abc
# Status: Fertig, gepusht
# Teleport-Befehl erhalten: claude --teleport session_xyz

# === Lokal: Session übertragen ===
cd ~/projects/slide_assistant
claude --teleport session_xyz

# Claude Code Desktop öffnet sich...

# === In Desktop: Agent aufrufen ===
@agent web-to-local-sync-tester {
  "remote_branch": "claude/multi-provider-abc",
  "test_scope": "full"
}

# === Agent-Report ===
✅ Tests: 35 passed, 0 failed
✅ No conflicts with master
✅ MERGE READY

Commands:
git checkout master
git merge claude/multi-provider-abc
git push origin master

# === Befehle ausführen ===
git checkout master
git merge claude/multi-provider-abc
git push origin master

# Fertig! ✅
```

### Weiterführende Docs

- **Quick Guide:** `TELEPORT_QUICK_GUIDE.md`
- **Multi-Session:** `TELEPORT_MULTI_SESSION_WORKFLOW.md`

---

## Trouble-Shooting

### Agent findet Remote-Branch nicht

**Problem:**
```
❌ Error: Remote branch 'claude/feature-xyz' not found
```

**Lösung:**
```bash
# Branch wurde vielleicht noch nicht gepusht?
git fetch origin --all
git branch -r | grep claude/

# Oder Tippfehler im Namen?
# Prüfen Sie auf GitHub: github.com/ihr-repo/branches
```

---

### Tests schlagen lokal fehl, aber im Web nicht

**Problem:**
```
❌ Tests fail locally but passed in claude.ai/code
```

**Mögliche Ursachen:**
1. **Dependencies unterschiedlich:** Web hat andere Package-Versionen
2. **Environment Variables:** .env fehlt lokal
3. **Python-Version:** Web nutzt Python 3.11, lokal 3.10

**Lösung:**
```bash
# 1. Dependencies aktualisieren
cd presentation/api
pip install -r requirements.txt --upgrade

# 2. .env prüfen
cat .env  # OPENAI_API_KEY gesetzt?

# 3. Python-Version prüfen
python3 --version
```

---

### Agent schlägt Merge vor, aber Sie sind unsicher

**Problem:**
```
✅ Agent sagt "Merge-Ready", aber ich bin skeptisch
```

**Lösung:**
```
# Zusätzliche manuelle Prüfung:

# 1. Diff anschauen
git fetch origin
git diff master origin/claude/feature-xyz

# 2. Spezifische Files prüfen
git show origin/claude/feature-xyz:presentation/unified-editor.html

# 3. Test-Coverage prüfen
cd presentation/api
pytest tests/ -v --cov=agents --cov-report=term

# 4. Frontend manuell testen
python3 run_api.py &
python3 -m http.server 8000
# Browser: http://localhost:8000/unified-editor.html
```

---

## Best Practices

### 1. Immer vor dem Merge testen

```bash
# ❌ NICHT TUN:
git merge claude/web-branch  # Ohne Test!

# ✅ RICHTIG:
# Erst Agent testen lassen, dann mergen
@agent web-to-local-sync-tester {...}
# Nur wenn ✅, dann mergen
```

---

### 2. Test Scope richtig wählen

- **Kleines Feature (1-2 Files):** `quick`
- **Backend-Only Änderungen:** `api-only`
- **Frontend-Only Änderungen:** `frontend-only`
- **Großes Feature (>5 Files):** `full`
- **Kritische Production-Änderungen:** `full`

---

### 3. Konflikte früh erkennen

```bash
# Teste gegen aktuellen master, nicht gegen alten
git fetch origin
git checkout master
git pull origin master

# Dann Agent aufrufen
@agent web-to-local-sync-tester {
  "remote_branch": "claude/feature",
  "local_branch": "master",  # Aktueller master!
  "test_scope": "full"
}
```

---

### 4. Dokumentiere Agent-Ergebnisse

```bash
# Agent-Report speichern für später
@agent web-to-local-sync-tester {...}

# Output in Datei speichern:
# Copy-Paste Agent-Output → SYNC_REPORT_2025-01-20.md
```

---

## Zusammenfassung

### Agent löst diese Probleme:

✅ **Manuelle Tests vergessen** → Agent testet automatisch
✅ **Konflikte zu spät erkannt** → Agent zeigt Konflikte VOR dem Merge
✅ **Unsicherheit beim Merge** → Agent gibt klare Empfehlung
✅ **Fehler erst nach Merge gefunden** → Agent testet VORHER
✅ **Keine klare Anleitung** → Agent gibt Schritt-für-Schritt Befehle

### Was der Agent NICHT kann:

❌ **Konflikte automatisch lösen** → Manuelle Resolution nötig
❌ **Code schreiben** → Nur Analyse & Empfehlungen
❌ **Automatisch mergen** → Sie entscheiden final

---

## Cheat Sheet

```bash
# Standard-Aufruf (Full Test)
@agent web-to-local-sync-tester {
  "remote_branch": "claude/xyz",
  "test_scope": "full"
}

# Quick Check
@agent web-to-local-sync-tester {
  "remote_branch": "claude/xyz",
  "test_scope": "quick"
}

# Nur API-Tests
@agent web-to-local-sync-tester {
  "remote_branch": "claude/xyz",
  "test_scope": "api-only"
}

# Custom local branch
@agent web-to-local-sync-tester {
  "remote_branch": "claude/xyz",
  "local_branch": "develop",
  "test_scope": "full"
}
```

---

**Autor:** Claude Code
**Version:** 1.0
**Datum:** 2025-01-20
**Lizenz:** Internal Use

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

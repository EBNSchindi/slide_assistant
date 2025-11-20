# Web-to-Local Sync Agent - Quick Start

## 🚀 Empfohlener Workflow: Teleport + Agent

**NEU:** Der bevorzugte Weg ist jetzt **Teleport** + **Agent** - nahtlos von Web zu Lokal!

### Schnellstart (4 Schritte)

```bash
# 1. In claude.ai/code (Web): Feature entwickeln & committen
# → Branch: claude/feature-xyz
# → Git: Committed & gepusht
# → Teleport-Befehl erhalten: claude --teleport session_xxx

# 2. Lokale Umgebung vorbereiten
cd /path/to/slide_assistant

# Falls Sie lokal AUCH entwickelt haben:
git status                                    # Status prüfen
git add . && git commit -m "WIP: Local work" # Changes sichern
git checkout master                           # Zu Master wechseln
git pull origin master                        # Master aktualisieren

# Falls Sie lokal NICHTS entwickelt haben:
git checkout master && git pull origin master # Einfach Master aktualisieren

# 3. Im lokalen Terminal: Session teleportieren
claude --teleport session_xxx
# → Claude Code Desktop öffnet sich mit vollständigem Kontext

# 4. In Claude Code Desktop: Agent testen lassen
@agent web-to-local-sync-tester {
  "remote_branch": "claude/feature-xyz",
  "test_scope": "full"
}
# → Agent gibt Report (✅ Merge Ready / ❌ Fixes Needed)
```

**Vorteile:**
- ✅ Kein Kontext-Verlust zwischen Web & Lokal
- ✅ Vollständige Konversationshistorie bleibt erhalten
- ✅ Automatisches Testing & Merge-Empfehlung
- ✅ Ideal für 2+ parallele Web-Entwicklungen

**Detaillierte Anleitung:** Siehe `TELEPORT_QUICK_GUIDE.md` (5 Min) oder `TELEPORT_MULTI_SESSION_WORKFLOW.md` (15 Min)

---

## Alternative: Direkter Agent-Aufruf (ohne Teleport)

Falls Sie den Agent direkt aufrufen möchten (ohne Teleport):

### Schritt 1: Agent aufrufen

```
Der lokale Branch und der Remote Branch sind voneinander unterschiedlich,
da ich hier zwei unterschiedliche Features entwickelt habe. Einmal lokal
mit Claude Code und einmal im Web mit Claude Code.

@agent web-to-local-sync-tester {
  "remote_branch": "claude/ihr-web-branch-name",
  "test_scope": "full"
}
```

### Schritt 2: Agent analysiert

Der Agent führt automatisch aus:

1. **Fetch:** Holt Remote-Branch von GitHub
2. **Analyse:** Zeigt alle Änderungen (Commits, Files, Diffs)
3. **Testing:** Führt Tests durch (API + Frontend)
4. **Konflikte:** Prüft auf Merge-Konflikte
5. **Report:** Gibt detaillierten Bericht

### Schritt 3: Ergebnis interpretieren

#### ✅ Wenn Tests erfolgreich:

```markdown
## Recommendation: ✅ MERGE READY

### Merge Commands:
git checkout master
git pull origin master
git merge claude/ihr-branch
git push origin master
```

**→ Führen Sie diese Befehle aus!**

#### ❌ Wenn Tests fehlgeschlagen:

```markdown
## Recommendation: ❌ FIXES NEEDED

### Failed Tests:
1. test_xyz.py: ModuleNotFoundError: 'package_name'
   Fix: pip install package_name

### Required Actions:
1. Install missing package
2. Re-run tests
3. Then merge
```

**→ Beheben Sie die Fehler, dann nochmal Agent aufrufen!**

#### ⚠️ Wenn Konflikte erkannt:

```markdown
## Recommendation: ⚠️ MANUAL MERGE REQUIRED

### Conflict in: presentation/unified-editor.html
Lines 1200-1250: Both branches modify same section

Resolution Strategy: COMBINE both features
```

**→ Siehe GIT_WORKFLOW_GUIDE.md für Konflikt-Resolution!**

---

## Praktisches Beispiel

### Ihr typischer Workflow (mit Teleport - empfohlen):

```bash
# 1. Im Web entwickelt (claude.ai/code)
# → Branch: claude/multi-provider-xyz
# → Features: Anthropic + Gemini Support
# → Git: Committed & gepusht
# → Teleport-Befehl erhalten: claude --teleport session_abc123

# 2. Lokale Umgebung vorbereiten
cd ~/Schreibtisch/cursor_dev/slide_assistant

# Prüfen, ob lokal entwickelt wurde:
git status

# Falls uncommitted changes (lokal entwickelt):
git add .
git commit -m "WIP: Fullscreen feature local work"
# Optional: Branch pushen für Backup
git push origin claude/fullscreen-local

# Zu Master wechseln:
git checkout master
git pull origin master

# 3. Im lokalen Terminal: Session teleportieren
claude --teleport session_abc123
# → Claude Code Desktop öffnet sich

# 4. In Claude Code Desktop: Agent testen lassen
@agent web-to-local-sync-tester {
  "remote_branch": "claude/multi-provider-xyz",
  "test_scope": "full"
}

# 5. Agent gibt Report:
✅ Tests: 35 passed, 0 failed
✅ No conflicts
✅ MERGE READY

# 6. Befehle ausführen (basierend auf Agent-Empfehlung):
git checkout master
git pull origin master
git merge claude/multi-provider-xyz
git push origin master

# 7. Optional: Zurück zu lokaler Arbeit
git checkout claude/fullscreen-local
git rebase master  # Lokale Arbeit auf neuen Master rebasen

# 8. Fertig! ✅
```

### Alternative: Ohne Teleport (Direkter Agent-Aufruf)

```
# 1. Im Web entwickelt (claude.ai/code)
# → Branch: claude/multi-provider-xyz

# 2. Lokal in Claude Code Desktop:
Der Web-Branch claude/multi-provider-xyz soll getestet werden
bevor ich ihn merge.

@agent web-to-local-sync-tester {
  "remote_branch": "claude/multi-provider-xyz",
  "local_branch": "master",
  "test_scope": "full"
}

# 3. Agent gibt Report & Merge-Befehle
# 4. Befehle ausführen
```

---

## Häufige Szenarien

### Szenario 1: Kleines Feature, schneller Check

```
Quick Test für Fullscreen-Button Feature.

@agent web-to-local-sync-tester {
  "remote_branch": "claude/fullscreen-abc",
  "test_scope": "quick"
}
```

**Ergebnis:** 1-2 Minuten → ✅ oder ❌

---

### Szenario 2: Nur Backend geändert

```
Neue Agents hinzugefügt, Frontend unverändert.

@agent web-to-local-sync-tester {
  "remote_branch": "claude/new-agents-xyz",
  "test_scope": "api-only"
}
```

**Ergebnis:** Nur API-Tests → 3-5 Minuten

---

### Szenario 3: Parallele Features (Konflikte möglich)

```
Ich habe 2 Features parallel entwickelt, beide ändern
unified-editor.html.

Feature 1: Model Selector
@agent web-to-local-sync-tester {
  "remote_branch": "claude/model-selector",
  "test_scope": "full"
}

Feature 2: Fullscreen
@agent web-to-local-sync-tester {
  "remote_branch": "claude/fullscreen",
  "local_branch": "claude/model-selector",
  "test_scope": "full"
}
```

**Ergebnis:** Agent zeigt Konflikte in unified-editor.html → Manuelle Resolution

---

### Szenario 4: Lokal + Web entwickelt (Hybrid Workflow)

```bash
# Ausgangssituation:
# - Lokal: claude/feature-a (in Arbeit, uncommitted)
# - Web: claude/feature-b (fertig, gepusht)

# Schritt 1: Lokale Arbeit sichern
cd ~/Schreibtisch/cursor_dev/slide_assistant
git status  # Zeigt uncommitted changes in Feature A
git add .
git commit -m "WIP: Feature A - work in progress"
git push origin claude/feature-a  # Backup!

# Schritt 2: Zu Master wechseln
git checkout master
git pull origin master

# Schritt 3: Web-Feature via Teleport testen
claude --teleport session_xxx

# In Claude Code Desktop:
@agent web-to-local-sync-tester {
  "remote_branch": "claude/feature-b",
  "test_scope": "full"
}

# Schritt 4: Web-Feature mergen (wenn ✅)
git checkout master
git merge claude/feature-b
git push origin master

# Schritt 5: Zurück zu lokaler Arbeit
git checkout claude/feature-a
git rebase master  # Feature A auf aktuellen Master (inkl. Feature B)

# Schritt 6: Weiter an Feature A arbeiten
# → Feature A hat jetzt Feature B integriert
```

**Ergebnis:** Beide Features bleiben aktuell, keine Konflikte durch rechtzeitiges Rebase

---

## Wichtige Hinweise

### ⚠️ Agent ist kein Ersatz für manuelle Prüfung

Der Agent automatisiert:
- ✅ Tests ausführen
- ✅ Konflikte erkennen
- ✅ Empfehlungen geben

Der Agent kann NICHT:
- ❌ Konflikte automatisch lösen
- ❌ Code schreiben/fixen
- ❌ Automatisch mergen

**→ Sie treffen finale Entscheidung!**

---

### ✅ Best Practice

1. **Immer `full` Test vor Production-Merge**
2. **Quick Test für kleine Features OK**
3. **Bei Unsicherheit: Manuelle Prüfung zusätzlich**
4. **Agent-Report dokumentieren** (Copy-Paste in File)

### ✅ Lokale Umgebung vorbereiten

**Vor jedem Teleport:**

```bash
# 1. Status prüfen
git status

# 2. Uncommitted changes sichern (falls vorhanden)
git add . && git commit -m "WIP: Lokale Arbeit"

# 3. Aktuellen Branch pushen (Backup!)
git push origin $(git branch --show-current)

# 4. Zu Master wechseln
git checkout master
git pull origin master

# 5. Jetzt erst teleportieren
claude --teleport session_xxx
```

**Warum wichtig?**
- ✅ Keine Arbeit geht verloren
- ✅ Sauberer Zustand für Agent-Tests
- ✅ Master ist aktuell für Merge
- ✅ Zurückkehren zu lokaler Arbeit jederzeit möglich

---

## Nächste Schritte

### Für Teleport-Workflow (empfohlen):
1. **Lesen:** `TELEPORT_QUICK_GUIDE.md` (5 Min) - 4-Schritte-Anleitung mit lokaler Vorbereitung
2. **Vertiefen:** `TELEPORT_MULTI_SESSION_WORKFLOW.md` (15 Min) - Für 2+ parallele Features
3. **Referenz:** `AGENT_WEB_TO_LOCAL_SYNC.md` - Vollständige Agent-Dokumentation

### Für direkten Agent-Aufruf:
1. **Lesen:** `AGENT_WEB_TO_LOCAL_SYNC.md` für vollständige Dokumentation
2. **Testen:** Agent mit einem Test-Branch ausprobieren
3. **Anpassen:** Test-Scope je nach Bedarf wählen
4. **Workflow etablieren:** Agent in regulären Workflow integrieren

---

## Support

Bei Problemen oder Fragen:
1. Siehe `AGENT_WEB_TO_LOCAL_SYNC.md` → Trouble-Shooting Section
2. Siehe `GIT_WORKFLOW_GUIDE.md` → Konflikt-Resolution
3. Siehe `CLAUDE.md` → Projekt-spezifische Infos

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

# Web-to-Local Sync Agent - Quick Start

## 🚀 Empfohlener Workflow: Teleport + Agent

**NEU:** Der bevorzugte Weg ist jetzt **Teleport** + **Agent** - nahtlos von Web zu Lokal!

### Schnellstart (3 Schritte)

```bash
# 1. In claude.ai/code (Web): Feature entwickeln & committen
# → Branch: claude/feature-xyz
# → Teleport-Befehl erhalten: claude --teleport session_xxx

# 2. Im lokalen Terminal: Session teleportieren
cd /path/to/slide_assistant
claude --teleport session_xxx
# → Claude Code Desktop öffnet sich mit vollständigem Kontext

# 3. In Claude Code Desktop: Agent testen lassen
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

# 2. Im lokalen Terminal: Session teleportieren
cd ~/Schreibtisch/cursor_dev/slide_assistant
claude --teleport session_abc123
# → Claude Code Desktop öffnet sich

# 3. In Claude Code Desktop: Agent testen lassen
@agent web-to-local-sync-tester {
  "remote_branch": "claude/multi-provider-xyz",
  "test_scope": "full"
}

# 4. Agent gibt Report:
✅ Tests: 35 passed, 0 failed
✅ No conflicts
✅ MERGE READY

# 5. Befehle ausführen (basierend auf Agent-Empfehlung):
git checkout master
git pull origin master
git merge claude/multi-provider-xyz
git push origin master

# 6. Fertig! ✅
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

---

## Nächste Schritte

### Für Teleport-Workflow (empfohlen):
1. **Lesen:** `TELEPORT_QUICK_GUIDE.md` (5 Min) - 3-Schritte-Anleitung
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

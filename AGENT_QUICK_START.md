# Web-to-Local Sync Agent - Quick Start

## So verwenden Sie den Agent in Claude Code

### Schritt 1: Agent aufrufen

Wenn Sie in Claude Code (Desktop oder Web) sind, geben Sie einfach ein:

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

### Ihr typischer Workflow:

```
# 1. Im Web entwickelt (claude.ai/code)
# → Branch: claude/multi-provider-xyz
# → Features: Anthropic + Gemini Support

# 2. Lokal in Claude Code Desktop:
Der Web-Branch claude/multi-provider-xyz soll getestet werden
bevor ich ihn merge.

@agent web-to-local-sync-tester {
  "remote_branch": "claude/multi-provider-xyz",
  "local_branch": "master",
  "test_scope": "full"
}

# 3. Agent gibt Report:
✅ Tests: 35 passed, 0 failed
✅ No conflicts
✅ Merge-Ready!

# 4. Befehle ausführen:
git checkout master
git pull origin master
git merge claude/multi-provider-xyz
git push origin master

# 5. Fertig! ✅
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

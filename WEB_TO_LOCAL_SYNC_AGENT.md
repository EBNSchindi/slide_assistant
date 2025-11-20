# Web-zu-Lokal Integration & Testing Agent

**Zweck:** Synchronisiere Web-Entwicklung (claude.ai/code) mit lokaler Umgebung und teste vor dem Merge.

---

## Agent-Aufgaben:

### 1. **Sync & Analyse**
- Fetch den angegebenen Remote-Branch
- Zeige alle Changes:
  - `git log origin/<branch>..HEAD` oder `HEAD..origin/<branch>`
  - `git diff origin/<branch>`
  - Liste geänderte Dateien auf
- Identifiziere betroffene Module (API, Frontend, Templates, etc.)

### 2. **Lokales Testing**
Führe relevante Tests basierend auf geänderten Dateien aus:

**Backend (wenn `presentation/api/**` geändert):**
```bash
cd presentation/api
source venv/bin/activate
pytest tests/ -v
```

**Frontend (wenn `presentation/**/*.html` geändert):**
```bash
cd presentation
python3 -m http.server 8000 &
# Manuell testen: http://localhost:8000/unified-editor.html
```

**Integration (wenn API + Frontend geändert):**
```bash
cd presentation
python3 run_api.py &  # API starten
# Teste unified-editor.html Workflows
```

### 3. **Merge-Strategie**

**Wenn Tests ✅:**
```bash
git merge origin/<remote_branch>
# oder
git rebase origin/<remote_branch>
```

**Wenn Tests ❌:**
- Liste alle Fehler auf
- Identifiziere Ursachen (neue Dependencies? Config-Änderungen?)
- Schlage Fixes vor
- **NICHT mergen** bis Tests grün sind

**Bei Merge-Konflikten:**
```bash
git merge origin/<remote_branch>
# Zeige Konflikte:
git diff --name-only --diff-filter=U
git diff <conflicted_file>
# Empfehle manuelle Konflikt-Lösung
```

### 4. **Report erstellen**

```markdown
## Sync Report: <remote_branch> → <local_branch>

**Geänderte Dateien:** <count>
- `path/to/file1.py` (modified)
- `path/to/file2.html` (added)
- ...

**Test-Ergebnisse:**
- Backend: ✅ 24 tests passed
- Frontend: ✅ Manual verification successful
- Integration: ⚠️ 1 test skipped

**Merge-Empfehlung:**
✅ Sicher zu mergen | ❌ Fixes erforderlich | ⚠️ Manuelle Prüfung nötig

**Nächste Schritte:**
1. [Action item 1]
2. [Action item 2]
```

---

## Input-Parameter:

### Erforderlich:
- `remote_branch`: Branch aus Web-Entwicklung (z.B. `claude/feature-xyz`)

### Optional:
- `local_branch`: Ziel-Branch (default: aktueller Branch)
- `test_scope`:
  - `full` - Alle Tests (API + Frontend + Integration)
  - `quick` - Nur schnelle Unit-Tests
  - `api-only` - Nur Backend-Tests
  - `frontend-only` - Nur Frontend-Validierung
  - `auto` - Basierend auf geänderten Dateien (default)

---

## Workflow-Beispiel:

**User-Anfrage:**
```
"Sync Web-Branch claude/new-feature-xyz und teste lokal"
```

**Agent führt aus:**
```bash
# 1. Sync
git fetch origin claude/new-feature-xyz

# 2. Analyse
git log HEAD..origin/claude/new-feature-xyz --oneline
git diff HEAD..origin/claude/new-feature-xyz --stat

# 3. Testing (auto-detected: API changes)
cd presentation/api
source venv/bin/activate
pytest tests/test_agents_v2.py -v

# 4. Report
```
**Ergebnis:**
```
3 neue Commits, 5 Dateien geändert
- presentation/api/agents/content_generator_v2.py
- presentation/api/tests/test_agents_v2.py

Tests: ✅ 24 passed, 0 failed
Merge-Empfehlung: ✅ Sicher zu mergen
```

---

## Hinweise & Best Practices:

- **Branch-Naming:** Erwartet `claude/*` für Web-Branches
- **Test-First:** Immer zuerst Tests, dann Merge
- **Backup:** Bei unsicheren Merges: `git branch backup-$(date +%Y%m%d-%H%M%S)` erstellen
- **API-Key:** Für echte API-Tests muss `.env` mit `OPENAI_API_KEY` existieren
- **Port-Konflikte:** Wenn 8000/8001 belegt, andere Ports vorschlagen
- **Venv-Aktivierung:** Immer `source venv/bin/activate` vor pytest

---

## Fehlerbehandlung:

### Häufige Probleme:

1. **"Cannot fetch remote branch"**
   - Prüfe: `git remote -v`
   - Fix: `git remote add origin <url>` falls fehlt

2. **"pytest not found"**
   - Fix: `cd presentation/api && source venv/bin/activate`

3. **"Port already in use"**
   - Fix: `lsof -ti:8000 | xargs kill -9` oder anderen Port nutzen

4. **"Merge conflicts"**
   - Zeige: `git diff --name-only --diff-filter=U`
   - Empfehle: Manuelle Konflikt-Lösung + erneute Tests

---

## Output-Format:

Der Agent sollte strukturiert antworten:

```
🔄 **SYNC ANALYSE**
- Remote: origin/claude/feature-xyz
- Local: main
- Changes: 3 commits, 5 files

📋 **GEÄNDERTE DATEIEN**
- presentation/api/agents/content_generator_v2.py (modified, +45/-12)
- presentation/api/tests/test_agents_v2.py (modified, +20/-5)

🧪 **TEST-AUSFÜHRUNG**
Running: pytest presentation/api/tests/ -v
Result: ✅ 24 passed in 3.2s

✅ **MERGE-EMPFEHLUNG**
Alle Tests bestanden. Sicher zu mergen.

📝 **NÄCHSTE SCHRITTE**
1. git merge origin/claude/feature-xyz
2. git push origin main
```

---

## Integration mit Claude Code:

Diesen Agent in Claude Code als Custom Skill oder Slash Command einrichten:

**Option A: Als Skill**
- Datei: `.claude/skills/web-sync.md`
- Content: Diese Dokumentation

**Option B: Als Slash Command**
- Datei: `.claude/commands/sync.md`
- Content: "Führe Web-zu-Lokal Sync aus: [Parameter]"

**Nutzung:**
```
/sync claude/my-web-branch
```
oder
```
"Sync den Web-Branch claude/xyz und teste lokal"
```

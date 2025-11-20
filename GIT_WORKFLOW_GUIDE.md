# Git Workflow Guide: Web & Lokal Entwicklung zusammenführen

## 🎯 Ihr typischer Workflow

Sie entwickeln Features parallel:
- **Lokal** mit Claude Code (Desktop)
- **Im Web** mit claude.ai/code
- **Verschiedene Branches** für verschiedene Features

Dieses Dokument zeigt Ihnen Schritt für Schritt, wie Sie diese zusammenführen.

---

## 📚 Grundlegende Konzepte

### Branch-Arten
- `master` - Hauptbranch (stabil, produktiv)
- `feature/xyz` - Neue Features
- `fix/xyz` - Bugfixes
- `claude/xyz` - Von Claude Code generierte Branches

### Pull Request (PR)
- Ein PR ist ein "Merge-Antrag"
- Sie sagen: "Ich möchte Branch X in Branch Y mergen"
- Andere können reviewen, bevor gemerged wird
- GitHub zeigt alle Änderungen übersichtlich

---

## 🚀 Workflow: Features zusammenführen

### Schritt 1: Lokalen Master aktualisieren ⚠️ IMMER ZUERST!

```bash
# 1. Neueste Änderungen vom Remote holen
git fetch origin

# 2. Zu Master wechseln
git checkout master

# 3. Master aktualisieren
git pull origin master
```

**Warum wichtig?**
- Ihr lokaler Master kann veraltet sein
- Beide Feature-Branches müssen auf aktuellem Master basieren
- Verhindert unnötige Merge-Konflikte

---

### Schritt 2: Feature-Branches identifizieren

```bash
# Alle lokalen Branches anzeigen
git branch

# Alle Remote-Branches anzeigen
git branch -r

# Branch-Status prüfen
git status
```

**Fragen Sie sich:**
- Welche Features habe ich lokal entwickelt?
- Welche Features wurden im Web entwickelt?
- Welcher Branch ist aktueller/größer?

---

### Schritt 3: Größtes Feature ZUERST mergen

**Regel:** Großes Feature → Master, dann kleines Feature → Master

**Beispiel:**
- Feature A: 150 Files, 5000 Lines → ZUERST mergen
- Feature B: 1 File, 50 Lines → DANACH mergen

**Warum?** Kleinere Features sind einfacher anzupassen, wenn Konflikte auftreten.

---

### Schritt 4: Pull Request erstellen

#### Option A: Via GitHub CLI (Terminal)

```bash
# 1. Zu Feature-Branch wechseln
git checkout feature/mein-feature

# 2. Neueste Änderungen pushen
git push origin feature/mein-feature

# 3. Pull Request erstellen
gh pr create --title "Feature: Mein neues Feature" \
  --body "Beschreibung was dieses Feature tut" \
  --base master
```

#### Option B: Via GitHub Website

1. Gehen Sie zu: https://github.com/EBNSchindi/slide_assistant
2. Klicken Sie auf "Pull requests" → "New pull request"
3. **Base:** `master` (Wohin mergen)
4. **Compare:** `feature/mein-feature` (Was mergen)
5. Titel & Beschreibung eingeben
6. "Create pull request" klicken

---

### Schritt 5: PR reviewen & mergen

**Checkliste vor dem Merge:**
- [ ] Alle Tests laufen durch?
- [ ] Keine Merge-Konflikte?
- [ ] Beschreibung ist verständlich?
- [ ] Code sieht sinnvoll aus?

**Auf GitHub:**
1. PR öffnen (z.B. PR #16)
2. Auf "Files changed" klicken → Änderungen anschauen
3. Auf "Checks" klicken → Tests prüfen
4. Wenn alles OK: **"Merge pull request"** klicken
5. **"Confirm merge"** klicken
6. Optional: Branch löschen (GitHub fragt automatisch)

---

### Schritt 6: Nach Merge - Master lokal aktualisieren

```bash
# Nach jedem Merge auf GitHub:
git checkout master
git pull origin master
```

**Warum?** Ihr lokaler Master braucht die neuen Änderungen für den nächsten Merge.

---

## 🔀 Konflikte auflösen (Manual Merge)

### Wann passieren Konflikte?

Beide Branches ändern **dieselbe Datei** an **derselben Stelle**.

**Beispiel:**
- Feature A ändert Zeile 100 in `unified-editor.html`
- Feature B ändert auch Zeile 100 in `unified-editor.html`
- Git weiß nicht, welche Version behalten werden soll → **KONFLIKT**

---

### Konflikt-Resolution: Schritt für Schritt

#### 1. Merge versuchen

```bash
git checkout feature/mein-feature
git merge master
```

#### 2. Konflikt wird angezeigt

```
Auto-merging presentation/unified-editor.html
CONFLICT (content): Merge conflict in presentation/unified-editor.html
Automatic merge failed; fix conflicts and then commit the result.
```

#### 3. Konfliktmarker in Datei finden

Git fügt spezielle Marker ein:

```html
<<<<<<< HEAD (Ihr Code - aktueller Branch)
<div class="fullscreen-controls">
  <button>Vollbild</button>
</div>
=======  (Trennlinie)
<select id="modelSelect">
  <option>GPT-4o</option>
</select>
>>>>>>> master (Master Code - incoming)
```

#### 4. Entscheiden: Was behalten?

**3 Optionen:**
- A) Nur HEAD (Ihr Code) behalten
- B) Nur master (Incoming Code) behalten
- C) **Beide kombinieren** (meist beste Option!)

**Beispiel kombiniert:**
```html
<!-- Beide Features kombiniert! -->
<select id="modelSelect">
  <option>GPT-4o</option>
</select>

<div class="fullscreen-controls">
  <button>Vollbild</button>
</div>
```

#### 5. Konfliktmarker entfernen

Löschen Sie alle Zeilen mit:
- `<<<<<<<`
- `=======`
- `>>>>>>>`

#### 6. Datei speichern & Merge abschließen

```bash
# Datei zu Staging hinzufügen
git add presentation/unified-editor.html

# Merge committen
git commit -m "Merge master: Combine model selector + fullscreen features"

# Zum Remote pushen
git push origin feature/mein-feature
```

---

## 🎨 Praktisches Beispiel: Fullscreen + Multi-Provider

### Situation
- **Branch A:** `claude/attempt-n-...` (Multi-Provider LLM - 142 Files)
- **Branch B:** `claude/fullscreen-...` (Fullscreen Mode - 1 File)
- **Konflikt:** Beide ändern `unified-editor.html`

### Konflikt-Details

**Branch A (Multi-Provider) fügt hinzu:**
```html
<select id="modelSelect">
  <optgroup label="OpenAI">...</optgroup>
  <optgroup label="Anthropic">...</optgroup>
  <optgroup label="Google">...</optgroup>
</select>
```

**Branch B (Fullscreen) fügt hinzu:**
```html
<div class="fullscreen-controls">
  <button id="enterFullscreenBtn">⛶ Vollbild</button>
</div>

<style>
.preview-panel.fullscreen {
  position: fixed;
  width: 100vw;
  height: 100vh;
}
</style>
```

### Lösung: Beide kombinieren!

1. Model Selector **OBEN** (im Header)
2. Fullscreen Styles **IM <style>-Tag**
3. Fullscreen Controls **IN Preview-Panel**

**Ergebnis:** Beide Features funktionieren zusammen! ✅

---

## 📋 Checkliste: Vor jedem Merge

- [ ] `git fetch origin` ausgeführt
- [ ] Lokaler Master ist aktuell (`git pull origin master`)
- [ ] Feature-Branch ist gepusht
- [ ] Tests laufen lokal (optional: `pytest`)
- [ ] Keine Syntax-Fehler im Code
- [ ] README/Docs aktualisiert (wenn nötig)

---

## 🎯 Tipps für konfliktfreies Arbeiten

### 1. Kleine, fokussierte Features

**Gut:**
```
feature/add-fullscreen-button (1 File)
feature/add-model-selector (2 Files)
```

**Schlecht:**
```
feature/complete-rewrite (150 Files)
```

### 2. Häufig pushen

```bash
# Nach jedem logischen Schritt:
git add .
git commit -m "Beschreibung"
git push origin mein-branch
```

**Vorteil:** Wenn etwas schief geht, können Sie zurückrollen.

### 3. Regelmäßig Master mergen

```bash
# Jede Woche (oder öfter):
git checkout mein-feature-branch
git merge master
```

**Vorteil:** Kleine, häufige Merges sind einfacher als ein großer Merge am Ende.

### 4. Kommunizieren

Wenn Sie an `unified-editor.html` arbeiten:
- Sagen Sie Ihrem Team Bescheid
- Oder: Koordinieren Sie, WER WANN an dieser Datei arbeitet

---

## 🛠️ Nützliche Git-Befehle

### Status & Info

```bash
# Aktueller Branch & Status
git status

# Branch-Liste
git branch -a

# Änderungen seit letztem Commit
git diff

# Commit-Historie
git log --oneline -10

# Wer hat diese Zeile geändert?
git blame dateiname.html
```

### Branch-Management

```bash
# Neuen Branch erstellen & wechseln
git checkout -b feature/neues-feature

# Branch wechseln
git checkout branch-name

# Branch löschen (lokal)
git branch -d branch-name

# Branch löschen (remote)
git push origin --delete branch-name
```

### Undo & Reset

```bash
# Letzte Änderungen verwerfen (⚠️ unwiderruflich!)
git restore dateiname.html

# Letzten Commit rückgängig (behält Änderungen)
git reset --soft HEAD~1

# Zum letzten Stand zurückkehren (⚠️ löscht Änderungen!)
git reset --hard HEAD

# Zum Remote-Stand zurückkehren
git reset --hard origin/master
```

---

## 🚨 Häufige Fehler & Lösungen

### Fehler 1: "Your local changes would be overwritten"

**Problem:** Sie haben uncommittete Änderungen, Git will nicht wechseln.

**Lösung:**
```bash
# Option A: Änderungen committen
git add .
git commit -m "WIP: Zwischenstand"

# Option B: Änderungen temporär weglegen
git stash
git checkout other-branch
# ... Arbeit erledigen ...
git checkout original-branch
git stash pop  # Änderungen zurückholen
```

---

### Fehler 2: "Pull request already exists"

**Problem:** Sie versuchen einen 2. PR für denselben Branch zu erstellen.

**Lösung:**
```bash
# PR-Status prüfen
gh pr status

# Existierenden PR anschauen
gh pr view 16

# Optional: PR updaten (neue Commits werden automatisch hinzugefügt)
git push origin branch-name
```

---

### Fehler 3: "Merge conflict in ..."

**Problem:** Beide Branches haben dieselbe Datei geändert.

**Lösung:** Siehe Abschnitt "Konflikt-Resolution" oben!

Kurz:
1. Konfliktdatei öffnen
2. Konfliktmarker (`<<<<<<<`, `=======`, `>>>>>>>`) finden
3. Entscheiden: Was behalten?
4. Marker entfernen
5. `git add datei.html`
6. `git commit`

---

### Fehler 4: "You are 20 commits behind origin/master"

**Problem:** Ihr lokaler Master ist veraltet.

**Lösung:**
```bash
git checkout master
git pull origin master
```

**Ab jetzt vor jedem Merge ausführen!**

---

## 🎓 Workflow-Beispiel: Vollständiger Durchlauf

### Szenario
- Lokal entwickelt: Fullscreen-Feature (1 File)
- Web entwickelt: Multi-Provider (142 Files)
- Beide ändern: `unified-editor.html`

### Schritt-für-Schritt (30 Minuten)

```bash
# ============================================
# PHASE 1: Vorbereitung (5 Min)
# ============================================

# 1. Master aktualisieren
git fetch origin
git checkout master
git pull origin master

# 2. Feature-Branches checken
git branch -a
# Sehe: claude/attempt-n-...
# Sehe: claude/fullscreen-...

# ============================================
# PHASE 2: Multi-Provider Branch (10 Min)
# ============================================

# 3. Multi-Provider Branch pushen
git checkout claude/attempt-n-013a8hfTz3c5TBaWGAezwxDR
git push origin claude/attempt-n-013a8hfTz3c5TBaWGAezwxDR

# 4. Pull Request erstellen
gh pr create --title "Feature: Multi-Provider LLM Support" \
  --body "Adds Anthropic Claude + Google Gemini" \
  --base master

# 5. Auf GitHub: PR #16 mergen
# (via Browser: "Merge pull request" klicken)

# 6. Master lokal aktualisieren
git checkout master
git pull origin master

# ============================================
# PHASE 3: Fullscreen Branch (15 Min)
# ============================================

# 7. Fullscreen Branch mit Master mergen
git checkout claude/fullscreen-display-window-01JoL4D7DqaJBB63eAcLU1JK
git merge master

# KONFLIKT! Erwartete Ausgabe:
# CONFLICT (content): Merge conflict in presentation/unified-editor.html

# 8. Konflikt manuell auflösen
code presentation/unified-editor.html
# (Editor öffnet sich)

# Konfliktmarker finden:
# <<<<<<< HEAD
# Mein Fullscreen-Code
# =======
# Master's Multi-Provider Code
# >>>>>>> master

# BEIDE kombinieren:
# - Model Selector aus Master behalten
# - Fullscreen Controls aus HEAD behalten

# 9. Konfliktmarker entfernen & speichern

# 10. Merge abschließen
git add presentation/unified-editor.html
git commit -m "Merge master: Combine multi-provider + fullscreen features"

# 11. Pushen & PR erstellen
git push origin claude/fullscreen-display-window-01JoL4D7DqaJBB63eAcLU1JK
gh pr create --title "Feature: Fullscreen Mode" \
  --body "Adds fullscreen button + ESC support" \
  --base master

# 12. Auf GitHub: PR #17 mergen

# ============================================
# PHASE 4: Cleanup (5 Min)
# ============================================

# 13. Master aktualisieren
git checkout master
git pull origin master

# 14. Feature-Branches löschen
git branch -d claude/attempt-n-013a8hfTz3c5TBaWGAezwxDR
git branch -d claude/fullscreen-display-window-01JoL4D7DqaJBB63eAcLU1JK

# 15. Remote-Branches löschen (optional)
git push origin --delete claude/attempt-n-013a8hfTz3c5TBaWGAezwxDR
git push origin --delete claude/fullscreen-display-window-01JoL4D7DqaJBB63eAcLU1JK

# FERTIG! ✅
```

---

## 📖 Weiterführende Ressourcen

### GitHub CLI (gh)

```bash
# Alle PRs anzeigen
gh pr list

# PR Details anschauen
gh pr view 16

# PR Status
gh pr status

# PR mergen (von Terminal)
gh pr merge 16 --merge

# PR schließen ohne Merge
gh pr close 16
```

### Git Workflows

- **Feature Branch Workflow:** Jedes Feature = eigener Branch
- **Gitflow:** master + develop + feature/* + release/*
- **Trunk-Based:** Alle committen auf master (nur für kleine Teams)

**Empfehlung für Sie:** Feature Branch Workflow (genau das, was Sie jetzt tun!)

---

## ✅ Zusammenfassung: Ihre Standard-Routine

```bash
# === JEDEN TAG BEIM START ===
git fetch origin
git checkout master
git pull origin master

# === NEUES FEATURE STARTEN ===
git checkout -b feature/mein-feature
# ... Code schreiben ...
git add .
git commit -m "Feature: Beschreibung"
git push origin feature/mein-feature

# === FEATURE FERTIG? ===
gh pr create --title "..." --body "..." --base master
# Auf GitHub: PR mergen
git checkout master
git pull origin master
git branch -d feature/mein-feature

# === KONFLIKT? ===
# 1. Konfliktdatei öffnen
# 2. Konfliktmarker finden & auflösen
# 3. git add datei.html
# 4. git commit
# 5. git push
```

---

## 💡 Ihr persönlicher Tipp

**Am Anfang:** Machen Sie kleine Features (1-2 Files), committen Sie oft (nach jeder Änderung).

**Mit Erfahrung:** Größere Features OK, aber trennen Sie logische Schritte in separate Commits.

**Bei Unsicherheit:** Lieber einmal mehr fragen/testen als direkt auf master pushen!

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

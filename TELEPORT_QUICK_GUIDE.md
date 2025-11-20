# Teleport + Agent Workflow - Quick Guide

## 🚀 Was ist Teleport?

**Teleport** = Session-Transfer von claude.ai/code (Web) → Claude Code Desktop (Lokal)

**Befehl aus Web:**
```bash
claude --teleport session_014KZZLRj1jWZvTfp2HMt6rq
```

**Was wird übertragen:**
- ✅ Komplette Konversation
- ✅ Agent-Status
- ✅ Projekt-Kontext
- ✅ Alle gelesenen Dateien

---

## 📋 3-Schritte-Anleitung

### Schritt 1: Web-Entwicklung abschließen

```
In claude.ai/code:
1. Feature entwickeln
2. Code committen
3. Branch pushen: git push origin claude/feature-xyz
4. Teleport-Befehl kopieren
   → claude --teleport session_xxx
```

### Schritt 2: Session teleportieren

```bash
# Im lokalen Terminal
cd /path/to/slide_assistant
claude --teleport session_xxx
```

**→ Claude Code Desktop öffnet sich mit Session**

### Schritt 3: Agent testen lassen

```
In Claude Code Desktop (nach Teleport):

@agent web-to-local-sync-tester {
  "remote_branch": "claude/feature-xyz",
  "test_scope": "full"
}

→ Agent testet Branch
→ Gibt Empfehlung (✅ Merge / ❌ Fix / ⚠️ Resolve)
```

---

## 💡 Beispiel: Single Session

### Szenario
Web-entwickeltes Multi-Provider Feature lokal testen.

```
┌─────────────────────────────────────┐
│ claude.ai/code (Web)                │
│ Feature: Multi-Provider LLM Support │
│ Branch: claude/multi-provider-abc   │
│ Status: Fertig entwickelt           │
│ → Teleport-Befehl:                  │
│   claude --teleport session_xyz     │
└─────────────────────────────────────┘
            ↓ (Teleport)
┌─────────────────────────────────────┐
│ Lokales Terminal                    │
│ cd ~/projects/slide_assistant       │
│ claude --teleport session_xyz       │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│ Claude Code Desktop                 │
│ Session geladen mit vollständigem   │
│ Kontext aus Web-Entwicklung         │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│ In Desktop-Session:                 │
│                                     │
│ @agent web-to-local-sync-tester {   │
│   "remote_branch":                  │
│     "claude/multi-provider-abc",    │
│   "test_scope": "full"              │
│ }                                   │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│ Agent-Report:                       │
│ ✅ Tests: 35 passed, 0 failed       │
│ ✅ No conflicts                     │
│ ✅ MERGE READY                      │
│                                     │
│ Commands:                           │
│ git checkout master                 │
│ git merge claude/multi-provider-abc │
│ git push origin master              │
└─────────────────────────────────────┘
```

---

## 🔄 Beispiel: Multi-Session (2+ parallele Features)

### Szenario
3 Features parallel im Web entwickelt.

```
Web-Sessions:
├── Session 1: claude/multi-provider-abc (42 Files, 12 Commits)
├── Session 2: claude/fullscreen-xyz (1 File, 2 Commits)
└── Session 3: claude/image-upload-def (8 Files, 5 Commits)
```

### Workflow

#### 1. Größtes Feature zuerst (Multi-Provider)

```bash
# Session 1 teleportieren
claude --teleport session_aaa

# In Desktop:
@agent web-to-local-sync-tester {
  "remote_branch": "claude/multi-provider-abc",
  "test_scope": "full"
}

# → ✅ Merge-Ready
git checkout master
git merge claude/multi-provider-abc
git push origin master
```

#### 2. Master aktualisieren, dann Session 2

```bash
# Zurück zu Terminal
git checkout master
git pull origin master  # Holt Multi-Provider Merge

# Session 2 teleportieren
claude --teleport session_bbb

# In Desktop:
@agent web-to-local-sync-tester {
  "remote_branch": "claude/fullscreen-xyz",
  "local_branch": "master",  # Aktualisierter Master!
  "test_scope": "full"
}

# → ✅ Merge-Ready (keine Konflikte mit Multi-Provider)
git checkout master
git merge claude/fullscreen-xyz
git push origin master
```

#### 3. Master aktualisieren, dann Session 3

```bash
git checkout master
git pull origin master

# Session 3 teleportieren
claude --teleport session_ccc

# In Desktop:
@agent web-to-local-sync-tester {
  "remote_branch": "claude/image-upload-def",
  "test_scope": "full"
}

# → ✅ Merge-Ready
git checkout master
git merge claude/image-upload-def
git push origin master
```

---

## 🎯 Welche Session zuerst?

### Priorisierungs-Regel

1. **Größe** → Größter Branch zuerst (weniger Konflikte später)
2. **Abhängigkeiten** → Foundation vor Detail-Features
3. **Konflikte** → Unabhängige vor konfliktträchtigen
4. **Kritikalität** → Wichtigste Features zuerst

### Beispiel-Entscheidung

```
Session A: 42 Files, ändert API + Frontend
Session B: 1 File, nur Frontend
Session C: 8 Files, nur API

Reihenfolge: A → C → B
Grund: A größtes (Foundation), C unabhängig, B klein (leicht anzupassen)
```

---

## ⚡ Quick Commands

### Single Session
```bash
# 1. Teleport
claude --teleport session_xxx

# 2. Agent (in Desktop)
@agent web-to-local-sync-tester {
  "remote_branch": "claude/branch-name",
  "test_scope": "full"
}

# 3. Merge (wenn ✅)
git checkout master
git merge claude/branch-name
git push origin master
```

### Multi-Session (Sequential)
```bash
# Session 1
claude --teleport session_aaa
# → Agent → Merge
git checkout master && git pull

# Session 2
claude --teleport session_bbb
# → Agent → Merge
git checkout master && git pull

# Session 3
claude --teleport session_ccc
# → Agent → Merge
```

---

## ⚠️ Wichtige Hinweise

### Vor Teleport

✅ **Feature fertig entwickelt** (im Web committet & gepusht)
✅ **Branch-Name kennen** (für Agent-Aufruf)
✅ **Richtiges Verzeichnis** (`cd /path/to/project`)

### Nach Teleport

✅ **Agent SOFORT aufrufen** (Kontext ist frisch)
✅ **Master aktualisieren** zwischen Sessions
✅ **Nicht mehrere Sessions parallel** teleportieren (nacheinander!)

### Bei Problemen

❌ **"Session not found"** → Prüfen Sie Session-ID
❌ **"Not in git repo"** → cd in richtiges Verzeichnis
❌ **"Tests fail after teleport"** → Dependencies lokal installieren

---

## 📊 Vergleich: Mit vs. Ohne Teleport

### Ohne Teleport (Alt)

```
1. Web: Feature entwickeln
2. Lokal: Branch manuell fetchen
3. Lokal: Tests manuell ausführen
4. Lokal: Merge manuell durchführen
→ Kontext-Verlust zwischen Web und Lokal
```

### Mit Teleport (Neu) ✅

```
1. Web: Feature entwickeln
2. Teleport: Session übertragen (Kontext bleibt!)
3. Agent: Automatisch testen
4. Merge: Basierend auf Agent-Empfehlung
→ Nahtloser Übergang, kein Kontext-Verlust
```

---

## 🎓 Best Practices

### 1. Branch-Namen dokumentieren

```
# Während Web-Entwicklung:
# → Notieren Sie Branch-Namen für Agent-Aufruf
# Beispiel:
Session 1 → claude/multi-provider-abc
Session 2 → claude/fullscreen-xyz
```

### 2. Sequential Testing

```
# ❌ NICHT parallel teleportieren:
claude --teleport session_aaa &
claude --teleport session_bbb &  # Verwirrung!

# ✅ SEQUENTIAL:
claude --teleport session_aaa
# → Agent → Merge
claude --teleport session_bbb
# → Agent → Merge
```

### 3. Master zwischen Sessions aktualisieren

```
# Nach jedem Merge:
git checkout master
git pull origin master

# Dann nächste Session:
claude --teleport session_next
```

---

## 🔗 Weiterführende Docs

- **Ausführlich:** `TELEPORT_MULTI_SESSION_WORKFLOW.md`
- **Agent-Details:** `AGENT_WEB_TO_LOCAL_SYNC.md`
- **Git-Basics:** `GIT_WORKFLOW_GUIDE.md`

---

## ✅ Zusammenfassung

**Teleport-Workflow:**
1. Web-Feature entwickeln
2. `claude --teleport session_xxx`
3. Agent testen lassen
4. Basierend auf Report mergen

**Multi-Session:**
- Größtes Feature zuerst
- Master zwischen Sessions aktualisieren
- Sequential (nicht parallel)

**Vorteile:**
- ✅ Kein Kontext-Verlust
- ✅ Automatisiertes Testing
- ✅ Sichere Merge-Entscheidung

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

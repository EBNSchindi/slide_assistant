# 🚀 Lokalen Server starten

Die **Beispiel-Dateien** funktionieren jetzt auch ohne Server! ✅

Für **eigene HTML-Dateien** benötigen Sie einen lokalen Server.

---

## ✅ Schnellstart (Python - Empfohlen)

```bash
cd /home/ubuntudani/Projects/Robo4you/presentation
python3 -m http.server 8000
```

Dann öffnen Sie im Browser:
```
http://localhost:8000/component-viewer.html
```

---

## Alternative: Node.js

```bash
cd /home/ubuntudani/Projects/Robo4you/presentation
npx http-server -p 8000
```

Dann öffnen Sie:
```
http://localhost:8000/component-viewer.html
```

---

## 💡 Warum ein Server?

Browser blockieren `fetch()` für lokale Dateien (file://) aus Sicherheitsgründen.

**Lösung:** Lokaler HTTP-Server stellt Dateien über `http://` bereit.

---

## ✨ Gute Nachricht

Die **3 Beispiel-Dateien** sind jetzt direkt eingebettet und funktionieren **ohne Server**!

- ✨ `beispiel 01 problem`
- ✨ `beispiel 02 loesung`
- ✨ `beispiel 03 markt`

Sie können diese sofort im Viewer testen, auch wenn Sie die HTML-Datei direkt öffnen (file://).

---

## 🔧 Server stoppen

**Python:** `Strg+C` im Terminal

**Node.js:** `Strg+C` im Terminal

---

## 📝 Workflow

### Für Beispiele (ohne Server):
1. ✅ Öffnen Sie `component-viewer.html` direkt
2. ✅ Wählen Sie eine Beispiel-Datei aus
3. ✅ Funktioniert sofort!

### Für eigene Dateien (mit Server):
1. ✅ Server starten (siehe oben)
2. ✅ Öffnen Sie `http://localhost:8000/component-viewer.html`
3. ✅ Wählen Sie Ihre Datei aus

---

**Tipp:** Lassen Sie den Server im Hintergrund laufen, während Sie arbeiten!


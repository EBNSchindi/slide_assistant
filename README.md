# Word-zu-Markdown-Konverter

Ein Python-Tool zum Konvertieren von Word-Dokumenten (.docx) in Markdown-Format (.md) mit exakter Wortwiedergabe.

## Features

- ✅ Exakte Wortwiedergabe ohne Inhaltsänderungen
- ✅ Unterstützung für Überschriften (Heading 1-6)
- ✅ Formatierungen: **Fett**, *Kursiv*, <u>Unterstrichen</u>
- ✅ Listen (Bullet- und nummerierte Listen)
- ✅ Tabellen
- ✅ Hyperlinks
- ✅ Batch-Verarbeitung mehrerer Dateien

## Installation

1. Stelle sicher, dass Python 3.6+ installiert ist:
```bash
python3 --version
```

2. Installiere die benötigten Abhängigkeiten:

**Option A: Mit pip (empfohlen)**
```bash
pip install -r requirements.txt
```

**Option B: Mit pip --user (falls system-weite Installation nicht möglich)**
```bash
pip install --user -r requirements.txt
```

**Option C: In einer virtuellen Umgebung (empfohlen für Isolierung)**
```bash
python3 -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Verwendung

### Einzelne Datei konvertieren

```bash
python convert_word_to_markdown.py dokument.docx
```

Dies erstellt automatisch `dokument.md` im gleichen Verzeichnis.

### Mit spezifischem Ausgabedateinamen

```bash
python convert_word_to_markdown.py dokument.docx ausgabe.md
```

### Batch-Verarbeitung (alle .docx-Dateien in einem Ordner)

```bash
python convert_word_to_markdown.py --folder ./documents
```

oder

```bash
python convert_word_to_markdown.py -f /pfad/zum/ordner
```

## Unterstützte Formatierungen

| Word-Format | Markdown-Output |
|------------|----------------|
| Heading 1 | `# Überschrift` |
| Heading 2 | `## Überschrift` |
| Heading 3 | `### Überschrift` |
| Fett | `**Text**` |
| Kursiv | `*Text*` |
| Unterstrichen | `<u>Text</u>` |
| Bullet-Liste | `- Punkt` |
| Nummerierte Liste | `1. Punkt` |
| Tabelle | `\| Spalte1 \| Spalte2 \|` |
| Hyperlink | `[Text](URL)` |

## Beispiele

```bash
# Einzelnes Dokument konvertieren
python convert_word_to_markdown.py Barrieren_und_Datenschutz.docx

# Alle Word-Dokumente im aktuellen Ordner konvertieren
python convert_word_to_markdown.py --folder .

# Mit eigenem Ausgabedateinamen
python convert_word_to_markdown.py input.docx output.md
```

## Hinweise

- Das Tool behält die exakte Wortfolge und den Inhalt bei
- Formatierungen werden so gut wie möglich ins Markdown-Format übertragen
- Komplexe Formatierungen (z.B. verschachtelte Listen, spezielle Styles) werden vereinfacht
- Bilder werden derzeit nicht extrahiert oder konvertiert

## Fehlerbehebung

**Fehler: "ModuleNotFoundError: No module named 'docx'"**
- Lösung: `pip install python-docx`

**Fehler beim Öffnen der Datei**
- Stelle sicher, dass die .docx-Datei nicht beschädigt ist
- Prüfe, ob die Datei wirklich im .docx-Format vorliegt (nicht .doc)

## Lizenz

Frei verwendbar für persönliche und kommerzielle Projekte.


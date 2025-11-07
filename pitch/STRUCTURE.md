# Pitch-Ordnerstruktur – Robo4you

Stand: November 2024

## 📁 Ordnerübersicht

```
pitch/
│
├── README.md                                   # Hauptnavigation & Schnellstart
├── STRUCTURE.md                                # Diese Datei – Ordnerstruktur-Dokumentation
│
├── 00_Executive_Summary.md                     # ⭐ START HIER – Überblick über alle Dokumente
├── 01_Pitch-Deck_Bank-Version.md              # ⭐ HAUPTDOKUMENT – 14 Folien für Banken
├── 02_Validierte_Statistiken_Quellen.md       # Alle Zahlen mit Quellen
├── 03_Praesentationsanleitung.md              # Folie-für-Folie Präsentations-Guide
├── 03_Einwaende_Barrieren_Tabelle.md          # 25 Barrieren & Antworten (aktiv genutzt)
│
├── archive/                                    # Alte Versionen & historische Dokumente
│   ├── 00_Pitch-Deck_Robo4you_ORIGINAL_v0.md # Original-Pitch-Deck (vor Optimierung)
│   └── 03_Einwaende_Barrieren_Tabelle_ORIGINAL.md # Kopie der Barrieren-Tabelle
│
├── assets/                                     # Medien & Design-Assets
│   ├── images/                                # Bilder für Pitch (Personas, Diagramme, etc.)
│   └── slides/                                # PowerPoint/PDF-Versionen des Pitch Decks
│
└── versions/                                   # Zukünftige Iterationen & Varianten
    └── (leer – für spätere Versionen)
```

---

## 📄 Aktive Dokumente (Root-Ebene)

### Haupt-Workflow:

**1. Einstieg:**
- `README.md` → Schnellstart & Navigation
- `00_Executive_Summary.md` → 5-Min-Überblick

**2. Vorbereitung:**
- `01_Pitch-Deck_Bank-Version.md` → Pitch lernen & verstehen (60 Min)
- `03_Praesentationsanleitung.md` → Wie präsentieren? (40 Min)

**3. Details:**
- `02_Validierte_Statistiken_Quellen.md` → Fact-Checking
- `03_Einwaende_Barrieren_Tabelle.md` → Einwände vorbereiten

---

## 🗄️ archive/ – Historische Dokumente

**Zweck:** Versionskontrolle & Vergleich

**Was gehört rein:**
- Alte Versionen von Pitch Decks (mit Datum/Version im Dateinamen)
- Ursprüngliche Research-Dokumente (falls durch neue ersetzt)
- Verworfene Ansätze (zur Dokumentation)

**Namenskonvention:**
```
[Nummer]_[Name]_[Status]_v[Version].md

Beispiele:
- 00_Pitch-Deck_Robo4you_ORIGINAL_v0.md
- 01_Pitch-Deck_Bank-Version_v1.1_2024-12.md
- 01_Pitch-Deck_Investor-Version_DRAFT_v0.5.md
```

**Wann archivieren:**
- ✅ Alte Version wird durch neue ersetzt
- ✅ Dokument ist nicht mehr aktiv genutzt
- ✅ Für Dokumentation/Vergleich aufbewahren

**Wann NICHT archivieren:**
- ❌ Dokument wird noch aktiv genutzt (bleibt in Root)
- ❌ Dokument ist veraltet und irrelevant (löschen)

---

## 🎨 assets/ – Medien & Design

### assets/images/
**Zweck:** Bilder für Pitch Deck

**Was gehört rein:**
- Persona-Bilder (Maria, Thomas, Familie Müller)
- Diagramme (Demografische Entwicklung, Altersquotient, etc.)
- Logos (Robo4you, Partner-Logos)
- Infografiken (3 Säulen, Use Cases, etc.)
- Screenshots (Roboter-Modelle, Referenzen)

**Namenskonvention:**
```
[Folie]-[Beschreibung].[Format]

Beispiele:
- 02-persona-maria.jpg
- 02-persona-thomas.jpg
- 03-timeline-2025-2027.png
- 05-werteversprechen-diagramm.svg
- logo-robo4you.png
```

### assets/slides/
**Zweck:** Exportierte Präsentationen

**Was gehört rein:**
- PowerPoint-Versionen (.pptx)
- PDF-Versionen (zum Ausdrucken)
- Google Slides-Links (als .txt-Datei mit URL)

**Namenskonvention:**
```
Robo4you_Pitch_[Zielgruppe]_[Datum].[Format]

Beispiele:
- Robo4you_Pitch_Bank_2024-11-15.pptx
- Robo4you_Pitch_Bank_2024-11-15.pdf
- Robo4you_Pitch_Investor_2024-12-01.pptx
- Robo4you_Pitch_Partner_2025-01-10.pdf
```

---

## 🔄 versions/ – Zukünftige Iterationen

**Zweck:** Arbeitskopien & Varianten

**Was gehört rein:**
- Work-in-Progress-Versionen (während Bearbeitung)
- Varianten für andere Zielgruppen (Investoren, Partner, Kunden)
- A/B-Test-Versionen (z.B. verschiedene Ansätze für Folie 5)

**Beispiele:**
```
versions/
├── investor/
│   ├── 01_Pitch-Deck_Investor-Version_WIP.md
│   └── README_Investor-Anpassungen.md
│
├── partner/
│   ├── 01_Pitch-Deck_Partner-Version_WIP.md
│   └── README_Partner-Fokus.md
│
└── experiments/
    ├── 05_Werteversprechen_Alternative-A.md
    └── 05_Werteversprechen_Alternative-B.md
```

**Workflow:**
1. Variante in `versions/[name]/` entwickeln
2. Testen & Feedback einholen
3. Bei Erfolg: In Root verschieben (alte Version archivieren)
4. Bei Misserfolg: In `archive/` verschieben oder löschen

---

## 🚀 Arbeitsabläufe

### Workflow 1: Neues Pitch Deck erstellen (für andere Zielgruppe)

**Beispiel:** Investor-Version erstellen

1. **Kopieren:**
   ```bash
   mkdir -p versions/investor
   cp 01_Pitch-Deck_Bank-Version.md versions/investor/01_Pitch-Deck_Investor-Version_WIP.md
   ```

2. **Anpassen:**
   - Folie 5 (Werteversprechen): Mehr Skalierung, weniger Sicherheit
   - Folie 9 (Geschäftsmodell): Exit-Strategien, TAM/SAM/SOM
   - Tonalität: Mehr "Wachstum", weniger "Risikominimierung"

3. **Testen:**
   - Mit Testpublikum durchgehen
   - Feedback sammeln

4. **Finalisieren:**
   ```bash
   mv versions/investor/01_Pitch-Deck_Investor-Version_WIP.md 01_Pitch-Deck_Investor-Version.md
   ```

---

### Workflow 2: Pitch Deck aktualisieren (neue Version)

**Beispiel:** Nach Bank-Feedback iterieren

1. **Alte Version archivieren:**
   ```bash
   cp 01_Pitch-Deck_Bank-Version.md archive/01_Pitch-Deck_Bank-Version_v1.0_2024-11.md
   ```

2. **Bearbeiten:**
   - Änderungen in `01_Pitch-Deck_Bank-Version.md` vornehmen

3. **Dokumentieren:**
   - Im Executive Summary: Versions-Historie aktualisieren
   - Changelog führen (optional)

---

### Workflow 3: PowerPoint-Version erstellen

1. **Markdown → PowerPoint:**
   - `01_Pitch-Deck_Bank-Version.md` öffnen
   - Jede Folie (INHALT-Abschnitt) → PowerPoint-Folie
   - SPRECHERNOTIZEN → Notizbereich

2. **Bilder einfügen:**
   - Aus `assets/images/` verwenden

3. **Speichern:**
   ```bash
   # In PowerPoint: "Speichern unter"
   # Ort: assets/slides/
   # Name: Robo4you_Pitch_Bank_2024-11-15.pptx
   ```

4. **PDF exportieren:**
   ```bash
   # In PowerPoint: "Exportieren als PDF"
   # Ort: assets/slides/
   # Name: Robo4you_Pitch_Bank_2024-11-15.pdf
   ```

---

## 📋 Namenskonventionen (Zusammenfassung)

### Root-Dokumente (aktiv):
```
[Nummer]_[Name].md

- Nummer: 00-99 (Reihenfolge)
- Name: Beschreibend, ohne Datum
- Keine Version im Namen (immer aktuellste)

Beispiele:
✅ 01_Pitch-Deck_Bank-Version.md
✅ 02_Validierte_Statistiken_Quellen.md
❌ 01_Pitch-Deck_Bank-Version_v1.0.md (Version nur im Archiv!)
```

### Archiv-Dokumente:
```
[Nummer]_[Name]_[Status]_v[Version]_[Datum].md

- Status: ORIGINAL, DRAFT, FINAL
- Version: v0, v1.0, v1.1, v2.0
- Datum: YYYY-MM (optional, bei häufigen Updates)

Beispiele:
✅ 00_Pitch-Deck_Robo4you_ORIGINAL_v0.md
✅ 01_Pitch-Deck_Bank-Version_v1.0_2024-11.md
✅ 01_Pitch-Deck_Investor-Version_DRAFT_v0.5.md
```

### Assets:
```
Images: [Folie]-[Beschreibung].[Format]
Slides: Robo4you_Pitch_[Zielgruppe]_[Datum].[Format]
```

---

## 🔍 Was gehört WOHIN? (Entscheidungsbaum)

**Frage 1: Ist das Dokument aktuell & aktiv genutzt?**
- ✅ JA → **Root-Ebene** (pitch/)
- ❌ NEIN → Frage 2

**Frage 2: Ist es eine alte Version oder historisch relevant?**
- ✅ JA → **archive/**
- ❌ NEIN → Frage 3

**Frage 3: Ist es ein Bild oder eine exportierte Präsentation?**
- ✅ Bild → **assets/images/**
- ✅ PowerPoint/PDF → **assets/slides/**
- ❌ NEIN → Frage 4

**Frage 4: Ist es eine Work-in-Progress-Version oder Variante?**
- ✅ JA → **versions/**
- ❌ NEIN → **Löschen** (nicht relevant)

---

## 🧹 Wartung & Cleanup

### Regelmäßig (alle 3 Monate):
- [ ] Archiv durchsehen: Was kann gelöscht werden?
- [ ] versions/ aufräumen: Verworfene Experimente löschen
- [ ] assets/images/ sortieren: Ungenutzte Bilder entfernen
- [ ] README.md & STRUCTURE.md aktualisieren

### Bei großen Änderungen:
- [ ] Alte Version archivieren (mit Datum!)
- [ ] Changelog führen (optional)
- [ ] Team informieren über neue Version

---

## 📊 Beispiel-Struktur (nach 6 Monaten)

```
pitch/
│
├── README.md
├── STRUCTURE.md
├── CHANGELOG.md                                # Optional: Versionshistorie
│
├── 00_Executive_Summary.md
├── 01_Pitch-Deck_Bank-Version.md              # v2.5 (aktuell)
├── 01_Pitch-Deck_Investor-Version.md          # v1.2 (aktuell)
├── 02_Validierte_Statistiken_Quellen.md
├── 03_Praesentationsanleitung.md
├── 03_Einwaende_Barrieren_Tabelle.md
│
├── archive/
│   ├── 2024-11/
│   │   ├── 00_Pitch-Deck_Robo4you_ORIGINAL_v0.md
│   │   └── 01_Pitch-Deck_Bank-Version_v1.0.md
│   ├── 2024-12/
│   │   ├── 01_Pitch-Deck_Bank-Version_v1.5.md
│   │   └── 01_Pitch-Deck_Investor-Version_DRAFT_v0.5.md
│   └── 2025-01/
│       ├── 01_Pitch-Deck_Bank-Version_v2.0.md
│       └── 01_Pitch-Deck_Investor-Version_v1.0.md
│
├── assets/
│   ├── images/
│   │   ├── logo-robo4you.png
│   │   ├── 02-persona-maria.jpg
│   │   ├── 02-persona-thomas.jpg
│   │   ├── 07-persona-familie-mueller.jpg
│   │   ├── 03-timeline-2025-2027.png
│   │   ├── 05-pepper-beispiel.jpg
│   │   └── 11-regulierung-timeline.png
│   └── slides/
│       ├── 2024-11/
│       │   ├── Robo4you_Pitch_Bank_2024-11-15.pptx
│       │   └── Robo4you_Pitch_Bank_2024-11-15.pdf
│       ├── 2024-12/
│       │   ├── Robo4you_Pitch_Bank_2024-12-05.pptx
│       │   ├── Robo4you_Pitch_Bank_2024-12-05.pdf
│       │   └── Robo4you_Pitch_Investor_2024-12-10.pptx
│       └── 2025-01/
│           └── Robo4you_Pitch_Bank_2025-01-20.pdf
│
└── versions/
    └── partner/
        ├── 01_Pitch-Deck_Partner-Version_WIP.md
        └── README_Partner-Anpassungen.md
```

---

## ✅ Best Practices

### DO:
✅ **Root-Ebene sauber halten** (nur aktive Dokumente)
✅ **Klare Namenskonventionen** befolgen
✅ **Alte Versionen archivieren** (mit Datum!)
✅ **Assets organisieren** (Bilder, Slides getrennt)
✅ **README aktuell halten** (bei größeren Änderungen)

### DON'T:
❌ **Keine Duplikate** in Root (alt + neu gleichzeitig)
❌ **Keine Versionen im Root-Namen** (01_Pitch_v1.md ❌)
❌ **Keine "temp" oder "test" Dateien** in Root (→ versions/)
❌ **Keine unsortierten Assets** (Bilder direkt in Root ❌)
❌ **Keine toten Links** in Dokumenten (regelmäßig prüfen)

---

## 🎯 Ziel der Struktur

**Klarheit:** Jeder findet sofort das aktuelle Dokument
**Nachvollziehbarkeit:** Alte Versionen sind dokumentiert
**Skalierbarkeit:** Struktur wächst mit dem Projekt
**Professionalität:** Zeigt organisiertes Arbeiten

---

Stand: November 2024 | Version 1.0 | Erstellt für Robo4you


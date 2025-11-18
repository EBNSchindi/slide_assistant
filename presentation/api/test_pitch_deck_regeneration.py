#!/usr/bin/env python3
"""
Pitch Deck Regeneration Test
Tests the v2 agent system by regenerating slides 01-08 from the pitch deck
and comparing results with existing ground truth examples.
"""

import requests
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Dict, List, Any

# Configuration
API_BASE_URL = "http://localhost:8001"
PROJECT_NAME = "beispiel-projekt"
PROJECT_BASE_PATH = Path("/home/dani/Schreibtisch/cursor_dev/slide_assistant/presentation/projects")
PITCH_DECK_PATH = PROJECT_BASE_PATH / PROJECT_NAME / "markdown/input/pitch-deck.md"
HTML_OUTPUT_DIR = PROJECT_BASE_PATH / PROJECT_NAME / "html"
TEST_OUTPUT_DIR = PROJECT_BASE_PATH / PROJECT_NAME / "test_output"

# Ensure test output directory exists
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Test case definitions for each slide
SLIDE_CONFIGS = [
    {
        "slide_number": 1,
        "title": "Problem - Demografischer Wandel",
        "expected_components": 3,
        "expected_types": ["stat-grid", "bullet-list", "stat-grid"],
        "ground_truth": "folie-01-problem.html",
    },
    {
        "slide_number": 2,
        "title": "Lösung - Robo4you",
        "expected_components": 3,
        "expected_types": ["text", "bullet-list", "text"],
        "ground_truth": "folie-02-loesung.html",
    },
    {
        "slide_number": 3,
        "title": "Markt - Robotik-Boom",
        "expected_components": 3,
        "expected_types": ["text", "text", "stat-grid"],
        "ground_truth": "folie-03-markt.html",
    },
    {
        "slide_number": 4,
        "title": "Vergleichstabelle - Roboter-Modelle",
        "expected_components": 2,
        "expected_types": ["table", "table"],
        "ground_truth": "folie-04-tabelle.html",
    },
    {
        "slide_number": 5,
        "title": "Prozesskette - Deployment-Workflow",
        "expected_components": 2,
        "expected_types": ["process", "process-horizontal"],
        "ground_truth": "folie-05-prozesskette.html",
    },
    {
        "slide_number": 6,
        "title": "Features & Vorteile",
        "expected_components": 1,
        "expected_types": ["feature-grid"],
        "ground_truth": "folie-06-features.html",
    },
    {
        "slide_number": 7,
        "title": "Daten & Metriken",
        "expected_components": 2,
        "expected_types": ["table", "table"],
        "ground_truth": "folie-07-daten.html",
    },
    {
        "slide_number": 8,
        "title": "Bilder & Visualisierungen",
        "expected_components": 4,
        "expected_types": ["image-frame", "image-grid", "image-frame", "image-frame"],
        "ground_truth": "folie-08-bilder.html",
    },
]

# Raw content for each slide (extracted from pitch deck)
SLIDE_INPUTS = {
    1: """## Folie 1: Problem - Demografischer Wandel

### Komponente 1.1: Die Zahlen sprechen für sich

- 83,6 Mio Einwohner in Deutschland (2024)
- 5,7 Mio Pflegebedürftige (Stand 2023)
- 500.000 Fehlende Pflegekräfte bis 2030
- 16.500 Pflegeheime benötigen Unterstützung

### Komponente 1.2: Wachsende Belastung

Der Altersquotient steigt dramatisch:

- **37%** heute (37 über 67-Jährige pro 100 Erwerbsfähige)
- **>50%** bis 2040 prognostiziert

> "17 Millionen erwirtschaften für 90 Millionen"

### Komponente 1.3: Finanzielle Belastung

- 52,9% Einkommensbelastungsquote (2025)
- Mehr als die Hälfte des Einkommens geht an den Staat
- Tendenz steigend""",

    2: """## Folie 2: Lösung - Robo4you

### Komponente 2.1: Unser Konzept

**Robotik as a Service** - Wir vermieten humanoide Roboter mit umfassendem Service-Paket.

**Die drei Säulen:**

- **🤖 Hardware:** Marktführende humanoide Roboter
- **🎓 Schulung:** Robotik-Coaches für optimale Nutzung
- **🔧 Service:** Wartung, Updates, Support inklusive

### Komponente 2.2: Vorteile für Kunden

- **Kein Kapitaleinsatz:** Monatliche Miete statt 50.000-150.000 € Kaufpreis
- **Planbare Kosten:** Feste monatliche Rate, keine Überraschungen
- **Immer aktuell:** Software-Updates und Hardware-Upgrades inklusive
- **Risikofrei:** Technologie-Risiko liegt bei uns

### Komponente 2.3: Zielgruppen

**Phase 1: Institutioneller Markt (2026-2028)**

- **Pflegeheime:** 16.500 Einrichtungen
- **Bibliotheken:** 8.800 öffentliche Bibliotheken
- **Schulen:** 32.000 allgemeinbildende Schulen

**Phase 2: Privater Markt (ab 2029)**

- **Haushalte:** ~15 Mio Zielgruppe (Sandwich-Generation)
- Konservatives Szenario: 1% Penetration = 150.000 Haushalte""",

    3: """## Folie 3: Markt - Robotik-Boom

### Komponente 3.1: Marktreife Modelle (2025)

Erste humanoide Roboter sind bereits verfügbar:

- ~84.000 € - Unitree H1 (High-End, Industrie)
- ~18.500 € - 1X NEO (Service-Roboter)
- ~15.000 € - Unitree G1 (Bildung/Forschung)
- ~5.100 € - Unitree R1 (Entry-Level)

### Komponente 3.2: Referenz-Deployments

**GXO × Agility Robotics**

Erster kommerzieller Dauerbetrieb von humanoiden Robotern in der Logistik (Atlanta, seit Juni 2024).

**BMW × Figure AI**

Humanoide Roboter im Produktionseinsatz (Spartanburg, 2024).

**Neura Robotics**

Deutscher Hersteller, Serienstart Ende 2025 angekündigt (IFA 2025).

### Komponente 3.3: Marktprognosen

- 18.000 Einheiten weltweit in 2025 (Bank of America)
- >1 Mrd. Roboter bis 2050 (Morgan Stanley)
- $5 Billionen Marktvolumen bis 2050

> "Die nächste industrielle Revolution hat bereits begonnen\"""",

    4: """## Folie 4: Vergleichstabelle - Roboter-Modelle

### Komponente 4.1: Roboter-Modell Vergleich

| Modell | Preis | Einsatzbereich | Verfügbarkeit |
|--------|-------|----------------|---------------|
| Unitree H1 | ~84.000 € | Industrie, Forschung | Verfügbar |
| 1X NEO | ~18.500 € | Service, Haushalt | 2026 |
| Unitree G1 | ~15.000 € | Bildung, Forschung | Verfügbar |
| Unitree R1 | ~5.100 € | Entry-Level, Entwicklung | Verfügbar |
| Neura 4NE-1 | <50.000 € | Industrie, Service | Ende 2025 |

### Komponente 4.2: Geschäftsmodell Vergleich

| Kriterium | Kauf | Miete (Robo4you) |
|-----------|------|------------------|
| Anschaffungskosten | 50.000 - 150.000 € | 0 € |
| Monatliche Kosten | Wartung: ~500 € | 2.500 - 4.500 € (alles inkl.) |
| Updates & Upgrades | Zusätzliche Kosten | Inklusive |
| Risiko | Beim Kunden | Bei Robo4you |
| Flexibilität | Gering | Hoch (kündbar) |""",

    5: """## Folie 5: Prozesskette - Deployment-Workflow

### Komponente 5.1: Vertikale Prozesskette

1. **Bedarfserhebung**
   Analyse der Anforderungen und Einsatzbereiche beim Kunden

2. **Roboter-Auswahl**
   Passendes Modell basierend auf Anforderungen und Budget

3. **Installation & Setup**
   Vor-Ort Installation und erste Konfiguration durch unsere Techniker

4. **Schulung & Training**
   Umfassende Schulung der Mitarbeiter durch Robotik-Coaches

5. **Betrieb & Support**
   Kontinuierlicher Support, Wartung und Updates während der Laufzeit

### Komponente 5.2: Horizontale Prozesskette

1. Kontakt - Erstgespräch
2. Analyse - Bedarf prüfen
3. Angebot - Kosten kalkulieren
4. Deployment - Installation
5. Betrieb - Support & Wartung""",

    6: """## Folie 6: Features & Vorteile

### Komponente 6.1: Unsere Service-Features

- **🤖 Hardware**
  Marktführende humanoide Roboter von etablierten Herstellern. Regelmäßige Hardware-Upgrades inklusive.

- **🎓 Schulung**
  Umfassende Schulungen durch zertifizierte Robotik-Coaches. Initial-Training und fortlaufende Weiterbildung.

- **🔧 Wartung**
  Proaktive Wartung und Reparaturen durch unser Service-Team. Minimale Ausfallzeiten garantiert.

- **📱 Software-Updates**
  Automatische Software-Updates und neue Features. Immer auf dem neuesten Stand der Technik.

- **📞 Support**
  24/7 Support-Hotline für kritische Fragen. Schnelle Reaktionszeiten bei Problemen.

- **🔄 Flexibilität**
  Monatlich kündbar, keine langfristigen Verträge. Anpassung der Anzahl der Roboter möglich.""",

    7: """## Folie 7: Daten & Metriken

### Komponente 7.1: Unit Economics

| Position | Monatlich | Jährlich |
|----------|-----------|----------|
| Mieteinnahmen | 3.500 € | 42.000 € |
| Finanzierung/Abschreibung | -800 € | -9.600 € |
| Wartung & Support | -400 € | -4.800 € |
| Versicherung | -200 € | -2.400 € |
| Robotik-Coach (anteilig) | -300 € | -3.600 € |
| **Deckungsbeitrag** | **1.800 €** | **21.600 €** |

**Break-Even:** Nach 17 Monaten | **Deckungsbeitrag:** 51%

### Komponente 7.2: Wachstumsprognose

| Jahr | Roboter | ARR | EBITDA |
|------|---------|-----|--------|
| 2026 | 50 | 1,5 Mio € | -500.000 € |
| 2027 | 150 | 4,5 Mio € | 1,2 Mio € |
| 2028 | 300 | 9 Mio € | 3,5 Mio € |
| 2029 | 500 | 15 Mio € | 6 Mio € |
| 2030 | 2.500 | 75 Mio € | 25 Mio € |""",

    8: """## Folie 8: Bilder & Visualisierungen

### Komponente 8.1: Einzelnes Bild mit Rahmen

![Unitree H1 - High-End Roboter](images/unitree-h1.jpg)

**Unitree H1 - High-End Roboter**

Der Unitree H1 ist ein humanoider Roboter für industrielle Anwendungen. Mit einer Höhe von 1,80m und 47 kg Gewicht bietet er beeindruckende Bewegungsfähigkeiten und kann Lasten bis zu 30 kg tragen.

### Komponente 8.2: Bild-Grid (mehrere Bilder)

![Unitree H1](images/unitree-h1.jpg) - **Unitree H1** - High-End Industrie-Roboter [Status: Verfügbar]

![1X NEO](images/1x-neo.jpg) - **1X NEO** - Service-Roboter für Haushalt [Status: 2026]

![Unitree G1](images/unitree-g1.jpg) - **Unitree G1** - Bildung & Forschung [Status: Verfügbar]

### Komponente 8.3: Referenz-Deployment

![GXO × Agility Robotics Deployment](images/gxo-agility.jpg)

**Erster kommerzieller Dauerbetrieb**

GXO Logistics und Agility Robotics haben im Juni 2024 den ersten kommerziellen Dauerbetrieb von humanoiden Robotern in einem Lager nahe Atlanta gestartet. Die Digit-Roboter unterstützen bei der Materialhandhabung und Logistik.

**Standort:** Atlanta, USA | **Start:** Juni 2024 | **Status:** Aktiv

### Komponente 8.4: Roboter im Einsatz

![Roboter in Pflegeeinrichtung](images/roboter-pflege.jpg)

**Einsatz in Pflegeheimen**

Humanoide Roboter unterstützen Pflegekräfte bei alltäglichen Aufgaben wie Materialtransport, Patientenbetreuung und Dokumentation. Dies entlastet das Personal und ermöglicht mehr Zeit für die direkte Pflege.

- Materialtransport zwischen Stationen
- Unterstützung bei der Patientenbetreuung
- Dokumentationshilfe
- 24/7 Verfügbarkeit""",
}


def extract_component_info(html: str) -> Dict[str, Any]:
    """Extract component information from HTML"""
    soup = BeautifulSoup(html, 'html.parser')

    components = []
    for comp in soup.find_all('div', class_='component'):
        comp_id = comp.get('id', 'unknown')
        # Try to detect component type from class or content
        if comp.find('div', class_='stat-grid'):
            comp_type = 'stat-grid'
        elif comp.find('ul', class_='bullet-list'):
            comp_type = 'bullet-list'
        elif comp.find('table'):
            comp_type = 'table'
        elif comp.find('div', class_='process-chain'):
            comp_type = 'process'
        elif comp.find('div', class_='process-horizontal'):
            comp_type = 'process-horizontal'
        elif comp.find('div', class_='feature-grid'):
            comp_type = 'feature-grid'
        elif comp.find('div', class_='image-grid'):
            comp_type = 'image-grid'
        elif comp.find('div', class_='image-frame') or comp.find('div', class_='image-container'):
            comp_type = 'image-frame'
        else:
            comp_type = 'text'

        components.append({
            'id': comp_id,
            'type': comp_type
        })

    return {
        'component_count': len(components),
        'component_types': [c['type'] for c in components],
        'components': components
    }


def regenerate_slide(slide_number: int, user_input: str, title: str) -> Dict[str, Any]:
    """Regenerate a single slide via API"""
    request_body = {
        "project_name": PROJECT_NAME,
        "slide_number": slide_number,
        "user_input": user_input,
        "slide_title": title,
        "theme": "github",
        "language": "de"
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v2/generate",
            json=request_body,
            timeout=60
        )

        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json(),
                "error": None
            }
        else:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


def compare_html_structures(generated_html: str, ground_truth_html: str) -> Dict[str, Any]:
    """Compare generated HTML with ground truth"""
    generated_info = extract_component_info(generated_html)
    ground_truth_info = extract_component_info(ground_truth_html)

    comparison = {
        "component_count_match": generated_info['component_count'] == ground_truth_info['component_count'],
        "generated_count": generated_info['component_count'],
        "expected_count": ground_truth_info['component_count'],
        "component_types_match": generated_info['component_types'] == ground_truth_info['component_types'],
        "generated_types": generated_info['component_types'],
        "expected_types": ground_truth_info['component_types'],
    }

    return comparison


def main():
    """Main test runner"""
    print("=" * 80)
    print("Pitch Deck Regeneration Test")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"API URL: {API_BASE_URL}")
    print(f"Project: {PROJECT_NAME}")
    print()

    # Test API connectivity
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ API health check failed!")
            return 1
        print("✅ API is running\n")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return 1

    results = []

    # Process each slide
    for config in SLIDE_CONFIGS:
        slide_num = config["slide_number"]
        title = config["title"]
        user_input = SLIDE_INPUTS[slide_num]
        ground_truth_file = HTML_OUTPUT_DIR / config["ground_truth"]

        print(f"Processing Slide {slide_num:02d}: {title}")
        print("-" * 80)

        # Regenerate slide
        print(f"  Calling API...")
        result = regenerate_slide(slide_num, user_input, title)

        if not result["success"]:
            print(f"  ❌ Generation failed: {result['error']}")
            results.append({
                "slide_number": slide_num,
                "title": title,
                "success": False,
                "error": result["error"],
                "comparison": None
            })
            print()
            continue

        response_data = result["data"]
        generated_html = response_data.get("html", "")
        iteration_count = response_data.get("iteration_count", 0)
        components = response_data.get("formatted_slide", {}).get("components", [])

        print(f"  ✅ Generation successful (iterations: {iteration_count})")
        print(f"  Components generated: {len(components)}")

        # Save generated HTML to test output
        test_output_file = TEST_OUTPUT_DIR / f"test_folie_{slide_num:02d}_{title.lower().replace(' ', '-')}.html"
        with open(test_output_file, 'w', encoding='utf-8') as f:
            f.write(generated_html)
        print(f"  Saved to: {test_output_file.name}")

        # Compare with ground truth
        if ground_truth_file.exists():
            print(f"  Comparing with ground truth...")
            with open(ground_truth_file, 'r', encoding='utf-8') as f:
                ground_truth_html = f.read()

            comparison = compare_html_structures(generated_html, ground_truth_html)

            # Validate expectations
            component_count_ok = len(components) == config["expected_components"]

            status = "✅" if component_count_ok else "⚠️"
            print(f"  {status} Components: {len(components)} (expected: {config['expected_components']})")

            print(f"  Generated types: {[c.get('type', 'unknown') for c in components]}")
            print(f"  Expected types:  {config['expected_types']}")

            results.append({
                "slide_number": slide_num,
                "title": title,
                "success": True,
                "component_count": len(components),
                "expected_count": config["expected_components"],
                "component_types": [c.get('type', 'unknown') for c in components],
                "expected_types": config["expected_types"],
                "component_count_ok": component_count_ok,
                "comparison": comparison,
                "iteration_count": iteration_count,
                "error": None
            })
        else:
            print(f"  ⚠️ Ground truth file not found: {ground_truth_file}")
            results.append({
                "slide_number": slide_num,
                "title": title,
                "success": True,
                "component_count": len(components),
                "expected_count": config["expected_components"],
                "component_types": [c.get('type', 'unknown') for c in components],
                "expected_types": config["expected_types"],
                "comparison": None,
                "iteration_count": iteration_count,
                "error": "Ground truth not found"
            })

        print()

    # Generate report
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    successful_regenerations = sum(1 for r in results if r.get("success"))
    total_slides = len(SLIDE_CONFIGS)
    component_count_matches = sum(1 for r in results if r.get("component_count_ok", False))

    print(f"\nRegeneration Success Rate: {successful_regenerations}/{total_slides}")
    print(f"Component Count Matches: {component_count_matches}/{total_slides}")

    print("\nDetailed Results:")
    print("-" * 80)
    for result in results:
        status = "✅" if result.get("success") else "❌"
        slide = result["slide_number"]
        title = result["title"]
        count = result.get("component_count", "?")
        expected = result.get("expected_count", "?")
        iterations = result.get("iteration_count", "?")

        print(f"{status} Slide {slide:02d}: {title}")
        print(f"   Components: {count}/{expected} | Iterations: {iterations}")
        if result.get("error"):
            print(f"   Error: {result['error']}")

    # Save detailed report
    report_file = TEST_OUTPUT_DIR / "comparison_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "api_url": API_BASE_URL,
            "project": PROJECT_NAME,
            "total_slides": total_slides,
            "successful": successful_regenerations,
            "component_matches": component_count_matches,
            "results": results
        }, f, indent=2, ensure_ascii=False)

    print(f"\nDetailed report saved to: {report_file}")
    print()

    return 0 if successful_regenerations == total_slides else 1


if __name__ == "__main__":
    sys.exit(main())

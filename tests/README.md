# Test Suite Documentation

## Übersicht

Dieses Projekt verfügt über eine umfassende Test-Suite mit Unit-Tests, Integrationstests und API-Tests.

## Test-Struktur

```
tests/
├── __init__.py
├── conftest.py                      # Shared fixtures und pytest-Konfiguration
├── README.md                        # Diese Datei
├── unit/                            # Unit-Tests für einzelne Komponenten
│   ├── test_agents.py               # Tests für Agent-Klassen
│   ├── test_file_service.py         # Tests für FileService
│   ├── test_project_service.py      # Tests für ProjectService
│   └── test_variants.py             # Tests für Varianten-Feature
├── integration/                     # Integrationstests
│   └── test_agents_integration.py   # End-to-End Agent-Pipeline Tests
└── api/                             # API Endpoint Tests
    └── test_endpoints.py            # FastAPI Endpoint Tests
```

## Test-Ausführung

### Alle Tests ausführen

```bash
pytest tests/
```

### Spezifische Test-Kategorien

```bash
# Nur Unit-Tests
pytest tests/unit/ -v

# Nur Integrationstests
pytest tests/integration/ -v

# Nur API-Tests
pytest tests/api/ -v

# Tests mit Coverage-Report
pytest tests/ --cov=presentation --cov-report=html

# Schnelle Tests (ohne slow marker)
pytest tests/ -m "not slow"

# Nur Tests die Mock-Agents verwenden
pytest tests/ -m "mock"
```

### Test-Marker

Die Tests verwenden folgende Pytest-Marker:

- `@pytest.mark.unit` - Unit-Tests (isolierte Komponententests)
- `@pytest.mark.integration` - Integrationstests (mehrere Komponenten)
- `@pytest.mark.api` - API Endpoint Tests
- `@pytest.mark.slow` - Langsam laufende Tests
- `@pytest.mark.requires_api_key` - Tests die OPENAI_API_KEY benötigen
- `@pytest.mark.mock` - Tests die Mock-Agents verwenden

## Test-Coverage

**Aktueller Stand:** 45% Code-Coverage

### Coverage nach Modul:

- **FileService:** 85%
- **ProjectService:** 89%
- **ContentAnalyzerAgent:** 60%
- **AgentOrchestrator:** 47%
- **PresentationStrategistAgent:** 30%
- **ContentGeneratorAgent:** 16%
- **StyleParser:** 79%
- **VariantStyleParser:** 58%

## Fixtures

Die wichtigsten Fixtures befinden sich in `conftest.py`:

- `project_root` - Projekt-Root-Verzeichnis
- `temp_project_dir` - Temporäres Test-Projektverzeichnis
- `mock_api_key` - Mock API-Key für Tests
- `test_mode` - Aktiviert TEST_MODE (Mock-Agents)
- `sample_markdown_content` - Beispiel-Markdown-Content
- `sample_html_content` - Beispiel-HTML-Content
- `sample_style_guide` - Beispiel-Style-Guide
- `sample_analysis` - Beispiel-Content-Analyse
- `sample_strategy` - Beispiel-Präsentationsstrategie

## Bekannte Probleme

### API Endpoint Tests

Die API Endpoint Tests (`tests/api/test_endpoints.py`) haben derzeit ein Kompatibilitätsproblem mit der starlette TestClient-Version (0.27.0).

**Problem:** `TypeError: Client.__init__() got an unexpected keyword argument 'app'`

**Workaround:** Tests können manuell mit httpx ausgeführt werden oder die starlette-Version muss aktualisiert werden.

**Status:** 45/59 Tests bestanden (API-Tests ausgeschlossen)

## Test-Entwicklung

### Neue Tests hinzufügen

1. Erstelle eine neue Test-Datei in der passenden Kategorie (unit/integration/api)
2. Importiere benötigte Fixtures aus `conftest.py`
3. Verwende die passenden Pytest-Marker
4. Folge dem bestehenden Test-Pattern

**Beispiel:**

```python
import pytest
from presentation.api.services import FileService


@pytest.mark.unit
class TestMyFeature:
    """Test MyFeature class"""

    def test_basic_functionality(self, temp_project_dir):
        """Test basic functionality"""
        # Arrange
        service = FileService(str(temp_project_dir))

        # Act
        result = service.some_method()

        # Assert
        assert result is not None
```

### Test-Best-Practices

1. **AAA-Pattern verwenden:** Arrange, Act, Assert
2. **Aussagekräftige Namen:** `test_should_save_file_when_valid_input`
3. **Isolierte Tests:** Jeder Test sollte unabhängig laufen
4. **Fixtures nutzen:** Wiederverwendbare Test-Daten in conftest.py
5. **Marker setzen:** Kategorisierung mit @pytest.mark.*
6. **Docstrings:** Kurze Beschreibung was der Test prüft

## CI/CD Integration

Die Tests können in CI/CD Pipelines integriert werden:

```yaml
# Beispiel GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install -r presentation/api/requirements.txt
    pip install pytest pytest-cov pytest-asyncio httpx
    pytest tests/unit/ tests/integration/ -v --cov=presentation
```

## Troubleshooting

### ImportError: No module named 'openai'

**Lösung:** Installiere API-Dependencies:
```bash
pip install -r presentation/api/requirements.txt
```

### Tests mit OPENAI_API_KEY

Einige Integrationstests können mit echtem API-Key ausgeführt werden:

```bash
export OPENAI_API_KEY=sk-...
pytest tests/integration/test_agents_integration.py::test_with_real_api
```

Ohne API-Key werden diese Tests übersprungen (skipped).

### TEST_MODE

Für lokale Entwicklung ohne API-Kosten:

```bash
export TEST_MODE=true
pytest tests/
```

Dies verwendet Mock-Agents statt echte OpenAI API-Calls.

## Weiterentwicklung

### Fehlende Tests

Folgende Bereiche benötigen noch zusätzliche Tests:

- [ ] StyleParser vollständige Coverage
- [ ] VariantStyleParser Edge-Cases
- [ ] ContentGeneratorAgent erweiterte Tests
- [ ] PresentationStrategistAgent erweiterte Tests
- [ ] API Endpoint Integration Tests (nach starlette-Fix)
- [ ] Error-Handling-Szenarien
- [ ] Performance-Tests für große Dateien

### Verbesserungsmöglichkeiten

1. Erhöhung der Code-Coverage auf 80%+
2. Mehr End-to-End Szenarien
3. Performance-Benchmarks
4. Load-Testing für API
5. Security-Tests für File-Upload
6. Regression-Tests für Bug-Fixes

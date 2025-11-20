# Testing Guide - Slide Assistant

Comprehensive testing documentation for the V2 architecture.

## Test Suite Overview

Location: `presentation/api/tests/`

All tests are organized in the `tests/` subdirectory with 11 test files covering different aspects of the V2 system.

## Test Files

### Core V2 Tests

#### 1. `test_agents_v2.py`
**Purpose:** Unit tests for V2 agent system

**Tests:**
- ContentAnalyzerAgentV2 functionality
- PresentationStrategistAgentV2 logic
- ContentGeneratorAgentV2 output
- Agent parameter handling (reasoning_effort, verbosity)
- Language auto-detection (German/English)

**Run:**
```bash
cd presentation/api
python3 -m pytest tests/test_agents_v2.py -v
```

#### 2. `test_v2_integration.py`
**Purpose:** Full V2 pipeline integration tests

**Tests:**
- End-to-end agent orchestration
- Agent 1 → Agent 2 → Agent 3 → Renderer flow
- FormattedSlide generation
- HTML output validation
- Feedback loop between Agent 2 ↔ Agent 3

**Run:**
```bash
export TEST_MODE=true
python3 -m pytest tests/test_v2_integration.py -v
```

#### 3. `test_v2_mock_flow.py`
**Purpose:** Mock agent testing (TEST_MODE)

**Tests:**
- Mock agent initialization
- Mock agent responses
- TEST_MODE vs production mode switching
- Mock data structures match real agents

**Run:**
```bash
export TEST_MODE=true
python3 -m pytest tests/test_v2_mock_flow.py -v
```

### Template & Rendering Tests

#### 4. `test_renderer_fix.py`
**Purpose:** Component renderer testing

**Tests:**
- Jinja2 template rendering
- All 10 component types:
  - stat-grid
  - bullet-list
  - quote
  - text
  - table
  - image-frame
  - image-grid
  - feature-grid
  - process
  - process-horizontal
- Theme application
- HTML output validation

**Run:**
```bash
python3 -m pytest tests/test_renderer_fix.py -v

# Test specific component
python3 -m pytest tests/test_renderer_fix.py::test_stat_grid -v
```

#### 5. `test_template_system.py`
**Purpose:** Template loader and system tests

**Tests:**
- Template discovery
- Template loading from `presentation/templates/`
- Template syntax validation
- Component wrapper templates
- Slide section templates

**Run:**
```bash
python3 -m pytest tests/test_template_system.py -v
```

### Table Support Tests

#### 6. `test_table_support.py`
**Purpose:** Markdown table detection and parsing

**Tests:**
- Table pattern recognition
- Markdown table → component conversion
- Header/row parsing
- Table data structure validation

**Run:**
```bash
python3 -m pytest tests/test_table_support.py -v
```

#### 7. `test_table_end_to_end.py`
**Purpose:** Complete table generation workflow

**Tests:**
- User input with tables → FormattedSlide
- Agent 1 table detection
- Agent 2 table component strategy
- Agent 3 table data generation
- Renderer table HTML output

**Run:**
```bash
export TEST_MODE=true
python3 -m pytest tests/test_table_end_to_end.py -v
```

#### 8. `test_v2_table_generation.py`
**Purpose:** V2-specific table generation features

**Tests:**
- Table generation with V2 architecture
- Table + other components on same slide
- Multi-line table cells
- Table styling with themes

**Run:**
```bash
export TEST_MODE=true
python3 -m pytest tests/test_v2_table_generation.py -v
```

### Semantic Framework Tests

#### 9. `test_semantic_e2e_gpt4o.py`
**Purpose:** End-to-end semantic tests with real GPT-4o API

**Tests:**
- Real OpenAI API integration
- Content semantic classification
- Multi-component slide generation
- Language detection with real model
- Production-like scenarios

**Requirements:** Valid OPENAI_API_KEY

**Run:**
```bash
export TEST_MODE=false
python3 -m pytest tests/test_semantic_e2e_gpt4o.py -v
```

**⚠️ Warning:** This test makes real API calls and incurs costs!

#### 10. `test_semantic_live.py`
**Purpose:** Live semantic framework testing

**Tests:**
- Semantic content block detection
- Content-type classification (narrative, stats, list, etc.)
- Semantic → component type mapping
- Multi-language semantic analysis

**Run:**
```bash
export TEST_MODE=true
python3 -m pytest tests/test_semantic_live.py -v
```

### Integration Tests

#### 11. `test_pitch_deck_regeneration.py`
**Purpose:** Full pitch deck regeneration testing

**Tests:**
- Regenerates 8 slides from beispiel-projekt
- Compares against reference slides
- Tests all component types in realistic scenarios
- Validates consistency across regenerations
- Tests:
  - Folie 1: Problem statement
  - Folie 2: Solution overview
  - Folie 3: Market analysis
  - Folie 4: Comparison table
  - Folie 5: Process flow
  - Folie 6: Features (feature-grid)
  - Folie 7: Data/metrics (stat-grid)
  - Folie 8: Images

**Run:**
```bash
export TEST_MODE=true
python3 -m pytest tests/test_pitch_deck_regeneration.py -v

# Test specific slide
python3 -m pytest tests/test_pitch_deck_regeneration.py::test_slide_06 -v
```

## Running Tests

### Quick Start

```bash
# Run all tests (mock mode)
cd presentation/api
export TEST_MODE=true
python3 -m pytest tests/ -v
```

### Test Modes

#### 1. Mock Mode (Recommended for Development)

```bash
# Fast, no API costs, reproducible
export TEST_MODE=true
python3 -m pytest tests/ -v
```

**Advantages:**
- ✅ No OpenAI API key needed
- ✅ Fast execution (~30 seconds for full suite)
- ✅ No API costs
- ✅ Deterministic results
- ✅ Works offline

**Disadvantages:**
- ❌ Uses mock data, not real AI responses
- ❌ May miss real API issues

#### 2. Production Mode (Real API)

```bash
# Requires API key, makes real calls, incurs costs
export TEST_MODE=false
export OPENAI_API_KEY=sk-...
python3 -m pytest tests/test_semantic_e2e_gpt4o.py -v
```

**Advantages:**
- ✅ Tests real API integration
- ✅ Validates actual LLM behavior
- ✅ Catches API-specific issues

**Disadvantages:**
- ❌ Requires valid API key
- ❌ Incurs OpenAI costs (~$0.10-0.50 per full suite run)
- ❌ Slower execution (~2-5 minutes)
- ❌ Non-deterministic (LLM outputs vary)

### Selective Testing

```bash
# Run specific test file
python3 -m pytest tests/test_renderer_fix.py -v

# Run specific test function
python3 -m pytest tests/test_renderer_fix.py::test_stat_grid -v

# Run tests matching pattern
python3 -m pytest tests/ -k "table" -v

# Run tests in parallel (faster)
python3 -m pytest tests/ -n auto -v
```

### Test Output Verbosity

```bash
# Minimal output
python3 -m pytest tests/

# Verbose output
python3 -m pytest tests/ -v

# Very verbose (show print statements)
python3 -m pytest tests/ -vv -s

# Show test duration
python3 -m pytest tests/ -v --durations=10
```

## Test Coverage

```bash
# Install coverage tool
pip install pytest-cov

# Run with coverage report
python3 -m pytest tests/ --cov=presentation/api --cov-report=html

# View coverage report
# Open: htmlcov/index.html
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          cd presentation/api
          pip install -r requirements.txt
          pip install pytest

      - name: Run tests (mock mode)
        run: |
          cd presentation/api
          export TEST_MODE=true
          python3 -m pytest tests/ -v
```

## Writing New Tests

### Test Template

```python
"""
Test description here.
"""
import pytest
from presentation.api.agents.content_analyzer_v2 import ContentAnalyzerAgentV2

def test_my_feature():
    """Test specific feature."""
    # Arrange
    agent = ContentAnalyzerAgentV2(project_name="beispiel-projekt")
    input_text = "Test input"

    # Act
    result = agent.analyze(input_text)

    # Assert
    assert result is not None
    assert result.language == "en"
```

### Pytest Fixtures

```python
@pytest.fixture
def sample_user_input():
    """Fixture for common test data."""
    return {
        "text": "Test content",
        "language": "de",
        "slide_number": 1
    }

def test_with_fixture(sample_user_input):
    """Use fixture in test."""
    assert sample_user_input["language"] == "de"
```

## Test Best Practices

### 1. Use TEST_MODE for Unit Tests

```python
# Good - fast, deterministic
export TEST_MODE=true
python3 -m pytest tests/test_agents_v2.py -v

# Avoid - slow, costs money
export TEST_MODE=false
python3 -m pytest tests/test_agents_v2.py -v
```

### 2. Isolate Tests

```python
# Good - each test is independent
def test_feature_a():
    agent = create_agent()  # Fresh instance
    result = agent.process("input")
    assert result.valid

def test_feature_b():
    agent = create_agent()  # Fresh instance
    result = agent.process("input")
    assert result.complete

# Avoid - shared state
agent = create_agent()  # Global

def test_feature_a():
    result = agent.process("input_a")  # Mutates global

def test_feature_b():
    result = agent.process("input_b")  # Depends on test_feature_a
```

### 3. Use Descriptive Test Names

```python
# Good - clear what's being tested
def test_stat_grid_renders_with_three_statistics():
    ...

def test_language_detection_identifies_german_text():
    ...

# Avoid - unclear
def test_render():
    ...

def test_language():
    ...
```

### 4. Test Edge Cases

```python
def test_empty_input():
    """Test behavior with empty input."""
    ...

def test_very_long_input():
    """Test behavior with 10,000 character input."""
    ...

def test_special_characters():
    """Test behavior with emoji, unicode, etc."""
    ...
```

## Troubleshooting Tests

### Common Issues

#### 1. ModuleNotFoundError

```bash
# Error: ModuleNotFoundError: No module named 'presentation'
# Solution: Run from presentation/ directory, not presentation/api/
cd presentation
python3 -m pytest api/tests/ -v
```

#### 2. OPENAI_API_KEY not found

```bash
# Error: OPENAI_API_KEY not found
# Solution: Set TEST_MODE or add API key
export TEST_MODE=true
# OR
export OPENAI_API_KEY=sk-...
```

#### 3. Template not found

```bash
# Error: TemplateNotFound: stat-grid.html.j2
# Solution: Ensure templates/ directory exists at correct location
ls presentation/templates/components/  # Should show .j2 files
```

#### 4. Import errors with __init__.py

```bash
# Error: cannot import name 'SlideBlueprintGenerator'
# Solution: Ensure __init__.py exists in schemas/
touch presentation/api/schemas/__init__.py
touch presentation/api/tests/__init__.py
```

## Test Maintenance

### Regular Updates

1. **After adding new component type:**
   - Add test in `test_renderer_fix.py`
   - Add template test in `test_template_system.py`

2. **After modifying agent:**
   - Update `test_agents_v2.py`
   - Update `test_v2_integration.py`
   - Run full regression: `pytest tests/ -v`

3. **Before releasing:**
   - Run full test suite in TEST_MODE
   - Run semantic tests with real API
   - Check test coverage (aim for >80%)

### Deprecating Tests

When removing V1 code:
1. Mark tests with `@pytest.mark.skip(reason="V1 deprecated")`
2. After 1 release cycle, delete test file
3. Update this documentation

## Further Reading

- **pytest documentation:** https://docs.pytest.org/
- **V2_ARCHITECTURE.md:** Detailed V2 system architecture
- **CLAUDE.md:** Full project documentation
- **presentation/api/README.md:** API-specific testing section

## Support

For test failures:
1. Check this guide for common issues
2. Review test output for specific error
3. Enable verbose mode: `-vv -s`
4. Open GitHub issue with full test output

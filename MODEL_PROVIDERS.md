# Model Providers - Multi-Model Support

Dokumentation für die Verwendung verschiedener LLM-Provider (OpenAI, Anthropic Claude) im Slide Assistant.

## Übersicht

Das System unterstützt mehrere LLM-Provider für die Content-Generierung:

1. **OpenAI** (GPT-4o, GPT-5, GPT-5-mini) - **Fully Implemented ✅**
2. **Anthropic Claude** (Claude 3.5 Sonnet) - **Prepared, Not Yet Implemented ⚠️**

## OpenAI (Fully Supported)

### Verfügbare Modelle

- **GPT-4o**: Standard-Modell, beste Balance zwischen Qualität und Geschwindigkeit
- **GPT-5**: Neuestes Modell mit erweiterten Reasoning-Capabilities
- **GPT-5-mini**: Kostengünstigere Variante für einfachere Aufgaben

### Setup

1. **API Key erhalten:**
   - Besuche https://platform.openai.com/api-keys
   - Erstelle einen neuen API Key

2. **.env konfigurieren:**
   ```bash
   cd presentation/api
   cp .env.example .env
   ```

   Editiere `.env`:
   ```env
   OPENAI_API_KEY=sk-your-key-here
   TEST_MODE=false
   DEFAULT_MODEL=gpt-4o
   MODEL_PROVIDER=openai
   ```

3. **Server starten:**
   ```bash
   cd presentation
   python3 run_api.py
   ```

### Model-spezifische Features

#### GPT-5 Advanced Controls

GPT-5 unterstützt zusätzliche Parameter für bessere Kontrolle:

- **reasoning_effort**: `minimal | low | medium | high`
  - Höhere Werte = mehr Reasoning-Time, bessere Qualität, höhere Kosten
  - Standard: `medium`

- **verbosity**: `minimal | low | medium | high`
  - Kontrolle über Output-Länge
  - Standard: `medium`

**Verwendung im Code:**
```python
from presentation.api.agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(
    project_name="beispiel-projekt",
    model="gpt-5",
    reasoning_effort="high",  # Für komplexe Slides
    verbosity="low",          # Für kürzere Outputs
    use_structured_outputs=True
)

result = orchestrator.generate_slide(
    user_input="...",
    slide_title="Folie 12",
    slide_number=12,
    theme="apple"
)
```

### Kosten-Optimierung

**Cost-Saving Strategies:**

1. **Verwende GPT-5-mini für einfache Slides:**
   ```env
   DEFAULT_MODEL=gpt-5-mini
   ```

2. **Reduziere reasoning_effort:**
   ```python
   reasoning_effort="low"  # Statt "high"
   ```

3. **Nutze TEST_MODE für Entwicklung:**
   ```env
   TEST_MODE=true  # Keine API-Kosten
   ```

## Anthropic Claude (Prepared)

### Status: ⚠️ Infrastruktur vorbereitet, Agents noch nicht implementiert

Die Grundlage für Anthropic Claude Support ist vorhanden:
- ✅ API Key wird in `config.py` gelesen
- ✅ `anthropic` Package in `requirements.txt`
- ✅ Model-Provider Mapping in `config.py`
- ✅ **Claude Sonnet 4.5 Support konfiguriert**
- ❌ Agent-Wrapper noch nicht implementiert

### Setup (Wenn implementiert)

1. **API Key erhalten:**
   - Besuche https://console.anthropic.com/
   - Erstelle einen API Key

2. **.env konfigurieren:**
   ```env
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   MODEL_PROVIDER=anthropic
   DEFAULT_MODEL=claude-sonnet-4.5-20250514
   ```

3. **Dependency installieren:**
   ```bash
   cd presentation/api
   pip install -r requirements.txt  # Installiert anthropic==0.40.0
   ```

### Verfügbare Modelle (Geplant)

- **claude-sonnet-4.5-20250514**: Neuestes Claude Sonnet 4.5 Modell (empfohlen)
- **claude-sonnet-4.5**: Alias für Claude Sonnet 4.5
- **claude-4.5-sonnet**: Alternativer Alias
- **claude-3-5-sonnet-20241022**: Claude 3.5 Sonnet (ältere Version)
- **claude-3-5-sonnet**: Alias für Claude 3.5 Sonnet

### Implementation TODO

Um Anthropic Support zu vervollständigen, müssen folgende Dateien erstellt werden:

1. **agents/content_analyzer_anthropic.py**
   ```python
   from anthropic import Anthropic

   class ContentAnalyzerAgentAnthropic:
       def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
           self.client = Anthropic(api_key=api_key)
           self.model = model

       def analyze(self, user_input: str, slide_title: str = None):
           # Ähnlich wie OpenAI-Version, aber mit Anthropic API
           response = self.client.messages.create(
               model=self.model,
               max_tokens=2048,
               system=self.system_prompt,
               messages=[{"role": "user", "content": user_input}]
           )
           # Parse und return analysis result
   ```

2. **agents/presentation_strategist_anthropic.py**
3. **agents/content_generator_anthropic.py**

4. **orchestrator.py Update:**
   ```python
   from config import MODEL_PROVIDER, MODEL_TO_PROVIDER

   # Dynamic import basierend auf Model Provider
   provider = MODEL_TO_PROVIDER.get(model, MODEL_PROVIDER)

   if provider == "anthropic":
       from .content_analyzer_anthropic import ContentAnalyzerAgentAnthropic as ContentAnalyzerAgent
   else:
       from .content_analyzer_v2 import ContentAnalyzerAgentV2 as ContentAnalyzerAgent
   ```

## Per-Request Model Selection

### Geplante Frontend-UI

**unified-editor.html** soll einen Model-Selector erhalten:

```html
<select id="modelSelect">
  <optgroup label="OpenAI">
    <option value="gpt-4o" selected>GPT-4o</option>
    <option value="gpt-5">GPT-5</option>
    <option value="gpt-5-mini">GPT-5 Mini</option>
  </optgroup>
  <optgroup label="Anthropic" disabled>
    <option value="claude-3-5-sonnet">Claude 3.5 Sonnet</option>
  </optgroup>
</select>

<!-- GPT-5 Reasoning Controls (nur wenn GPT-5 ausgewählt) -->
<div id="gpt5Controls" style="display: none;">
  <label>Reasoning Effort:</label>
  <select id="reasoningEffortSelect">
    <option value="low">Low (Fast, Cheap)</option>
    <option value="medium" selected>Medium</option>
    <option value="high">High (Slow, Quality)</option>
  </select>
</div>
```

### API Request Format

```json
POST /api/v2/generate
{
  "project_name": "beispiel-projekt",
  "user_input": "...",
  "slide_title": "Folie 12",
  "slide_number": 12,
  "theme": "apple",
  "model": "gpt-5",
  "provider": "openai",
  "reasoning_effort": "high",
  "verbosity": "medium"
}
```

### Backend Implementation (routes/v2.py)

```python
@router.post("/generate")
async def generate_slide_v2(request_data: Dict[str, Any]):
    # Extract model parameters
    model = request_data.get("model", DEFAULT_MODEL)
    provider = request_data.get("provider")

    # Auto-detect provider from model if not specified
    if not provider:
        provider = MODEL_TO_PROVIDER.get(model, MODEL_PROVIDER)

    # Get GPT-5 controls if applicable
    reasoning_effort = request_data.get("reasoning_effort", "medium")
    verbosity = request_data.get("verbosity", "medium")

    # Initialize agents with correct provider
    if provider == "anthropic":
        analyzer = ContentAnalyzerAgentAnthropic(
            api_key=ANTHROPIC_API_KEY,
            model=model
        )
    else:
        analyzer = ContentAnalyzerAgentV2(
            api_key=OPENAI_API_KEY,
            model=model,
            reasoning_effort=reasoning_effort,
            verbosity=verbosity
        )

    # ... rest of pipeline
```

## Model Comparison

| Feature | GPT-4o | GPT-5 | GPT-5-mini | Claude Sonnet 4.5 | Claude 3.5 Sonnet |
|---------|--------|-------|------------|-------------------|-------------------|
| Status | ✅ Full | ✅ Full | ✅ Full | ⚠️ Prepared | ⚠️ Prepared |
| Context Window | 128k | 128k | 128k | 200k | 200k |
| Reasoning Controls | ❌ | ✅ | ✅ | ❌ | ❌ |
| Structured Outputs | ✅ | ✅ | ✅ | ⚠️ TBD | ⚠️ TBD |
| Cost (per 1M tokens) | $5/$15 | $10/$30 | $0.30/$1.20 | $3/$15 | $3/$15 |
| Speed | Fast | Medium | Very Fast | Fast | Fast |
| Quality | High | Very High | Medium | Very High | Very High |
| Release Date | 2024 | 2025 | 2025 | 2025-05 | 2024-10 |

## Testing mit verschiedenen Modellen

### TEST_MODE (No API Costs)

```env
TEST_MODE=true
```

In diesem Modus werden Mock-Agents verwendet, die keine echten API-Calls machen.

### GPT-4o Testing

```bash
cd presentation/api
export TEST_MODE=false
export DEFAULT_MODEL=gpt-4o
python3 run_api.py
```

### GPT-5 Testing

```bash
export DEFAULT_MODEL=gpt-5
export REASONING_EFFORT=high
python3 run_api.py
```

### GPT-5-mini Testing (Cost-Saving)

```bash
export DEFAULT_MODEL=gpt-5-mini
export REASONING_EFFORT=low
python3 run_api.py
```

## Environment Variables Reference

```env
# Provider Configuration
MODEL_PROVIDER=openai              # openai | anthropic
DEFAULT_MODEL=gpt-4o               # gpt-4o | gpt-5 | gpt-5-mini | claude-3-5-sonnet

# API Keys
OPENAI_API_KEY=sk-...              # Required für OpenAI
ANTHROPIC_API_KEY=sk-ant-...       # Required für Anthropic (wenn implementiert)

# GPT-5 Controls (Optional)
REASONING_EFFORT=medium            # minimal | low | medium | high
VERBOSITY=medium                   # minimal | low | medium | high

# Development
TEST_MODE=false                    # true = Mock Agents (no API costs)
```

## Troubleshooting

### OpenAI API Error

**Problem:** `OPENAI_API_KEY not found`

**Lösung:**
1. Prüfe `.env` Datei in `presentation/api/`
2. Stelle sicher, dass Key mit `sk-` beginnt
3. Keine Leerzeichen um den Key

### Rate Limits

**Problem:** `RateLimitError: Rate limit exceeded`

**Lösungen:**
1. Warte ein paar Minuten
2. Verwende GPT-5-mini statt GPT-5
3. Reduziere `reasoning_effort`
4. Upgrade deinen OpenAI Plan

### Model Not Found

**Problem:** `InvalidRequestError: Model 'gpt-5' not found`

**Lösungen:**
1. Prüfe Model-Name (korrekt geschrieben?)
2. Prüfe, ob du Zugriff auf das Modell hast (GPT-5 Beta?)
3. Verwende `gpt-4o` als Fallback

### Anthropic Not Working

**Problem:** Anthropic models funktionieren nicht

**Erklärung:** Anthropic Support ist vorbereitet, aber noch nicht vollständig implementiert.

**Workaround:** Verwende OpenAI Models.

**TODO:** Agent-Wrapper für Anthropic implementieren (siehe "Implementation TODO" oben).

## Best Practices

### 1. Model-Auswahl nach Use-Case

- **Einfache Slides** (Listen, Text): `gpt-5-mini`
- **Standard Slides** (Statistiken, Features): `gpt-4o`
- **Komplexe Slides** (Tabellen, Prozesse): `gpt-5` mit `reasoning_effort=high`

### 2. Kosten-Management

- Nutze TEST_MODE für Entwicklung
- GPT-5-mini für Bulk-Generierung
- GPT-5 nur für wichtige/komplexe Slides

### 3. Caching

```python
# Cache häufig verwendete Prompts
# Verwende Structured Outputs für deterministische Responses
use_structured_outputs=True
```

### 4. Error Handling

```python
try:
    result = orchestrator.generate_slide(...)
except openai.RateLimitError:
    # Fallback zu billigerem Modell
    orchestrator.model = "gpt-5-mini"
    result = orchestrator.generate_slide(...)
```

## Future Enhancements

### Geplante Features

1. **Anthropic Claude Full Support**
   - Agent-Wrapper implementieren
   - Testing & Validation
   - Frontend Model-Selector

2. **Model-Switching per Request**
   - Frontend UI für Model-Auswahl
   - API Parameter `model` und `provider`
   - Automatische Provider-Detection

3. **Advanced Model Controls**
   - Temperature Control
   - Top-P Control
   - Custom System Prompts per Model

4. **Model Performance Tracking**
   - Latency Monitoring
   - Cost Tracking
   - Quality Metrics

## Support

Bei Fragen oder Problemen:
1. Prüfe API-Logs für Fehler
2. Teste mit TEST_MODE=true
3. Öffne GitHub Issue mit Reproduktionsschritten

## Referenzen

- **OpenAI API Docs:** https://platform.openai.com/docs
- **Anthropic API Docs:** https://docs.anthropic.com/
- **config.py:** `presentation/api/config.py`
- **orchestrator.py:** `presentation/api/agents/orchestrator.py`
- **routes/v2.py:** `presentation/api/routes/v2.py`

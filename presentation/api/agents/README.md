# Agent System - Advanced Features

This document describes the advanced features available in the multi-agent presentation generation system.

## Table of Contents

1. [GPT-5 Support](#gpt-5-support)
2. [Pydantic Structured Outputs](#pydantic-structured-outputs)
3. [Usage Examples](#usage-examples)
4. [Migration Guide](#migration-guide)

---

## GPT-5 Support

All agents now support GPT-5 and GPT-5-mini with advanced controls for reasoning effort and verbosity.

### Features

- **`reasoning_effort`**: Controls how much "thinking" the model does
  - `minimal`: Fastest, cheapest, least thorough
  - `low`: Quick responses
  - `medium`: Balanced (default for GPT-4o)
  - `high`: Maximum quality (default for GPT-5, recommended for strategy)

- **`verbosity`**: Controls output verbosity
  - `minimal`: Concise outputs
  - `low`: Brief responses
  - `medium`: Balanced (default)
  - `high`: Detailed explanations

### Automatic Detection

The system automatically detects GPT-5 models and applies the `extra_body` controls:

```python
# Automatically uses GPT-5 controls if model contains "gpt-5"
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-5-mini"  # Auto-detected
)
```

### Custom Controls

```python
# Fine-tune for cost optimization
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-5-mini",
    reasoning_effort="minimal",  # Reduce cost
    verbosity="low"              # Shorter outputs
)

# Fine-tune for maximum quality
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-5",
    reasoning_effort="high",   # Best quality
    verbosity="medium"         # Balanced output
)
```

### Agent-Specific Defaults

- **ContentAnalyzerAgent**: `reasoning_effort="medium"` (balanced analysis)
- **PresentationStrategistAgent**: `reasoning_effort="high"` (strategy requires deeper thinking)
- **ContentGeneratorAgent**: `reasoning_effort="medium"` (balanced content generation)

---

## Pydantic Structured Outputs

All agents support optional Pydantic schemas for 100% type-safe JSON outputs.

### Benefits

✅ **Type Safety**: Guaranteed valid output structure
✅ **Auto-Validation**: Pydantic validates all fields
✅ **Better Errors**: Clear error messages when output doesn't match schema
✅ **IDE Support**: Full autocomplete and type hints
✅ **No Prompt Pollution**: Schema is enforced by API, not by prompt tokens

### Schemas

Located in `agents/schemas.py`:

- **`ContentAnalysis`**: Output from ContentAnalyzerAgent
- **`PresentationStrategy`**: Output from PresentationStrategistAgent
- **`GeneratedContent`**: Output from ContentGeneratorAgent
- **`VariantGeneration`**: Output when generating design variants

### Enabling Structured Outputs

```python
# Enable for all agents via orchestrator
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-4o",
    use_structured_outputs=True  # ✅ Type-safe outputs
)

# Or enable per agent
from agents import ContentAnalyzerAgent
from agents.schemas import ContentAnalysis

analyzer = ContentAnalyzerAgent(
    api_key=API_KEY,
    model="gpt-4o",
    use_structured_outputs=True
)

result = analyzer.analyze("...")
# result is guaranteed to match ContentAnalysis schema
```

### Backwards Compatibility

Structured outputs are **opt-in**. Default behavior uses JSON mode:

```python
# Default: JSON mode (backwards compatible)
orchestrator = AgentOrchestrator(api_key=API_KEY, model="gpt-4o")

# Explicit: Pydantic schemas (type-safe)
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-4o",
    use_structured_outputs=True
)
```

### Schema Example

```python
from pydantic import BaseModel, Field
from typing import List, Literal

class ContentAnalysis(BaseModel):
    """Structured analysis of user input content"""
    content_type: Literal["statistics", "narrative", "list", "quote", "image", "mixed", "phased", "hierarchical"]
    key_messages: List[str] = Field(..., min_items=1, max_items=3)
    has_statistics: bool = Field(default=False)
    has_images: bool = Field(default=False)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    # ... more fields
```

---

## Usage Examples

### Example 1: Cost-Optimized GPT-5-mini

```python
from agents import AgentOrchestrator

# Cheap and fast for simple slides
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-5-mini",
    reasoning_effort="minimal",  # Save costs
    verbosity="low"              # Concise output
)

result = orchestrator.process(
    user_input="3 statistics about market growth",
    project_path="./presentation/projects/my-project",
    project_name="my-project",
    slide_title="Market Overview"
)
```

### Example 2: Quality-Optimized GPT-5

```python
# Best quality for important presentations
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-5",
    reasoning_effort="high",   # Maximum quality
    verbosity="medium",        # Balanced
    use_structured_outputs=True  # Type safety
)

result = orchestrator.process(
    user_input="Complex analysis of competitive landscape...",
    project_path="./presentation/projects/investor-pitch",
    project_name="investor-pitch",
    slide_title="Competitive Analysis",
    project_scope="Investor pitch deck for Series A funding"
)
```

### Example 3: Direct Agent Usage with Schemas

```python
from agents import ContentAnalyzerAgent
from agents.schemas import ContentAnalysis

analyzer = ContentAnalyzerAgent(
    api_key=API_KEY,
    model="gpt-4o",
    use_structured_outputs=True  # Get Pydantic object
)

# Returns dict matching ContentAnalysis schema
analysis = analyzer.analyze(
    "We grew revenue 45% YoY to €12.3M, expanded to 8 new markets",
    slide_title="Growth Metrics"
)

# Type-safe access
print(analysis["content_type"])  # "statistics"
print(analysis["has_statistics"])  # True
print(analysis["confidence_score"])  # 0.95
```

### Example 4: Combining Features

```python
# GPT-5 + Structured Outputs + Custom Controls
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-5",
    reasoning_effort="high",
    verbosity="medium",
    use_structured_outputs=True
)

result = orchestrator.process(
    user_input="Phase 1: Institutional market (2026-2028)...",
    project_path="./presentation/projects/startup-deck",
    project_name="startup-deck",
    slide_title="Go-to-Market Strategy",
    project_scope="B2B SaaS startup targeting enterprise clients",
    preferences={"generate_variants": True}  # Generate 3 design variants
)

# result["generated_slides"][0] contains slide data
# result["agent_steps"] shows all agent execution steps
```

---

## Migration Guide

### From gpt-4o to gpt-5

**Minimal change (default settings):**
```python
# Before
orchestrator = AgentOrchestrator(api_key=API_KEY, model="gpt-4o")

# After - just change model string
orchestrator = AgentOrchestrator(api_key=API_KEY, model="gpt-5-mini")
# Automatically uses GPT-5 controls with intelligent defaults
```

**With optimization:**
```python
# After - with cost optimization
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-5-mini",
    reasoning_effort="minimal",  # Reduce cost
    verbosity="low"
)

# After - with quality optimization
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-5",
    reasoning_effort="high",  # Best quality
    verbosity="medium"
)
```

### Enabling Structured Outputs

**No code changes needed** - just add the flag:

```python
# Before
orchestrator = AgentOrchestrator(api_key=API_KEY, model="gpt-4o")

# After - add use_structured_outputs
orchestrator = AgentOrchestrator(
    api_key=API_KEY,
    model="gpt-4o",
    use_structured_outputs=True  # ✅ Type-safe outputs
)
```

The output format remains the same (dict), but now it's guaranteed to match the Pydantic schemas.

---

## Advanced Configuration

### Per-Agent Customization

```python
from agents import ContentAnalyzerAgent, PresentationStrategistAgent, ContentGeneratorAgent

# Different settings per agent
analyzer = ContentAnalyzerAgent(
    api_key=API_KEY,
    model="gpt-5-mini",
    reasoning_effort="low",  # Quick analysis
    use_structured_outputs=True
)

strategist = PresentationStrategistAgent(
    api_key=API_KEY,
    model="gpt-5",
    reasoning_effort="high",  # Deep strategic thinking
    use_structured_outputs=True
)

generator = ContentGeneratorAgent(
    api_key=API_KEY,
    model="gpt-5-mini",
    reasoning_effort="medium",  # Balanced generation
    use_structured_outputs=True
)
```

### Environment-Based Configuration

```python
import os

MODEL = os.getenv("LLM_MODEL", "gpt-4o")
USE_STRUCTURED = os.getenv("USE_STRUCTURED_OUTPUTS", "false").lower() == "true"
REASONING = os.getenv("REASONING_EFFORT", "medium")

orchestrator = AgentOrchestrator(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=MODEL,
    reasoning_effort=REASONING,
    use_structured_outputs=USE_STRUCTURED
)
```

---

## Performance Comparison

| Configuration | Speed | Cost | Quality | Use Case |
|--------------|-------|------|---------|----------|
| gpt-4o (default) | Fast | $$ | Good | General use |
| gpt-5-mini + minimal | Fastest | $ | Good | High-volume, simple slides |
| gpt-5-mini + medium | Fast | $$ | Better | Most presentations |
| gpt-5 + high | Slower | $$$$ | Best | Critical presentations |
| Structured Outputs | +5% | +0% | Same | When type safety matters |

---

## Troubleshooting

### Structured Outputs Not Working

**Error:** `AttributeError: 'OpenAI' object has no attribute 'beta'`

**Solution:** Update OpenAI client:
```bash
pip install --upgrade openai
```

Structured outputs require OpenAI Python SDK >= 1.12.0.

### GPT-5 Controls Not Applied

**Check model string:**
```python
# ✅ Correct - "gpt-5" in lowercase
orchestrator = AgentOrchestrator(model="gpt-5-mini")

# ❌ Won't auto-detect
orchestrator = AgentOrchestrator(model="GPT-5-MINI")
```

The auto-detection checks for `"gpt-5"` in `model.lower()`.

### Cost Concerns

**Use cost controls:**
```python
# Minimize cost for batch processing
orchestrator = AgentOrchestrator(
    model="gpt-5-mini",
    reasoning_effort="minimal",
    verbosity="low"
)
```

---

## Best Practices

1. **Use GPT-5-mini for most slides** - It's fast and cost-effective
2. **Use GPT-5 with reasoning_effort="high" for complex strategy** - Especially for PresentationStrategist
3. **Enable structured_outputs for production** - Type safety prevents bugs
4. **Set project_scope** - Helps LLM understand context
5. **Monitor costs** - Use `verbosity="low"` for cost control

---

## Support

For questions or issues:
- Check the schemas in `agents/schemas.py`
- Review examples above
- Test with `use_structured_outputs=False` first (simpler debugging)

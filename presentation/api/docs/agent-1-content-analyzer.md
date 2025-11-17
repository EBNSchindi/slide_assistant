# Agent 1: Content Analyzer

**Version:** 1.0
**Status:** Draft
**Agent Role:** Content Understanding
**Last Updated:** 2025-11-17

## Mission Statement

**"Was will diese Folie eigentlich sagen? Und aus welchen Bausteinen besteht der Inhalt?"**

Agent 1 analyzes user input (text, bullet points, markdown) and extracts structured content blocks without making layout decisions.

## Responsibilities

### ✅ What Agent 1 DOES

1. **Content Classification**
   - Identify content type (statistics, narrative, list, quote, mixed, etc.)
   - Detect language (German or English)
   - Determine slide purpose (problem, solution, team, KPIs, timeline, etc.)

2. **Content Extraction**
   - Break input into semantic **content blocks**
   - Extract key messages (max 3)
   - Identify statistics, quotes, lists, image references
   - Detect temporal context (dates, timeframes)

3. **Content Quality Assessment**
   - Flag content density (low/medium/high/too_high)
   - Detect potential issues (missing info, ambiguous phrasing)
   - Provide confidence score for analysis

4. **Metadata Collection**
   - Identify data sources (e.g., "Bank of America", "Gartner")
   - Extract temporal context (e.g., "2025", "bis 2030")
   - Detect icons/emojis used
   - Note image references

### ❌ What Agent 1 DOES NOT DO

1. **No Layout Decisions** - Does not choose components or positions
2. **No Text Formatting** - Does not write final headings or bullet points
3. **No HTML/Markdown Generation** - Output is structured JSON only
4. **No Image Selection** - Only notes that images are referenced
5. **No Design Choices** - No colors, fonts, spacing decisions

## Process Flow

### When is Agent 1 Called?

**Trigger:** User submits content for a new slide via `/api/generate` endpoint.

**Frequency:** Once per slide generation request.

**Order:** First agent in the pipeline (before Agent 2 and Agent 3).

### Agent 1 Workflow

```
┌─────────────────────────────────────┐
│  User Input                         │
│  - Freetext / Markdown              │
│  - Optional: Image filenames        │
│  - Optional: Target audience        │
│  - Optional: Slide context          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Agent 1: Content Analyzer          │
│                                     │
│  1. Detect language (de/en)         │
│  2. Classify content type           │
│  3. Extract content blocks          │
│  4. Identify key messages (max 3)   │
│  5. Assess content density          │
│  6. Flag issues/warnings            │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Output: ContentAnalysis (JSON)     │
│  - content_type                     │
│  - key_messages [list]              │
│  - content_blocks [list]            │
│  - metadata (sources, dates, etc.)  │
│  - quality indicators               │
└─────────────────────────────────────┘
              ↓
         [Agent 2]
```

## Input Specification

### Required Fields

```python
class ContentAnalyzerInput(BaseModel):
    user_input: str = Field(..., description="Raw user content (text/markdown)")
    slide_context: Optional[str] = Field(None, description="Context (e.g., 'Investor Pitch', 'Team Update')")
```

### Optional Fields

```python
    project_name: Optional[str] = Field(None, description="Project name (e.g., 'Robo4you')")
    target_audience: Optional[str] = Field(None, description="Target audience (e.g., 'investors', 'team')")
    uploaded_images: Optional[List[str]] = Field(None, description="List of uploaded image filenames")
    language_hint: Optional[Literal["de", "en"]] = Field(None, description="Language hint (auto-detected if not provided)")
```

### Example Inputs

#### Example 1: Simple Statistics

```json
{
  "user_input": "5 Experten, 20 Jahre Erfahrung, 3 Standorte (Berlin, München, Hamburg)",
  "slide_context": "Team Overview",
  "project_name": "Robo4you"
}
```

#### Example 2: Problem Statement

```json
{
  "user_input": "Aktuelle Probleme:\n- Manuelle Prozesse kosten 40% der Zeit\n- Fehlerquote über 15%\n- Bestehende Lösungen zu teuer",
  "slide_context": "Problem Slide",
  "target_audience": "investors"
}
```

#### Example 3: Mixed Content with Image

```json
{
  "user_input": "Unser Team besteht aus 5 Robotik-Experten mit über 20 Jahren Erfahrung. Wir haben Standorte in Berlin, München und Hamburg. [Bild: Teamfoto vor dem Büro]",
  "uploaded_images": ["teamfoto.png"],
  "slide_context": "Team Slide"
}
```

## Output Specification

### Output Schema: ContentAnalysis

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ContentBlock(BaseModel):
    """Single semantic content block"""
    block_type: Literal["statistic", "statement", "bullet", "quote", "image_ref", "temporal"] = Field(
        ..., description="Type of content block"
    )
    raw_text: str = Field(..., description="Original text of this block")
    importance: Literal["critical", "high", "medium", "low"] = Field(
        ..., description="Importance of this block for the slide"
    )

    # Type-specific fields
    statistic_value: Optional[str] = Field(None, description="For statistics: the numeric value")
    statistic_unit: Optional[str] = Field(None, description="For statistics: unit (e.g., '%', 'Mio', '€')")
    statistic_label: Optional[str] = Field(None, description="For statistics: label/description")

    quote_author: Optional[str] = Field(None, description="For quotes: author name")
    quote_source: Optional[str] = Field(None, description="For quotes: source")

    image_filename: Optional[str] = Field(None, description="For image refs: filename")
    image_context: Optional[str] = Field(None, description="For image refs: context/description")

class ContentAnalysis(BaseModel):
    """Complete analysis output from Agent 1"""

    # Primary classification
    content_type: Literal["statistics", "narrative", "list", "quote", "image", "mixed", "phased", "hierarchical"] = Field(
        ..., description="Primary content type"
    )
    language: Literal["de", "en"] = Field(..., description="Detected language")
    slide_purpose: Optional[str] = Field(None, description="Inferred slide purpose (e.g., 'team_overview', 'problem_statement')")

    # Core content
    key_messages: List[str] = Field(
        ...,
        min_items=1,
        max_items=3,
        description="Main takeaways (max 3)"
    )
    content_blocks: List[ContentBlock] = Field(
        ...,
        description="Structured content blocks"
    )

    # Content flags
    has_statistics: bool = Field(default=False)
    has_lists: bool = Field(default=False)
    has_quotes: bool = Field(default=False)
    has_images: bool = Field(default=False)
    has_icons: bool = Field(default=False)

    # Metadata
    sources: Optional[List[str]] = Field(None, description="Data sources cited")
    temporal_context: Optional[List[str]] = Field(None, description="Time references")
    icons_used: Optional[List[str]] = Field(None, description="Icons/emojis detected")

    # Quality indicators
    content_density: Literal["low", "medium", "high", "too_high"] = Field(
        ..., description="Information density"
    )
    warnings: List[str] = Field(default_factory=list, description="Issues detected")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Analysis confidence")

    # Recommendations for Agent 2
    suggested_component_count: int = Field(..., ge=1, le=3, description="Recommended component count")
```

### Example Outputs

#### Example 1: Statistics Slide

```json
{
  "content_type": "statistics",
  "language": "de",
  "slide_purpose": "team_overview",

  "key_messages": [
    "Team von 5 Experten mit langjähriger Erfahrung",
    "Präsenz an 3 Standorten in Deutschland",
    "Über 20 Jahre kombinierte Expertise"
  ],

  "content_blocks": [
    {
      "block_type": "statistic",
      "raw_text": "5 Experten",
      "importance": "critical",
      "statistic_value": "5",
      "statistic_unit": null,
      "statistic_label": "Experten"
    },
    {
      "block_type": "statistic",
      "raw_text": "20 Jahre Erfahrung",
      "importance": "high",
      "statistic_value": "20",
      "statistic_unit": "Jahre",
      "statistic_label": "Erfahrung"
    },
    {
      "block_type": "statistic",
      "raw_text": "3 Standorte",
      "importance": "medium",
      "statistic_value": "3",
      "statistic_unit": null,
      "statistic_label": "Standorte"
    }
  ],

  "has_statistics": true,
  "has_lists": false,
  "has_quotes": false,
  "has_images": false,
  "has_icons": false,

  "content_density": "low",
  "warnings": [],
  "confidence_score": 0.95,
  "suggested_component_count": 1
}
```

#### Example 2: Problem Statement (Bullets)

```json
{
  "content_type": "list",
  "language": "de",
  "slide_purpose": "problem_statement",

  "key_messages": [
    "Manuelle Prozesse verschwenden Zeit",
    "Hohe Fehlerquote bei repetitiven Aufgaben",
    "Bestehende Lösungen nicht praktikabel"
  ],

  "content_blocks": [
    {
      "block_type": "bullet",
      "raw_text": "Manuelle Prozesse kosten 40% der Zeit",
      "importance": "critical"
    },
    {
      "block_type": "bullet",
      "raw_text": "Fehlerquote über 15%",
      "importance": "high"
    },
    {
      "block_type": "bullet",
      "raw_text": "Bestehende Lösungen zu teuer",
      "importance": "high"
    }
  ],

  "has_statistics": true,
  "has_lists": true,
  "has_quotes": false,
  "has_images": false,
  "has_icons": false,

  "content_density": "medium",
  "warnings": [],
  "confidence_score": 0.92,
  "suggested_component_count": 1
}
```

#### Example 3: Mixed Content with Image

```json
{
  "content_type": "mixed",
  "language": "de",
  "slide_purpose": "team_overview",

  "key_messages": [
    "Erfahrenes Kernteam mit Robotik-Expertise",
    "Deutschlandweite Präsenz",
    "Langjährige Branchenerfahrung"
  ],

  "content_blocks": [
    {
      "block_type": "statistic",
      "raw_text": "5 Robotik-Experten",
      "importance": "critical",
      "statistic_value": "5",
      "statistic_label": "Robotik-Experten"
    },
    {
      "block_type": "statistic",
      "raw_text": "über 20 Jahren Erfahrung",
      "importance": "high",
      "statistic_value": "20+",
      "statistic_unit": "Jahre",
      "statistic_label": "Erfahrung"
    },
    {
      "block_type": "statement",
      "raw_text": "Standorte in Berlin, München und Hamburg",
      "importance": "medium"
    },
    {
      "block_type": "image_ref",
      "raw_text": "[Bild: Teamfoto vor dem Büro]",
      "importance": "medium",
      "image_filename": "teamfoto.png",
      "image_context": "Teamfoto vor dem Büro"
    }
  ],

  "has_statistics": true,
  "has_lists": false,
  "has_quotes": false,
  "has_images": true,
  "has_icons": false,

  "content_density": "medium",
  "warnings": [],
  "confidence_score": 0.88,
  "suggested_component_count": 2
}
```

## LLM Prompt Guidelines

### System Prompt (Agent 1)

```
You are a Content Analyzer for presentation slides.

Your job is to:
1. Understand what the slide is trying to communicate
2. Break content into semantic blocks (statistics, statements, bullets, quotes, images)
3. Extract key messages (max 3)
4. Assess content quality and density

You do NOT:
- Make layout decisions
- Choose components
- Write final text
- Generate HTML/Markdown

Analyze the user input and return a structured JSON with:
- content_type
- language
- key_messages (max 3)
- content_blocks (list of semantic blocks)
- quality indicators (density, warnings, confidence)

Always respond in JSON format using the ContentAnalysis schema.
```

### User Prompt Template

```
Analyze the following slide content:

INPUT:
{user_input}

CONTEXT:
- Project: {project_name}
- Audience: {target_audience}
- Slide Purpose: {slide_context}
- Uploaded Images: {uploaded_images}

Provide a structured analysis following the ContentAnalysis schema.
```

## Decision Rules

### Content Type Classification

| Input Pattern | Content Type | Example |
|---------------|--------------|---------|
| 2+ numbers with units | `statistics` | "€12M revenue, 85% growth" |
| 3+ bullet points | `list` | "- Item 1\n- Item 2\n- Item 3" |
| Quoted text with attribution | `quote` | ""Innovation is key" - Steve Jobs" |
| Image references only | `image` | "[Bild: Dashboard Screenshot]" |
| Mix of above | `mixed` | Stats + bullets + image |
| Time-based phases | `phased` | "Phase 1 (2025): ..., Phase 2 (2026): ..." |
| Nested structure (H2, H3) | `hierarchical` | Markdown with subheadings |

### Language Detection

1. **German:** Keywords like "der/die/das", "und", "für", "über", "Jahre"
2. **English:** Keywords like "the", "and", "for", "over", "years"
3. **Fallback:** If ambiguous, default to English
4. **User Override:** If `language_hint` provided, use it

### Importance Scoring

| Importance | Criteria |
|------------|----------|
| `critical` | Core metric, main problem, key solution |
| `high` | Supporting data, secondary problem |
| `medium` | Context, background info |
| `low` | Nice-to-have details |

### Suggested Component Count

| Content Blocks | Suggested Components |
|----------------|---------------------|
| 1-3 blocks | 1 component |
| 4-6 blocks | 2 components |
| 7+ blocks | 3 components (or warning: too_high density) |

## Error Handling

### Warning Types

1. **`too_much_content`** - More than 6 content blocks detected
2. **`ambiguous_intent`** - Cannot determine slide purpose
3. **`missing_context`** - No clear key messages
4. **`image_not_found`** - Referenced image not in uploaded list
5. **`mixed_languages`** - Multiple languages detected in input

### Confidence Score Calculation

- **0.9-1.0:** Clear content type, obvious key messages, no warnings
- **0.7-0.89:** Some ambiguity, but analyzable
- **0.5-0.69:** Significant ambiguity, may need user clarification
- **< 0.5:** Cannot reliably analyze (should request user input)

## Testing Strategy

### Unit Tests

1. **Content Type Detection**
   - Test each content type (statistics, list, quote, etc.)
   - Test mixed content

2. **Language Detection**
   - Pure German input
   - Pure English input
   - Mixed language input

3. **Block Extraction**
   - Statistics parsing (various formats: €, %, Mio, Mrd)
   - Bullet point detection
   - Image reference extraction

4. **Edge Cases**
   - Empty input → error
   - Single word input → low confidence
   - Very long input (1000+ words) → too_high density warning

### Integration Tests

1. Agent 1 → Agent 2 handoff
2. Validate output schema compliance
3. Check all required fields populated

### Fixture Data

Create test fixtures in `presentation/api/tests/fixtures/agent1/`:
- `statistics_de.json`
- `problem_list_en.json`
- `mixed_with_image_de.json`
- `edge_case_empty.json`

## Performance Targets

- **Response Time:** < 2 seconds for typical input (100-500 words)
- **Accuracy:** 90%+ content type classification (manual validation)
- **Token Usage:** < 500 tokens per analysis (GPT-4o)

## Version History

- **1.0** (2025-11-17) - Initial specification

## Related Documentation

- [Blueprint Schema](./blueprint-schema.md)
- [Agent 2 Specification](./agent-2-presentation-strategist.md)
- [Agent 3 Specification](./agent-3-content-generator.md)

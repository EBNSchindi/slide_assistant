# Agent 3: Content Generator (Copywriter)

**Version:** 1.0
**Status:** Draft
**Agent Role:** Text Formulation & Copywriting
**Last Updated:** 2025-11-17

## Mission Statement

**"Ich schreibe die tatsächlichen Texte – in der passenden Länge, Tonalität und Sprache – aber noch nicht als HTML."**

Agent 3 takes the partial blueprint from Agent 2 and fills in all text content (titles, bullets, captions, labels) to create a complete, render-ready blueprint—without generating HTML.

## Responsibilities

### ✅ What Agent 3 DOES

1. **Text Writing**
   - Write slide title and subtitle
   - Write component titles
   - Formulate bullet points (concise, parallel structure)
   - Write statistic labels
   - Write image titles, captions, and alt texts
   - Write quotes (if applicable)

2. **Readability Optimization**
   - Keep bullets under 120 characters
   - Use active voice
   - Avoid jargon (unless target audience expects it)
   - Ensure parallel structure in lists
   - Apply readability best practices

3. **Language & Tone Matching**
   - Write in detected language (from Agent 1)
   - Match tone to target audience (investor pitch = formal, team update = casual)
   - Maintain consistency across all text elements

4. **Blueprint Completion**
   - Fill all `[TBD]` placeholders from Agent 2
   - Add metadata (created_at, content_density, tags)
   - Validate completeness before returning

5. **Quality Assurance**
   - Check readability score (easy/medium/complex)
   - Ensure accessibility compliance (alt texts, clear language)
   - Flag overly long or complex text

### ❌ What Agent 3 DOES NOT DO

1. **No HTML/Markdown Generation** - Output is complete Blueprint (JSON), not markup
2. **No Layout Changes** - Uses layout plan from Agent 2 as-is
3. **No Component Selection** - Does not add/remove components
4. **No Image Creation** - Only writes text about existing images
5. **No Design Decisions** - No colors, fonts, or visual styling

## Process Flow

### When is Agent 3 Called?

**Trigger:** Agent 2 completes layout planning.

**Frequency:** Once per slide, immediately after Agent 2.

**Order:** Third (final) agent in pipeline, before Renderer.

### Agent 3 Workflow

```
┌─────────────────────────────────────┐
│  Input from Agent 2                 │
│  - PartialBlueprint                 │
│  - layout_type                      │
│  - component_mappings               │
│  - [TBD] placeholders for text      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Input from Agent 1                 │
│  - content_blocks (raw text)        │
│  - language                         │
│  - key_messages                     │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Copywriting Guidelines             │
│  - Readability rules                │
│  - Tone/audience info               │
│  - Character limits                 │
│  - Accessibility requirements       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Agent 3: Content Generator         │
│                                     │
│  1. Write slide title/subtitle      │
│  2. For each component:             │
│     - Write titles                  │
│     - Formulate bullets/labels      │
│     - Write image captions          │
│  3. Generate alt texts (images)     │
│  4. Add metadata                    │
│  5. Validate completeness           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Output: Complete Blueprint         │
│  - All text fields filled           │
│  - No [TBD] placeholders            │
│  - Metadata complete                │
│  - Ready for Renderer               │
└─────────────────────────────────────┘
              ↓
        [Renderer]
```

## Input Specification

### Required Fields

```python
class GeneratorInput(BaseModel):
    """Input for Agent 3"""
    partial_blueprint: PartialBlueprint = Field(..., description="Partial blueprint from Agent 2")
    content_analysis: ContentAnalysis = Field(..., description="Content analysis from Agent 1")

    # Copywriting context
    target_audience: Optional[str] = Field(None, description="Target audience (e.g., 'investors', 'team')")
    tone: Literal["formal", "casual", "technical", "inspirational"] = Field(
        default="formal",
        description="Writing tone"
    )

    # Project context
    project_name: str = Field(..., description="Project name (for context)")
    slide_number: Optional[int] = Field(None, description="Slide number (for ID generation)")
```

### Example Input

```json
{
  "partial_blueprint": {
    "layout_type": "two_column",
    "component_mappings": [
      {
        "component_id": "comp-1",
        "component_type": "stat_grid",
        "position": "left",
        "content_block_indices": [0, 1],
        "structure_hint": "2x1 grid"
      },
      {
        "component_id": "comp-2",
        "component_type": "image_frame",
        "position": "right",
        "content_block_indices": [2],
        "image_filename": "teamfoto.png",
        "structure_hint": "single image with caption"
      }
    ],
    "cognitive_load_score": "low"
  },

  "content_analysis": {
    "language": "de",
    "content_blocks": [
      {
        "block_type": "statistic",
        "raw_text": "5 Experten",
        "statistic_value": "5",
        "statistic_label": "Experten"
      },
      {
        "block_type": "statistic",
        "raw_text": "20 Jahre Erfahrung",
        "statistic_value": "20",
        "statistic_unit": "Jahre",
        "statistic_label": "Erfahrung"
      },
      {
        "block_type": "image_ref",
        "raw_text": "Teamfoto vor dem Büro",
        "image_filename": "teamfoto.png"
      }
    ]
  },

  "target_audience": "investors",
  "tone": "formal",
  "project_name": "Robo4you",
  "slide_number": 3
}
```

## Output Specification

### Output Schema: CompleteBlueprint

```python
class CompleteBlueprint(SlideBlueprint):
    """Complete blueprint ready for rendering (extends SlideBlueprint)"""

    # All fields from SlideBlueprint are filled:
    # - slide_title ✅
    # - slide_subtitle ✅
    # - components[].content ✅ (all text fields populated)
    # - metadata ✅

    # Additional validation fields
    readability_score: Literal["easy", "medium", "complex"] = Field(
        ...,
        description="Overall readability assessment"
    )
    accessibility_compliant: bool = Field(
        ...,
        description="Whether blueprint meets accessibility requirements"
    )
    word_count_per_component: List[int] = Field(
        ...,
        description="Word count for each component (for content density tracking)"
    )
```

### Example Output (Complete Blueprint)

```json
{
  "schema_version": "1.0",
  "slide_id": "slide-03-team",
  "slide_title": "Unser Team",
  "slide_subtitle": "Expertise trifft Innovation",

  "layout_type": "two_column",
  "language": "de",

  "components": [
    {
      "component_id": "comp-1",
      "type": "stat_grid",
      "position": "left",
      "content": {
        "title": null,
        "items": [
          {
            "value": "5",
            "label": "Robotik-Experten",
            "unit": null,
            "emphasis": true
          },
          {
            "value": "20+",
            "label": "Jahre Branchenerfahrung",
            "unit": "Jahre",
            "emphasis": false
          }
        ],
        "layout": "2x1"
      }
    },
    {
      "component_id": "comp-2",
      "type": "image_frame",
      "position": "right",
      "content": {
        "image_id": "teamfoto.png",
        "image_path": "projects/robo4you/images/uploads/teamfoto.png",
        "title": "Unser Kernteam",
        "caption": "Führende Experten für Robotik, KI und Automatisierung mit kombiniert über 100 Jahren Erfahrung",
        "alt_text": "Gruppenfoto von fünf Teammitgliedern vor dem Robo4you Bürogebäude in Berlin",
        "frame_variant": "single",
        "aspect_ratio": "16:9"
      }
    }
  ],

  "metadata": {
    "created_by": "ai",
    "created_at": "2025-11-17T10:35:00Z",
    "agent_versions": {
      "analyzer": "1.0",
      "strategist": "1.0",
      "generator": "1.0"
    },
    "content_density": "medium",
    "tags": ["team", "expertise", "about-us"],
    "notes": "Formal tone for investor audience"
  },

  "readability_score": "easy",
  "accessibility_compliant": true,
  "word_count_per_component": [6, 24]
}
```

## Copywriting Rules

### General Rules

1. **Brevity:**
   - Slide titles: Max 60 characters
   - Bullet points: Max 120 characters
   - Image captions: Max 200 characters

2. **Clarity:**
   - Active voice preferred
   - Concrete over abstract
   - Specific numbers over vague terms ("5 experts" not "several experts")

3. **Consistency:**
   - Parallel structure in bullet lists
   - Consistent terminology across slide
   - Match language detected by Agent 1

4. **Accessibility:**
   - Alt texts required for all images (descriptive, max 150 chars)
   - Avoid relying solely on color or visual cues
   - Clear, simple language when possible

### Component-Specific Rules

#### Stat Grid

```python
# Good
{
  "value": "€12,5",
  "label": "Umsatz",
  "unit": "Mio"
}

# Bad (too verbose)
{
  "value": "€12,5",
  "label": "Gesamtumsatz im letzten Geschäftsjahr",  # Too long
  "unit": "Millionen"
}
```

**Rules:**
- Labels: 1-3 words max
- Values: Formatted with units (€, %, Mio, Mrd)
- Units: Abbreviations preferred (Mio > Millionen)

#### Bullet List

```python
# Good (parallel structure, concise)
[
  "Manuelle Prozesse kosten 40% der Arbeitszeit",
  "Fehlerquote bei Routineaufgaben über 15%",
  "Bestehende Lösungen zu komplex oder zu teuer"
]

# Bad (inconsistent structure)
[
  "40% der Arbeitszeit wird verschwendet",           # Passive voice
  "Es gibt hohe Fehlerquoten",                       # Vague
  "Lösungen sind zu teuer, komplex, unflexibel, ..."  # Too long, unfocused
]
```

**Rules:**
- Start with verb or noun (parallel structure)
- One idea per bullet
- Max 120 characters
- No punctuation at end (unless multiple sentences)

#### Image Frame

```python
{
  "title": "Unser Kernteam",  # Short, descriptive
  "caption": "Führende Experten für Robotik und KI mit über 100 Jahren kombinierter Erfahrung",  # Context, benefits
  "alt_text": "Gruppenfoto von fünf Teammitgliedern vor dem Robo4you Bürogebäude in Berlin"  # Visual description
}
```

**Rules:**
- Title: Max 60 chars, focus on "what"
- Caption: Max 200 chars, focus on "why it matters"
- Alt text: Max 150 chars, describe visual content objectively

#### Quote

```python
{
  "quote_text": "Robo4you hat unsere Produktionszeit um 60% reduziert. Ein echtes Game-Changer.",
  "author": "Dr. Maria Schmidt",
  "author_title": "CTO, AutoTech GmbH",
  "source": "Kundeninterview, März 2025"
}
```

**Rules:**
- Quote: Max 300 chars, use quotation marks in template
- Author: Name only (no titles)
- Author title: Role + company
- Source: Optional, for credibility

#### Text Block

```python
{
  "title": "Unsere Mission",
  "paragraphs": [
    "Wir entwickeln intelligente Robotiklösungen, die Unternehmen effizienter machen.",
    "Unsere Technologie kombiniert KI, Computer Vision und fortschrittliche Sensorik."
  ],
  "emphasis_phrases": ["intelligente Robotiklösungen", "KI"]
}
```

**Rules:**
- 1-3 paragraphs max
- Each paragraph: 1-2 sentences
- Emphasis: Key terms only (2-4 phrases max)

### Tone Guidelines

| Audience | Tone | Example |
|----------|------|---------|
| **Investors** | Formal, data-driven | "Nachweisbare Effizienzsteigerung von 40%" |
| **Customers** | Benefit-focused, clear | "Sparen Sie 40% Ihrer Zeit" |
| **Team** | Casual, motivating | "Wir rocken 40% mehr Effizienz!" |
| **Technical** | Precise, detailed | "Durchsatz-Optimierung: +40% (n=127, p<0.01)" |

## LLM Prompt Guidelines

### System Prompt (Agent 3)

```
You are a professional copywriter for presentation slides.

Your job is to:
1. Write clear, concise text for slide components
2. Follow strict character limits
3. Match the language and tone to the audience
4. Ensure readability and accessibility
5. Complete the blueprint with all text content

You do NOT:
- Generate HTML or Markdown
- Change layout or component selection
- Add or remove components
- Create new content beyond the provided content blocks

Copywriting Rules:
- Slide titles: Max 60 characters
- Bullets: Max 120 characters
- Image captions: Max 200 characters
- Alt texts: Max 150 characters (required)
- Use active voice
- Be specific (numbers > vague terms)
- Maintain parallel structure in lists

Respond with a CompleteBlueprint JSON structure with all text fields filled.
```

### User Prompt Template

```
Complete this slide blueprint by writing all text content:

PARTIAL BLUEPRINT (from Agent 2):
{partial_blueprint_json}

CONTENT BLOCKS (from Agent 1):
{content_blocks_json}

LANGUAGE: {language}
TONE: {tone}
TARGET AUDIENCE: {target_audience}

INSTRUCTIONS:
- Write slide title and subtitle (if needed)
- For each component, fill in all text fields:
  - Stat grid: Write labels (1-3 words max)
  - Bullet list: Write bullets (max 120 chars, parallel structure)
  - Image frame: Write title (max 60 chars), caption (max 200 chars), alt text (max 150 chars)
  - Text block: Write paragraphs (1-2 sentences each)
  - Quote: Format quote text (max 300 chars)

- Follow copywriting best practices
- Ensure accessibility (alt texts required)
- Maintain consistency across all text

Provide a CompleteBlueprint with:
- All text fields filled (no [TBD] placeholders)
- metadata (created_at, tags, etc.)
- readability_score
- accessibility_compliant (true/false)
- word_count_per_component
```

## Validation & Quality Checks

### Pre-Output Validation

Before returning the CompleteBlueprint, Agent 3 must validate:

1. **Completeness:**
   - ✅ `slide_title` is not empty
   - ✅ All component `content` fields are filled
   - ✅ No `[TBD]` or placeholder text remains
   - ✅ `metadata` is populated

2. **Character Limits:**
   - ✅ Slide title ≤ 60 chars
   - ✅ Bullets ≤ 120 chars
   - ✅ Image captions ≤ 200 chars
   - ✅ Alt texts ≤ 150 chars

3. **Accessibility:**
   - ✅ All images have alt texts
   - ✅ Alt texts are descriptive (not just filenames)

4. **Readability:**
   - ✅ Bullets use parallel structure
   - ✅ No overly complex jargon (unless technical audience)
   - ✅ Active voice preferred

### Readability Score Calculation

| Score | Criteria |
|-------|----------|
| `easy` | Short sentences, simple words, clear structure |
| `medium` | Some longer sentences, domain-specific terms, mostly clear |
| `complex` | Long sentences, technical jargon, requires domain knowledge |

**Auto-flags for "complex":**
- Average sentence length > 20 words
- Multiple nested clauses
- High jargon density (> 30% technical terms)

## Error Handling

### Common Issues

1. **Character Limit Exceeded:**
   - **Action:** Truncate and flag in warnings
   - **Example:** "Bullet text too long, truncated to 120 chars"

2. **Missing Alt Text:**
   - **Action:** Generate generic alt text from filename
   - **Warning:** "Auto-generated alt text, recommend manual review"

3. **Language Mismatch:**
   - **Action:** Re-write in correct language
   - **Warning:** "Detected language mismatch, corrected to {language}"

4. **Tone Inconsistency:**
   - **Action:** Adjust tone in second pass
   - **Note:** Log in `metadata.notes`

## Testing Strategy

### Unit Tests

1. **Text Generation:**
   - Generate titles within 60 chars
   - Generate bullets within 120 chars
   - Generate alt texts (required, descriptive)

2. **Readability:**
   - Parallel structure in bullets
   - Active voice usage
   - Specific vs. vague language

3. **Language Consistency:**
   - German input → German output
   - English input → English output

4. **Tone Matching:**
   - Formal tone for investors
   - Casual tone for team

### Integration Tests

1. Agent 2 → Agent 3 → Renderer pipeline
2. Validate CompleteBlueprint structure
3. Ensure Renderer can consume output without errors

### Fixture Data

Create test fixtures in `presentation/api/tests/fixtures/agent3/`:
- `complete_blueprint_team_de.json`
- `complete_blueprint_problem_en.json`
- `complete_blueprint_with_image.json`
- `edge_case_long_text.json`

## Performance Targets

- **Response Time:** < 3 seconds (includes LLM call for text generation)
- **Token Usage:** < 800 tokens per slide (GPT-4o)
- **Accuracy:** 95%+ character limit compliance
- **Quality:** 90%+ readability score "easy" or "medium" (manual review)

## Output Artifacts

### Primary Output

**CompleteBlueprint JSON** → saved to `projects/{name}/blueprints/slide-{NN}-{title}.json`

### Secondary Outputs (for debugging)

- **Copywriting Log:** Track character counts, readability metrics
- **Warnings Log:** Any issues encountered during text generation

## Version History

- **1.0** (2025-11-17) - Initial specification

## Related Documentation

- [Blueprint Schema](./blueprint-schema.md)
- [Agent 1 Specification](./agent-1-content-analyzer.md)
- [Agent 2 Specification](./agent-2-presentation-strategist.md)
- [Renderer Specification](./renderer-specification.md)

# Variant Generation Logic (V1 Archive)

This document archives the variant generation logic from V1 (content_generator.py) for future reference when porting to V2.

## Overview

The V1 variant generation system produces 3 design variants of the same content slide, each styled according to a different design profile (corporate, modern, minimal).

## Architecture

### Entry Point
```python
# In ContentGeneratorAgent.generate()
if generate_variants and variant_profiles:
    return self._generate_variants(
        analysis, strategy, style_guide, slide_title,
        project_scope, image_references, project_name,
        base_context, base_system_prompt, variant_profiles
    )
```

### Method Signature
```python
def _generate_variants(
    self,
    analysis: dict,
    strategy: dict,
    style_guide: dict,
    slide_title: str,
    project_scope: str,
    image_references: list,
    project_name: str,
    base_context: str,
    base_system_prompt: str,
    variant_profiles: list,
) -> dict:
```

### Input: variant_profiles

Each profile is a dict with:
```python
{
    "name": "corporate" | "modern" | "minimal",
    "primary_color": "#238636" | "#0066cc" | "#666666",
    "character": "Professional, clean, green-accented" | etc,
    "visual_properties": {
        "typography": {
            "font_family": "...",
            "font_weights": {...}
        },
        "borders_effects": {
            "border_width": "2px" | "1px",
            "shadow": "lg" | "minimal"
        },
        "spacing": "generous" | "moderate" | "compact",
        "colors": {...}
    }
}
```

## Algorithm

### Step 1: Loop Through Profiles
For each variant profile (corporate, modern, minimal):

### Step 2: Build Profile-Specific System Prompt
The base system prompt is extended with design-specific instructions:

```
═══════════════════════════════════════════════════════════
🎨 DESIGN PROFILE: {PROFILE_NAME}
═══════════════════════════════════════════════════════════

This variant should follow the {profile_name.title()} design profile:
- Primary Color: {primary_color}
- Character: {profile.get('character', 'N/A')}
- Typography: {font_family}
- Border Style: {border_width} borders
- Shadows: {shadow}

Design this variant to visually align with the {profile_name} profile while maintaining
the same semantic content. Use colors and styling that match the profile definition.

All other requirements remain the same.
```

### Step 3: API Call with Profile Context
For each variant, make an OpenAI API call with:

**System Message:** Base system prompt + profile-specific design instructions
**User Message:** Base context + "Please generate both markdown and HTML for this slide based on the analysis and strategy. This is the {profile_name} variant."

**Parameters:**
- temperature: 0.5 (consistent but slightly creative)
- response_format: JSON object (structured output)

**GPT-5 Specific (if using GPT-5 model):**
```python
if "gpt-5" in self.model.lower():
    api_params["extra_body"] = {
        "reasoning_effort": self.reasoning_effort,  # minimal|low|medium|high
        "verbosity": self.verbosity,  # minimal|low|medium|high
    }
```

### Step 4: Parse and Collect Output
Expected JSON response format:
```json
{
    "html": "...",
    "markdown": "...",
    "components_used": ["stat-grid", "bullet-list"],
    "readability_score": "high"
}
```

Each variant is collected with:
```python
{
    "profile": "corporate" | "modern" | "minimal",
    "html_content": "...",
    "markdown_content": "...",
    "components_used": [...],
    "readability_score": "..."
}
```

### Step 5: Error Handling
If variant generation fails, a fallback variant is still added:
```python
{
    "profile": "corporate",
    "html_content": "<div class='error'>Failed to generate corporate variant: {error}</div>",
    "markdown_content": "# Error: Failed to generate corporate variant",
    "components_used": [],
    "error": "{error_message}"
}
```

## Output Format

```python
{
    "variants": [
        {
            "profile": "corporate",
            "html_content": "...",
            "markdown_content": "...",
            "components_used": [...],
            "readability_score": "high"
        },
        {
            "profile": "modern",
            "html_content": "...",
            "markdown_content": "...",
            "components_used": [...],
            "readability_score": "high"
        },
        {
            "profile": "minimal",
            "html_content": "...",
            "markdown_content": "...",
            "components_used": [...],
            "readability_score": "high"
        }
    ],
    "variant_count": 3,
    "components_used": [
        ["stat-grid", "bullet-list"],
        ["stat-grid", "bullet-list"],
        ["stat-grid", "bullet-list"]
    ]
}
```

## Key Characteristics

1. **Same Content, Different Styles**: The semantic content (text, data, structure) remains identical across variants; only the HTML/CSS styling changes.

2. **LLM-Generated HTML**: V1 uses the LLM to generate HTML directly, which can lead to inconsistency. This is why V2 uses deterministic rendering with Jinja2 templates instead.

3. **Profile-Driven Design**: Design instructions are injected into the LLM prompt, relying on the model to interpret and apply them to the HTML output.

4. **Temperature 0.5**: Slightly creative to ensure visual diversity while maintaining quality.

5. **Cost Optimization**: For GPT-5, reasoning_effort and verbosity can be tuned to reduce API costs while maintaining output quality.

## Porting to V2

When porting variant generation to V2, consider:

### Advantages of V2 Approach
- **Deterministic**: Jinja2 templates ensure consistent HTML structure
- **Theme-Aware**: CSS variables in design-guide.json can automatically switch colors/typography
- **No API Cost**: Variant generation doesn't require additional LLM calls
- **Faster**: Template rendering is instant vs. waiting for LLM response

### Implementation Strategy for V2
1. Keep the agent-generated FormattedSlide (pure data) the same across variants
2. Instead of LLM-generated variants, use the same FormattedSlide with different CSS themes
3. Generate 3 HTML outputs by rendering through different theme templates
4. Each render uses the design-guide.json for that theme (corporate=github, modern=modern, minimal=minimal)

### Pseudocode for V2 Variant Generation
```python
def generate_variants_v2(formatted_slide: FormattedSlide, theme_profiles: list) -> dict:
    """
    Args:
        formatted_slide: Pure data from ContentGeneratorAgentV2
        theme_profiles: ["github", "modern", "minimal"]

    Returns:
        {
            "variants": [
                {"profile": "corporate", "html": "..."},
                {"profile": "modern", "html": "..."},
                {"profile": "minimal", "html": "..."}
            ]
        }
    """
    variants = []
    for theme in theme_profiles:
        design_guide = load_design_guide(theme)  # design-guide.json
        html = render_slide(formatted_slide, theme, design_guide)
        variants.append({
            "profile": theme,
            "html": html
        })
    return {"variants": variants}
```

## Files to Update When Porting

1. `presentation/api/agents/content_generator_v2.py` - Add variant generation method
2. `presentation/api/routes/v2.py` - Add variant parameter to endpoint
3. `presentation/api/renderers/component_renderer.py` - Add theme switching support
4. Tests in `presentation/api/test_*.py` - Add variant tests

## References

- **Source Files**:
  - `/presentation/api/agents/content_generator.py:1245-1350` (_generate_variants method)
  - `/presentation/api/agents/content_generator.py:1172-1187` (variant dispatch logic)

- **Related**:
  - VariantGeneration schema in `presentation/api/agents/schemas.py`
  - VariantStyleParser in `presentation/api/services/variant_style_parser.py`

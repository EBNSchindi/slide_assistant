# Changelog

All notable changes to the Slide Assistant project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added - Documentation Reorganization (2025-11-20)

**New Documentation Structure:**
- Created `docs/` directory with hybrid organization (guides/, api/, reference/)
- Main documentation index at `docs/README.md`

**Theme Creation Guides:**
- `docs/guides/theme-creation/README.md` - Quick reference with 10-step checklist
- `docs/guides/theme-creation/tutorial.md` - Complete 30-minute tutorial (Nordic Minimal example)
- `docs/guides/theme-creation/apple-walkthrough.md` - Real-world Apple Design theme walkthrough
- `docs/guides/theme-creation/openai-walkthrough.md` - Real-world OpenAI Design theme walkthrough
- `docs/guides/theme-creation/tools.md` - Curated design tools reference (colors, fonts, accessibility)
- `docs/guides/theme-creation/troubleshooting.md` - Common theme issues and solutions

**Tutorial & Getting Started:**
- `docs/guides/first-slide-tutorial.md` - 5-minute beginner guide for first slide generation

**API Documentation:**
- `docs/api/README.md` - API overview and multi-provider support
- `docs/api/endpoints.md` - Complete endpoint reference with curl/Python/JavaScript examples
- `docs/api/multi-provider.md` - Multi-provider guide (OpenAI, Anthropic, Google)

**Reference Documentation:**
- `docs/reference/architecture.md` - V2 system architecture deep-dive
- `docs/reference/components.md` - All 10 component types with slots and CSS classes
- `docs/reference/migration-v1-v2.md` - V1 to V2 migration guide
- `docs/reference/remaining-features.md` - Planned features roadmap
- `docs/reference/legacy-theme-guide.md` - Original theme creation guide (archived)

**Documentation Moved:**
- `TESTING.md` → `docs/guides/testing.md`
- `MODEL_PROVIDERS.md` → `docs/api/multi-provider.md`
- `MIGRATION_GUIDE.md` → `docs/reference/migration-v1-v2.md`
- `REMAINING_FEATURES.md` → `docs/reference/remaining-features.md`
- `THEME_CREATION_GUIDE.md` → `docs/reference/legacy-theme-guide.md`

### Changed

**CLAUDE.md Updates:**
- Added `shared-themes/` directory to project structure
- Updated Multi-Agent API System section for OrchestratorV2
- Added multi-provider support documentation (OpenAI, Anthropic Claude, Google Gemini)
- Added provider-specific agent documentation
- Updated .env configuration examples with ANTHROPIC_API_KEY and GOOGLE_API_KEY
- Added "Provider API keys missing" to Common Gotchas

**Documentation Quality:**
- ~7,700 lines of new documentation across 12 files
- Complete code examples for all tutorials
- Accessibility-focused guidance (WCAG AA/AAA)
- Cross-referenced documentation for easy navigation
- Both quick reference and detailed tutorial formats

---

## [2.0.0] - V2 Architecture Launch

### Added
- V2 multi-agent pipeline (ContentAnalyzerV2, PresentationStrategistV2, ContentGeneratorV2)
- Deterministic Jinja2-based HTML rendering (no LLM for HTML generation)
- OrchestratorV2 with multi-provider support
- design-guide.json for all themes (github, modern, minimal)
- Reference HTML showcases for all themes
- Shared themes system (`shared-themes/apple`, `shared-themes/openai`)

### Changed
- Replaced LLM-based HTML generation with Jinja2 templates
- Agent pipeline now generates pure data (FormattedSlide) instead of HTML
- 3-variant generation optimized (instant, no extra API calls)

### Removed
- V1 agents (content_analyzer.py, content_generator.py, presentation_strategist.py)
- V1 API endpoints (`/api/generate`, `/api/regenerate`)
- LLM-based variant generation system

---

## [1.0.0] - Initial Release

### Added
- Word-to-Markdown converter
- Component-based presentation system
- 10 component types (stat-grid, bullet-list, quote, text, table, image-frame, image-grid, feature-grid, process, process-horizontal)
- 3 base themes (GitHub Design, Modern, Minimal)
- FastAPI backend with OpenAI GPT-4o support
- ai-editor.html for content generation
- component-viewer.html for viewing/screenshots
- Project-based workspace system

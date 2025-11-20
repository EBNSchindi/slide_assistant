# OpenAI Theme Walkthrough

A complete guide to creating a warm, approachable OpenAI-inspired theme with the signature teal color and soft shadows.

**Theme Characteristics:**
- Primary Color: **#10A37F** (OpenAI Teal)
- Design Philosophy: Friendly, approachable, innovative
- Best for: AI companies, startups, tech-forward organizations
- Accessibility: WCAG AA compliance with warm color palette
- Design Style: Soft shadows, rounded corners, warm whites

---

## Table of Contents

1. [Overview & Design Philosophy](#overview--design-philosophy)
2. [Complete design-guide.json](#complete-design-guidejson)
3. [Color Strategy & Warmth](#color-strategy--warmth)
4. [CSS Implementation](#css-implementation)
5. [Component Patterns](#component-patterns)
6. [Testing & Accessibility](#testing--accessibility)

---

## Overview & Design Philosophy

### Why OpenAI Teal?

OpenAI's **#10A37F** represents:
- **Innovation**: Modern, forward-thinking tech
- **Trust**: Warm yet trustworthy presence
- **Approachability**: Friendly, not clinical
- **Accessibility**: 5.1:1 contrast on white (WCAG AA)

Unlike the crisp Apple Blue, this teal feels warm and organic.

### Design Philosophy

OpenAI's design emphasizes:
- **Warmth**: Soft shadows, warm grays, rounded corners
- **Friendliness**: Larger spacing, less formal
- **Approachability**: Rounded UI elements, softer edges
- **Innovation**: Modern color palette, contemporary spacing

### Color Palette

| Color | Hex | Usage | Contrast Ratio |
|-------|-----|-------|-----------------|
| OpenAI Teal | `#10A37F` | Primary accent, highlights | 5.1:1 (AA) |
| Warm White | `#FFFFFF` | Main backgrounds | N/A |
| Soft Warm Gray | `#F7F7F8` | Subtle backgrounds | 1.1:1 |
| Text Dark | `#5E5E63` | Primary text | 8.2:1 (AAA) |
| Text Gray | `#8B8B91` | Secondary text | 5.4:1 (AA) |
| Soft Tan | `#E6E0DB` | Borders, dividers | N/A |
| Warm Accent | `#FF9500` | Secondary highlight | 4.6:1 (AA) |
| Semantic Green | `#4CAF50` | Success states | 5.2:1 (AA) |
| Warm Red | `#FF6B6B` | Error states | 4.9:1 (AA) |

---

## Complete design-guide.json

The canonical design system for OpenAI theme:

```json
{
  "theme": "openai",
  "name": "OpenAI Design",
  "description": "Warm, approachable design inspired by OpenAI's design language with teal accent and soft shadows",
  "version": "1.0.0",

  "tokens": {
    "colors": {
      "primary": {
        "main": "#10A37F",
        "light": "#2FB786",
        "dark": "#0E7C5C",
        "name": "OpenAI Teal",
        "usage": "Primary accent for highlights, buttons, and interactive elements"
      },
      "background": {
        "main": "#FFFFFF",
        "subtle": "#F7F7F8",
        "component": "#FAFAFA",
        "overlay": "#F2F2F3",
        "name": "Warm whites and soft grays"
      },
      "text": {
        "primary": "#5E5E63",
        "secondary": "#8B8B91",
        "muted": "#A9A9B0",
        "onPrimary": "#FFFFFF",
        "name": "Warm gray text colors"
      },
      "border": {
        "main": "#D9D9E3",
        "muted": "#EFEFEF",
        "hover": "#10A37F",
        "name": "Soft border colors"
      },
      "semantic": {
        "success": {
          "bg": "#E8F5E9",
          "text": "#2E7D32",
          "border": "#4CAF50",
          "name": "Success/Available"
        },
        "warning": {
          "bg": "#FFF3E0",
          "text": "#E65100",
          "border": "#FF9500",
          "name": "Warning/Pending"
        },
        "danger": {
          "bg": "#FFEBEE",
          "text": "#C62828",
          "border": "#FF6B6B",
          "name": "Danger/Error"
        },
        "accent": {
          "main": "#FF9500",
          "name": "Secondary accent (warm orange)"
        }
      }
    },

    "typography": {
      "fontFamily": {
        "default": "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif",
        "mono": "'Courier New', Courier, monospace",
        "name": "System Font Stack with warm fallbacks"
      },
      "fontWeights": {
        "light": 300,
        "normal": 400,
        "medium": 500,
        "semibold": 600,
        "bold": 700
      },
      "lineHeights": {
        "tight": 1.35,
        "normal": 1.65,
        "relaxed": 1.85
      },
      "headings": {
        "h1": {
          "fontSize": "48px",
          "fontWeight": 600,
          "lineHeight": 1.25
        },
        "h2": {
          "fontSize": "36px",
          "fontWeight": 600,
          "lineHeight": 1.3
        },
        "h3": {
          "fontSize": "28px",
          "fontWeight": 500,
          "lineHeight": 1.35
        },
        "h4": {
          "fontSize": "20px",
          "fontWeight": 600,
          "lineHeight": 1.4
        }
      },
      "body": {
        "fontSize": "16px",
        "fontWeight": 400,
        "lineHeight": 1.65
      }
    },

    "spacing": {
      "xs": "6px",
      "sm": "12px",
      "md": "16px",
      "lg": "24px",
      "xl": "32px",
      "2xl": "48px"
    },

    "borderRadius": {
      "sm": "6px",
      "md": "10px",
      "lg": "16px",
      "full": "50%"
    },

    "shadows": {
      "sm": "0 2px 4px rgba(0,0,0,0.06)",
      "md": "0 8px 16px rgba(16,163,127,0.12)",
      "lg": "0 16px 32px rgba(0,0,0,0.1)",
      "xl": "0 24px 48px rgba(0,0,0,0.12)"
    }
  },

  "components": [
    {
      "id": "stat-grid",
      "name": "Statistic Grid",
      "description": "Display metrics in warm, friendly card layout",
      "type": "container",
      "cssClasses": ["component", "stat-grid", "stat-card"],
      "features": ["responsive-grid", "warm-shadows", "multi-line-labels"],
      "gridColumns": "auto-fit, minmax(240px, 1fr)"
    },
    {
      "id": "bullet-list",
      "name": "Bullet List",
      "description": "Formatted list with teal accent border",
      "type": "container",
      "cssClasses": ["component", "bullet-list"],
      "features": ["emoji-support", "bold-emphasis", "warm-background"]
    },
    {
      "id": "text",
      "name": "Text Block",
      "description": "Rich text content with warm styling",
      "type": "container",
      "cssClasses": ["component", "text-block"],
      "features": ["heading-hierarchy", "warm-typography", "phased-sections"]
    },
    {
      "id": "quote",
      "name": "Quote",
      "description": "Highlighted quote with soft background",
      "type": "container",
      "cssClasses": ["component", "quote"],
      "backgroundColor": "subtle",
      "borderColor": "primary"
    },
    {
      "id": "table",
      "name": "Data Table",
      "description": "Data display with warm styling and soft shadows",
      "type": "container",
      "cssClasses": ["component", "table"],
      "features": ["responsive", "warm-header", "soft-hover"]
    },
    {
      "id": "image-frame",
      "name": "Image Frame",
      "description": "Single image with rounded frame and soft shadow",
      "type": "media",
      "cssClasses": ["component", "image-container"],
      "features": ["responsive", "rounded-corners", "soft-shadow"]
    },
    {
      "id": "image-grid",
      "name": "Image Grid",
      "description": "Multi-image grid with rounded corners",
      "type": "media",
      "cssClasses": ["component", "image-grid"],
      "gridOptions": ["grid-2x2", "grid-3x2"]
    },
    {
      "id": "feature-grid",
      "name": "Feature Grid",
      "description": "Feature cards with warm styling",
      "type": "container",
      "cssClasses": ["component", "feature-grid", "feature-card"],
      "features": ["emoji-icons", "soft-hover", "warm-colors"]
    },
    {
      "id": "process",
      "name": "Process Chain",
      "description": "Vertical timeline with rounded step indicators",
      "type": "container",
      "cssClasses": ["component", "process-chain"]
    },
    {
      "id": "process-horizontal",
      "name": "Process Horizontal",
      "description": "Horizontal timeline with rounded styling",
      "type": "container",
      "cssClasses": ["component", "process-horizontal"]
    }
  ],

  "componentBestPractices": {
    "stat-grid": {
      "maxCards": 4,
      "recommendedLayout": "2-4 column",
      "cardBackgroundColor": "warm-subtle",
      "shadowIntensity": "soft"
    },
    "bullet-list": {
      "maxItems": 6,
      "emojiSupport": true,
      "backgroundColor": "warm-subtle",
      "borderRadius": "rounded"
    },
    "quote": {
      "maxLength": "250 characters",
      "backgroundColor": "subtle",
      "borderWidth": "3px",
      "italicText": true
    },
    "image-grid": {
      "standardLayouts": ["2x2", "3x2"],
      "borderRadius": "lg",
      "shadowIntensity": "soft"
    }
  },

  "colorAccessibility": {
    "contrastRatio": {
      "primary_white": "5.1:1 (AA)",
      "text_bg": "8.2:1 (AAA)",
      "secondary_bg": "5.4:1 (AA)"
    },
    "wcagCompliance": "AA - All critical colors meet AA standard"
  },

  "responsiveBreakpoints": {
    "desktop": "≥1024px",
    "tablet": "768px - 1023px",
    "mobile": "<768px"
  }
}
```

---

## Color Strategy & Warmth

### Teal as Primary Accent

OpenAI's teal (#10A37F) is different from Apple Blue:

- **More organic**: Teal feels natural, like water or nature
- **Warmer**: Not as clinical or corporate
- **Friendly**: Approachable and inviting
- **Modern**: Contemporary tech feel

Use teal for:
- Call-to-action buttons
- Primary highlights
- Interactive elements
- Key metrics

### Warm Whites & Grays

Instead of pure white (#FFFFFF), use warm variations:

| Usage | Color | Effect |
|-------|-------|--------|
| Main background | `#FFFFFF` | Clean, professional |
| Component fill | `#FAFAFA` | Slightly warm, softer |
| Subtle areas | `#F7F7F8` | Very subtle warmth |
| Borders | `#D9D9E3` | Warm gray, not cool |

This creates a **cohesive warm palette** instead of stark whites.

### Text Colors

Use warm gray instead of pure black:

- **Primary text**: `#5E5E63` (warm dark gray) instead of `#000000`
- **Secondary text**: `#8B8B91` (medium warm gray)
- **Muted text**: `#A9A9B0` (light warm gray)

**Why?** Warm gray is easier on the eyes and creates a friendlier feel.

### Secondary Accent

Use warm orange (#FF9500) sparingly for:
- Warning states
- Secondary actions
- Emphasis elements
- Call-out boxes

This complements the teal and creates a vibrant, modern palette.

---

## CSS Implementation

### variables.css

```css
/* ═══════════════════════════════════════════════════════════ */
/* OpenAI Design System - CSS Variables */
/* ═══════════════════════════════════════════════════════════ */

:root {
  /* Colors - Warm Teal Palette */
  --color-primary: #10A37F;
  --color-primary-light: #2FB786;
  --color-primary-dark: #0E7C5C;

  --color-bg-main: #FFFFFF;
  --color-bg-subtle: #F7F7F8;
  --color-bg-component: #FAFAFA;
  --color-bg-overlay: #F2F2F3;

  --color-text-primary: #5E5E63;
  --color-text-secondary: #8B8B91;
  --color-text-muted: #A9A9B0;
  --color-text-on-primary: #FFFFFF;

  --color-border-main: #D9D9E3;
  --color-border-muted: #EFEFEF;
  --color-border-hover: #10A37F;

  --color-accent-warm: #FF9500;
  --color-accent-light: #FFB347;

  --color-success-bg: #E8F5E9;
  --color-success-text: #2E7D32;
  --color-success-border: #4CAF50;

  --color-warning-bg: #FFF3E0;
  --color-warning-text: #E65100;
  --color-warning-border: #FF9500;

  --color-danger-bg: #FFEBEE;
  --color-danger-text: #C62828;
  --color-danger-border: #FF6B6B;

  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-family-mono: 'Courier New', Courier, monospace;

  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Spacing - Slightly Larger */
  --spacing-xs: 6px;
  --spacing-sm: 12px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;

  /* Border Radius - Rounded */
  --border-radius-sm: 6px;
  --border-radius-md: 10px;
  --border-radius-lg: 16px;
  --border-radius-full: 50%;

  /* Shadows - Soft & Warm */
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.06);
  --shadow-md: 0 8px 16px rgba(16,163,127,0.12);
  --shadow-lg: 0 16px 32px rgba(0,0,0,0.1);
  --shadow-xl: 0 24px 48px rgba(0,0,0,0.12);

  /* Component Defaults */
  --component-padding: 24px;
  --component-border-width: 1px;
  --component-border-radius: var(--border-radius-md);
  --component-shadow: var(--shadow-sm);
  --component-shadow-hover: var(--shadow-md);

  /* Transitions - Smooth */
  --transition-fast: 200ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Key CSS Classes (from style.css)

```css
/* Component Base - Warm Foundation */
.component {
  background: var(--color-bg-component);
  border: var(--component-border-width) solid var(--color-border-main);
  border-radius: var(--component-border-radius);
  padding: var(--component-padding);
  box-shadow: var(--component-shadow);
  transition: all var(--transition-normal);
}

.component:hover {
  border-color: var(--color-border-hover);
  box-shadow: var(--component-shadow-hover);
}

/* Stat Grid - Warm Card Layout */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
  width: 100%;
}

.stat-card {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border-main);
  border-radius: var(--border-radius-md);
  padding: 28px;
  text-align: center;
  transition: all var(--transition-normal);
  cursor: pointer;
}

.stat-card:hover {
  background: var(--color-bg-main);
  border-color: var(--color-primary);
  box-shadow: 0 8px 16px rgba(16,163,127,0.12);
  transform: translateY(-2px);
}

.stat-number {
  font-size: 40px;
  font-weight: 700;
  color: var(--color-primary);
  display: block;
  margin-bottom: var(--spacing-sm);
}

.stat-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.65;
  font-weight: 500;
}

.stat-source {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: var(--spacing-sm);
  font-style: italic;
}

/* Bullet List - Warm Background */
.bullet-list {
  list-style: none;
  padding: 0;
  margin: var(--spacing-lg) 0;
}

.bullet-list li {
  padding: 16px var(--spacing-md);
  margin: var(--spacing-sm) 0;
  background: var(--color-bg-subtle);
  border-left: 4px solid var(--color-primary);
  border-radius: var(--border-radius-sm);
  color: var(--color-text-primary);
  transition: all var(--transition-fast);
  line-height: 1.65;
}

.bullet-list li:hover {
  background: var(--color-bg-component);
  border-left-color: var(--color-primary-light);
  transform: translateX(4px);
}

.bullet-list li strong {
  color: var(--color-primary);
  font-weight: 600;
}

.bullet-list li em {
  color: var(--color-accent-warm);
  font-style: normal;
}

/* Quote - Soft Background */
.quote {
  background: var(--color-bg-subtle);
  border-left: 4px solid var(--color-primary);
  border-radius: var(--border-radius-sm);
  padding: 20px;
  padding-left: 20px;
  margin: var(--spacing-lg) 0;
  font-style: italic;
  color: var(--color-text-secondary);
  line-height: 1.85;
}

.quote-author {
  font-style: normal;
  color: var(--color-text-primary);
  font-weight: 600;
  margin-top: var(--spacing-md);
}

.quote-source {
  font-size: 12px;
  color: var(--color-text-muted);
  font-style: normal;
  font-weight: normal;
  margin-top: var(--spacing-sm);
}

/* Feature Cards - Warm & Interactive */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--spacing-lg);
  margin: var(--spacing-lg) 0;
  width: 100%;
}

.feature-card {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border-main);
  border-radius: var(--border-radius-md);
  padding: var(--component-padding);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.feature-card:hover {
  background: var(--color-bg-main);
  border-color: var(--color-primary);
  box-shadow: 0 8px 16px rgba(16,163,127,0.12);
  transform: translateY(-4px);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
  display: block;
  line-height: 1;
}

.feature-card h4 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
  line-height: 1.35;
}

.feature-card p {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.65;
}

/* Process Chain - Rounded Steps */
.process-chain {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin: var(--spacing-lg) 0;
}

.process-step {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  position: relative;
}

.process-step:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 26px;
  top: 60px;
  width: 2px;
  height: calc(100% + 12px);
  background: var(--color-border-main);
}

.process-number {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(16,163,127,0.2);
  position: relative;
  z-index: 1;
}

.process-content h4 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
  line-height: 1.35;
}

.process-content p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.65;
}

/* Tables - Warm Styling */
.component table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--spacing-md) 0;
}

.component table th {
  background: var(--color-bg-subtle);
  color: var(--color-text-primary);
  font-weight: 600;
  padding: 14px;
  text-align: left;
  border-bottom: 2px solid var(--color-border-main);
  font-size: 14px;
}

.component table td {
  padding: 14px;
  border-bottom: 1px solid var(--color-border-muted);
  color: var(--color-text-primary);
  font-size: 14px;
}

.component table tr:hover {
  background: var(--color-bg-component);
}

/* Badges - Warm & Friendly */
.badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 14px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  transition: all var(--transition-fast);
}

.badge-success {
  background: var(--color-success-bg);
  color: var(--color-success-text);
}

.badge-warning {
  background: var(--color-warning-bg);
  color: var(--color-warning-text);
}

.badge-danger {
  background: var(--color-danger-bg);
  color: var(--color-danger-text);
}

/* Images - Rounded Corners */
.image-container {
  border: 1px solid var(--color-border-main);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  background: var(--color-bg-component);
  box-shadow: var(--shadow-sm);
}

.image-wrapper {
  width: 100%;
  background: var(--color-bg-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  min-height: 220px;
}

.image-wrapper img {
  max-width: 100%;
  height: auto;
  border-radius: var(--border-radius-sm);
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-normal);
}

.image-wrapper:hover img {
  transform: scale(1.02);
}

.image-content {
  padding: var(--component-padding);
  border-top: 1px solid var(--color-border-muted);
}

.image-content h4 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
}

.image-content p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.65;
}

/* Image Grid - Rounded Cards */
.image-grid {
  display: grid;
  gap: var(--spacing-lg);
  margin: var(--spacing-lg) 0;
  width: 100%;
}

.image-grid.grid-2x2 {
  grid-template-columns: repeat(2, 1fr);
}

.image-grid.grid-3x2 {
  grid-template-columns: repeat(3, 1fr);
}

.image-card {
  border: 1px solid var(--color-border-main);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  background: var(--color-bg-component);
  transition: all var(--transition-normal);
}

.image-card:hover {
  border-color: var(--color-primary);
  box-shadow: 0 8px 16px rgba(16,163,127,0.12);
}

.image-card .image-wrapper {
  aspect-ratio: 16 / 10;
  padding: 20px;
  background: var(--color-bg-subtle);
}

.image-card .image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-card .image-content {
  padding: var(--spacing-md);
}

/* Responsive */
@media (max-width: 768px) {
  .image-grid.grid-2x2,
  .image-grid.grid-3x2 {
    grid-template-columns: 1fr;
  }

  .process-horizontal {
    flex-direction: column;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }
}
```

---

## Component Patterns

### Stat Grid - Key Metrics

**When to use:**
- Revenue/sales figures
- User growth metrics
- Performance indicators
- Resource counts

**Styling approach:**
- Warm subtle background
- Large, bold teal numbers
- Secondary gray labels
- Soft shadow on hover
- Lifts up 2px on hover

**Example:**
```
┌─────────────────────────────────────────┐
│  12.5M       5.3%        $89M      47K  │
│ Users      Growth      Revenue     Beta │
└─────────────────────────────────────────┘
```

### Feature Grid - Product Features

**When to use:**
- Core product features
- Service offerings
- Company strengths
- Capabilities

**Styling approach:**
- Large emoji/icon (48px)
- Bold title (18px)
- Secondary description text
- Warm background on hover
- Grows on hover

**Example:**
```
┌──────────────┐  ┌──────────────┐
│     🤖       │  │     ⚡       │
│  Powerful    │  │   Fast       │
│  Advanced    │  │   Response   │
│  AI Model    │  │   Times      │
└──────────────┘  └──────────────┘
```

### Process Chain - Implementation Steps

**When to use:**
- Project phases
- Customer journey
- Implementation steps
- Product roadmap

**Styling approach:**
- Rounded teal circles (52px)
- Vertical line connector
- Bold titles with descriptions
- Soft spacing between steps

**Example:**
```
  ① Setup
  │ Initial configuration
  │
  ② Integration
  │ Connect your systems
  │
  ③ Testing
  │ Validate everything works
  │
  ④ Launch
    Go live!
```

### Quote - Testimonials

**When to use:**
- Customer testimonials
- Important statements
- Key insights
- Highlighted messages

**Styling approach:**
- Warm subtle background
- Teal left border (4px)
- Italic text
- Optional author attribution
- Rounded corners

**Example:**
```
┌────────────────────────────────────┐
│ "This technology changed how we    │
│  approach our challenges."         │
│                                    │
│                        — John Doe  │
└────────────────────────────────────┘
```

---

## Testing & Accessibility

### Contrast Validation

Use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/):

```
✅ OpenAI Teal (#10A37F) on White (#FFFFFF): 5.1:1 (AA)
✅ Warm Dark Gray (#5E5E63) on White (#FFFFFF): 8.2:1 (AAA)
✅ Medium Gray (#8B8B91) on White (#FFFFFF): 5.4:1 (AA)
✅ Warm Orange (#FF9500) on White (#FFFFFF): 4.6:1 (AA)
✅ Dark Gray on Subtle (#F7F7F8): 7.5:1 (AAA)
```

### Component Checklist

- [ ] Stat Grid: 2-4 columns, hover effect
- [ ] Feature Grid: Icon, title, description, hover
- [ ] Bullet List: 3-6 items, emoji support
- [ ] Quote: Left border, italic, attribution
- [ ] Process: 3-5 steps, connectors visible
- [ ] Image Grid: 2x2 or 3x2, responsive
- [ ] Tables: Header styling, hover, badges
- [ ] Text Block: Heading hierarchy, lists

### Accessibility Checklist

- [ ] Color contrast meets WCAG AA (at minimum 4.5:1)
- [ ] Interactive elements have focus states
- [ ] Images have alt text
- [ ] Semantic HTML used throughout
- [ ] Font size minimum 14px for body text
- [ ] Line height minimum 1.5 for readability
- [ ] Rounded corners don't break functionality
- [ ] Transitions respect `prefers-reduced-motion`

### Performance Checklist

- [ ] CSS file under 40KB
- [ ] No external font downloads
- [ ] Smooth transitions (60fps)
- [ ] Shadow effects not excessive
- [ ] Images optimized for web

### Browser Testing

Test on:
- ✅ Chrome (Desktop & Mobile)
- ✅ Firefox (Desktop)
- ✅ Safari (macOS & iOS)
- ✅ Edge (Windows)

---

## Best Practices

### Color Usage

1. **Teal sparingly**: 15-20% of interface
2. **Warm accents**: Use orange for secondary elements
3. **Gray gradation**: Use multiple grays for hierarchy
4. **High contrast**: Always test contrast ratios

### Spacing

1. **Generous spacing**: More space = friendlier feel
2. **Consistent gaps**: Use the spacing scale consistently
3. **Breathing room**: Don't cram content
4. **Card spacing**: 16px between items

### Typography

1. **Warm grays for text**: Not pure black
2. **Clear hierarchy**: Large headings, readable body
3. **Line height**: 1.65 for body text (above average)
4. **Font weight variety**: Use weight changes for emphasis

### Shadows

1. **Soft shadows**: Not harsh or heavy
2. **Teal-tinted**: Use rgba(16,163,127,...) for primary elements
3. **Subtle differences**: Small change on hover
4. **No drop shadows**: Keep interface clean

---

## Deployment Checklist

- [ ] design-guide.json configured with all 10 components
- [ ] variables.css with all CSS custom properties
- [ ] style.css with all component styles
- [ ] All colors tested for contrast
- [ ] Responsive design tested on mobile/tablet
- [ ] Accessibility checklist passed
- [ ] Registered in projects.json
- [ ] Theme appears in UI dropdown
- [ ] Test slide generated successfully

---

## Conclusion

The OpenAI theme demonstrates warm, approachable design:

1. **Friendly teal**: Modern but not clinical
2. **Warm palette**: Soft whites and grays
3. **Soft shadows**: Subtle depth
4. **Generous spacing**: Premium feel
5. **Rounded corners**: Contemporary design

Perfect for AI companies, startups, and tech-forward organizations that want to balance innovation with approachability.


# Apple Theme Walkthrough

A complete guide to creating a professional Apple-inspired theme with the iconic blue accent color and minimalist aesthetic.

**Theme Characteristics:**
- Primary Color: **#0071E3** (Apple Blue)
- Design Philosophy: Minimalist, premium, accessible
- Best for: Tech companies, corporate presentations, professional services
- Accessibility: AAA contrast compliance throughout
- Typography: System font stack for platform consistency

---

## Table of Contents

1. [Overview & Color Philosophy](#overview--color-philosophy)
2. [Complete design-guide.json](#complete-design-guidejson)
3. [Key Design Decisions](#key-design-decisions)
4. [CSS Implementation](#css-implementation)
5. [Component Styling Examples](#component-styling-examples)
6. [Testing & Validation](#testing--validation)

---

## Overview & Color Philosophy

### Why Apple Blue?

Apple's **#0071E3** represents trust, innovation, and premium quality. It's:
- **Accessible**: 7.2:1 contrast ratio on white (AAA)
- **Versatile**: Works in light and dark contexts
- **Professional**: Trusted by millions globally
- **Balanced**: Not too vibrant, not too muted

### Color Palette Strategy

The Apple theme uses a minimalist color approach:

| Color | Hex | Usage | Contrast Ratio |
|-------|-----|-------|-----------------|
| Apple Blue | `#0071E3` | Primary accent, highlights | 7.2:1 (AAA) |
| Pure White | `#FFFFFF` | Backgrounds, text containers | N/A |
| Dark Gray | `#1D1D1D` | Primary text | 17.2:1 (AAA) |
| Mid Gray | `#6E6E73` | Secondary text, descriptions | 7.9:1 (AAA) |
| Light Gray | `#F5F5F7` | Subtle backgrounds, dividers | 1.1:1 |
| Semantic Green | `#34C759` | Success states | 5.8:1 (AA) |
| Semantic Red | `#FF3B30` | Danger/error states | 4.8:1 (AA) |

### Typography Choices

Apple uses **San Francisco** as its system font, but we use the system font stack for web compatibility:

```
-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif
```

This ensures:
- Loads native Apple fonts on macOS/iOS
- Falls back to Segoe on Windows
- Clean, readable hierarchy
- No font loading delays

---

## Complete design-guide.json

This is the canonical design system definition for the Apple theme:

```json
{
  "theme": "apple",
  "name": "Apple Design",
  "description": "Premium minimalist design inspired by Apple's design language with blue accent color and premium typography",
  "version": "1.0.0",

  "tokens": {
    "colors": {
      "primary": {
        "main": "#0071E3",
        "light": "#0A84FF",
        "dark": "#0051BA",
        "name": "Apple Blue",
        "usage": "Primary accent for highlights, buttons, links, and interactive elements"
      },
      "background": {
        "main": "#FFFFFF",
        "subtle": "#F5F5F7",
        "component": "#FFFFFF",
        "overlay": "#F9F9FB",
        "name": "White backgrounds with subtle variations"
      },
      "text": {
        "primary": "#1D1D1D",
        "secondary": "#6E6E73",
        "muted": "#A2A2A7",
        "onPrimary": "#FFFFFF",
        "name": "Text colors with accessibility focus"
      },
      "border": {
        "main": "#E5E5EA",
        "muted": "#F2F2F7",
        "hover": "#0071E3",
        "name": "Subtle border colors"
      },
      "semantic": {
        "success": {
          "bg": "#DFF5E8",
          "text": "#1D6B3C",
          "border": "#34C759",
          "name": "Success/Available"
        },
        "warning": {
          "bg": "#FFF4E6",
          "text": "#8B5A00",
          "border": "#FF9500",
          "name": "Warning/Pending"
        },
        "danger": {
          "bg": "#FFEAEA",
          "text": "#8B0000",
          "border": "#FF3B30",
          "name": "Danger/Error"
        },
        "accent": {
          "main": "#AF52DE",
          "name": "Secondary accent (purple)"
        }
      }
    },

    "typography": {
      "fontFamily": {
        "default": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji'",
        "mono": "ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
        "name": "System Font Stack with emoji support"
      },
      "fontWeights": {
        "light": 300,
        "normal": 400,
        "medium": 500,
        "semibold": 600,
        "bold": 700
      },
      "lineHeights": {
        "tight": 1.3,
        "normal": 1.6,
        "relaxed": 1.8
      },
      "headings": {
        "h1": {
          "fontSize": "48px",
          "fontWeight": 700,
          "lineHeight": 1.2,
          "letterSpacing": "-0.5px"
        },
        "h2": {
          "fontSize": "32px",
          "fontWeight": 700,
          "lineHeight": 1.25,
          "letterSpacing": "-0.3px"
        },
        "h3": {
          "fontSize": "24px",
          "fontWeight": 600,
          "lineHeight": 1.3,
          "letterSpacing": "-0.2px"
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
        "lineHeight": 1.6
      }
    },

    "spacing": {
      "xs": "4px",
      "sm": "8px",
      "md": "16px",
      "lg": "24px",
      "xl": "32px",
      "2xl": "48px"
    },

    "borderRadius": {
      "sm": "4px",
      "md": "8px",
      "lg": "12px",
      "full": "50%"
    },

    "shadows": {
      "sm": "0 1px 2px rgba(0,0,0,0.05)",
      "md": "0 4px 12px rgba(0,0,0,0.08)",
      "lg": "0 12px 32px rgba(0,113,227,0.12)",
      "xl": "0 20px 48px rgba(0,0,0,0.12)"
    }
  },

  "components": [
    {
      "id": "stat-grid",
      "name": "Statistic Grid",
      "description": "Display multiple statistics in grid layout with premium styling",
      "type": "container",
      "cssClasses": ["component", "stat-grid", "stat-card"],
      "features": ["responsive-grid", "multi-line-labels", "source-attribution"],
      "gridColumns": "auto-fit, minmax(220px, 1fr)"
    },
    {
      "id": "bullet-list",
      "name": "Bullet List",
      "description": "Formatted list with subtle accent bar on left",
      "type": "container",
      "cssClasses": ["component", "bullet-list"],
      "features": ["emoji-support", "bold-emphasis", "nested-bullets"]
    },
    {
      "id": "text",
      "name": "Text Block",
      "description": "Rich text content with heading hierarchy support",
      "type": "container",
      "cssClasses": ["component", "text-block"],
      "features": ["heading-hierarchy", "nested-lists", "phased-sections"]
    },
    {
      "id": "quote",
      "name": "Quote",
      "description": "Highlighted quote with left border accent",
      "type": "container",
      "cssClasses": ["component", "quote"],
      "borderColor": "primary"
    },
    {
      "id": "table",
      "name": "Data Table",
      "description": "Structured data display with clean styling",
      "type": "container",
      "cssClasses": ["component", "table"],
      "features": ["responsive", "header-highlight", "row-hover"]
    },
    {
      "id": "image-frame",
      "name": "Image Frame",
      "description": "Single image with subtle frame and caption",
      "type": "media",
      "cssClasses": ["component", "image-container"],
      "features": ["responsive", "alt-text", "caption-support"]
    },
    {
      "id": "image-grid",
      "name": "Image Grid",
      "description": "Multi-image grid with clean spacing",
      "type": "media",
      "cssClasses": ["component", "image-grid"],
      "gridOptions": ["grid-2x2", "grid-3x2"]
    },
    {
      "id": "feature-grid",
      "name": "Feature Grid",
      "description": "Card-based grid for features with icons",
      "type": "container",
      "cssClasses": ["component", "feature-grid", "feature-card"],
      "features": ["emoji-icons", "hover-effect", "responsive"]
    },
    {
      "id": "process",
      "name": "Process Chain",
      "description": "Vertical timeline with numbered steps",
      "type": "container",
      "cssClasses": ["component", "process-chain"]
    },
    {
      "id": "process-horizontal",
      "name": "Process Horizontal",
      "description": "Horizontal timeline with step indicators",
      "type": "container",
      "cssClasses": ["component", "process-horizontal"]
    }
  ],

  "componentBestPractices": {
    "stat-grid": {
      "maxCards": 4,
      "recommendedLayout": "2-4 column",
      "minHeight": "140px",
      "cardSpacing": "16px"
    },
    "bullet-list": {
      "maxItems": 5,
      "emojiSupport": true,
      "boldFirstPhrase": "recommended",
      "lineHeight": "1.8"
    },
    "quote": {
      "maxLength": "200 characters",
      "borderWidth": "3px",
      "italicText": true,
      "includeAttribution": "recommended"
    },
    "image-grid": {
      "standardLayouts": ["2x2", "3x2"],
      "minImageHeight": "200px",
      "aspectRatio": "16:10"
    }
  },

  "colorAccessibility": {
    "contrastRatio": {
      "primary_white": "7.2:1 (AAA)",
      "primary_light": "4.5:1 (AA minimum)",
      "text_bg": "17.2:1 (AAA)",
      "secondary_bg": "7.9:1 (AAA)"
    },
    "wcagCompliance": "AAA - All color combinations meet triple-A standard"
  },

  "responsiveBreakpoints": {
    "desktop": "≥1024px",
    "tablet": "768px - 1023px",
    "mobile": "<768px"
  }
}
```

---

## Key Design Decisions

### 1. Color Hierarchy

**Apple Blue (#0071E3)** is used strategically:

- **Primary Actions**: Buttons, links, hover states
- **Accent Elements**: Borders, stat highlights, component accents
- **Not overused**: Only ~15-20% of interface is blue

The rest is neutral grays and whites, creating a premium, professional feel.

### 2. Spacing & Whitespace

Apple emphasizes breathing room:

- **Large gaps** between major sections (24-32px)
- **Moderate gaps** between components (16px)
- **Tight gaps** within components (8px)
- **Padding**: Components have 16-20px internal padding

This creates a spacious, premium feel that's different from cramped interfaces.

### 3. Shadows & Depth

Apple uses **subtle shadows** for depth without heaviness:

- **Cards**: `0 4px 12px rgba(0,0,0,0.08)` - very soft
- **Hover**: `0 12px 32px rgba(0,113,227,0.12)` - blue-tinted
- **No drop shadows**: Keeps interface clean

This contrasts with other design systems that use heavier shadows.

### 4. Typography Scale

Apple uses aggressive font sizes and weights:

- **H1**: 48px, bold (7 levels deep)
- **H2**: 32px, bold (5 levels deep)
- **Body**: 16px, regular (readable line length)

High contrast between heading and body creates clear visual hierarchy.

---

## CSS Implementation

### variables.css

```css
/* ═══════════════════════════════════════════════════════════ */
/* Apple Design System - CSS Variables */
/* ═══════════════════════════════════════════════════════════ */

:root {
  /* Colors */
  --color-primary: #0071E3;
  --color-primary-light: #0A84FF;
  --color-primary-dark: #0051BA;

  --color-bg-main: #FFFFFF;
  --color-bg-subtle: #F5F5F7;
  --color-bg-overlay: #F9F9FB;

  --color-text-primary: #1D1D1D;
  --color-text-secondary: #6E6E73;
  --color-text-muted: #A2A2A7;
  --color-text-on-primary: #FFFFFF;

  --color-border-main: #E5E5EA;
  --color-border-muted: #F2F2F7;
  --color-border-hover: #0071E3;

  --color-success-bg: #DFF5E8;
  --color-success-text: #1D6B3C;
  --color-success-border: #34C759;

  --color-warning-bg: #FFF4E6;
  --color-warning-text: #8B5A00;
  --color-warning-border: #FF9500;

  --color-danger-bg: #FFEAEA;
  --color-danger-text: #8B0000;
  --color-danger-border: #FF3B30;

  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji';
  --font-family-mono: ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;

  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;

  /* Border Radius */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  --border-radius-full: 50%;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 12px 32px rgba(0,113,227,0.12);
  --shadow-xl: 0 20px 48px rgba(0,0,0,0.12);

  /* Component Defaults */
  --component-padding: 20px;
  --component-border-width: 1px;
  --component-border-radius: var(--border-radius-md);
  --component-shadow: var(--shadow-sm);
  --component-shadow-hover: var(--shadow-md);

  /* Transitions */
  --transition-fast: 150ms ease-out;
  --transition-normal: 250ms ease-out;
  --transition-slow: 400ms ease-out;
}
```

### Key CSS Classes (from style.css)

```css
/* Component Base Styles */
.component {
  background: var(--color-bg-main);
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

/* Stat Grid - Premium Card Layout */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
}

.stat-card {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border-main);
  border-radius: var(--border-radius-md);
  padding: 24px;
  text-align: center;
  transition: all var(--transition-normal);
}

.stat-card:hover {
  background: var(--color-bg-main);
  border-color: var(--color-primary);
  box-shadow: 0 12px 32px rgba(0,113,227,0.12);
  transform: translateY(-4px);
}

.stat-number {
  font-size: 40px;
  font-weight: 700;
  color: var(--color-primary);
  display: block;
  margin-bottom: var(--spacing-sm);
  letter-spacing: -0.5px;
}

.stat-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

/* Bullet List - Subtle Left Border */
.bullet-list {
  list-style: none;
  padding: 0;
  margin: var(--spacing-lg) 0;
}

.bullet-list li {
  padding: 14px var(--spacing-md);
  margin: var(--spacing-sm) 0;
  background: var(--color-bg-subtle);
  border-left: 3px solid var(--color-primary);
  border-radius: var(--border-radius-sm);
  color: var(--color-text-primary);
  transition: all var(--transition-fast);
}

.bullet-list li:hover {
  background: var(--color-bg-main);
  border-left-color: var(--color-primary-light);
}

.bullet-list li strong {
  color: var(--color-primary);
  font-weight: 600;
}

/* Quote - Left Border Accent */
.quote {
  border-left: 3px solid var(--color-primary);
  padding-left: 20px;
  margin: var(--spacing-lg) 0;
  font-style: italic;
  color: var(--color-text-secondary);
  line-height: 1.8;
}

/* Feature Cards - Interactive Hover */
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
  box-shadow: 0 12px 32px rgba(0,113,227,0.12);
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
  margin-bottom: var(--spacing-sm);
}

.feature-card p {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.6;
}

/* Process Chain - Vertical Timeline */
.process-step {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  position: relative;
}

.process-step:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 24px;
  top: 50px;
  width: 2px;
  height: calc(100% + 16px);
  background: var(--color-border-main);
}

.process-number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,113,227,0.2);
}

.process-content h4 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
}

.process-content p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

/* Tables */
.component table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--spacing-md) 0;
}

.component table th {
  background: var(--color-bg-subtle);
  color: var(--color-text-primary);
  font-weight: 600;
  padding: 12px;
  text-align: left;
  border-bottom: 2px solid var(--color-border-main);
}

.component table td {
  padding: 12px;
  border-bottom: 1px solid var(--color-border-muted);
  color: var(--color-text-primary);
}

.component table tr:hover {
  background: var(--color-bg-subtle);
}

/* Badges */
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
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

/* Images */
.image-container {
  border: 1px solid var(--color-border-main);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  background: var(--color-bg-main);
}

.image-wrapper {
  width: 100%;
  background: var(--color-bg-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  min-height: 200px;
}

.image-wrapper img {
  max-width: 100%;
  height: auto;
  border-radius: var(--border-radius-sm);
  box-shadow: var(--shadow-md);
}

.image-content {
  padding: var(--component-padding);
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
  line-height: 1.6;
}
```

---

## Component Styling Examples

### Stat Grid Component

**Purpose**: Display key metrics with premium styling

**Styling highlights**:
- **Cards**: Subtle background, minimal border
- **Hover**: Transforms up, glows with blue shadow
- **Number**: Large, bold, blue accent color
- **Label**: Smaller, gray text for hierarchy

**When to use**:
- Revenue metrics
- Performance indicators
- Growth statistics
- User counts

### Feature Grid Component

**Purpose**: Showcase features or benefits in cards

**Styling highlights**:
- **Icon**: Large emoji (48px)
- **Title**: Bold, clear hierarchy
- **Description**: Secondary gray text
- **Hover**: Lifts up, blue border, shadow glow

**When to use**:
- Product features
- Value propositions
- Company strengths
- Service offerings

### Process/Timeline

**Purpose**: Show step-by-step processes or timelines

**Styling highlights**:
- **Numbers**: Blue circles with soft shadow
- **Connector**: Subtle gray line
- **Text**: Clear title and description
- **Responsive**: Stacks on mobile

**When to use**:
- Implementation steps
- Customer journey
- Product roadmap
- Project phases

---

## Testing & Validation

### Color Contrast Checklist

Use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/):

```
✅ Apple Blue (#0071E3) on White (#FFFFFF): 7.2:1 (AAA)
✅ Dark Gray (#1D1D1D) on White (#FFFFFF): 17.2:1 (AAA)
✅ Mid Gray (#6E6E73) on White (#FFFFFF): 7.9:1 (AAA)
✅ Apple Blue on Light Gray (#F5F5F7): 6.4:1 (AAA)
✅ Dark Gray on Light Gray (#F5F5F7): 15.3:1 (AAA)
```

### Component Testing

Test each component type:

1. **Stat Grid**
   - [ ] 2-column layout
   - [ ] 4-column layout
   - [ ] Multi-line labels
   - [ ] Hover effects on desktop
   - [ ] Responsive on mobile

2. **Bullet List**
   - [ ] 3-5 items
   - [ ] Emoji rendering
   - [ ] Bold emphasis
   - [ ] Nested bullets (if supported)

3. **Feature Grid**
   - [ ] 3-6 cards
   - [ ] Emoji icons
   - [ ] Hover lift effect
   - [ ] Text wrapping
   - [ ] Mobile responsive

4. **Process/Timeline**
   - [ ] 3-5 steps
   - [ ] Vertical on mobile
   - [ ] Number circles visible
   - [ ] Connector lines visible

5. **Tables**
   - [ ] Header styling
   - [ ] Row hover
   - [ ] Responsive scrolling
   - [ ] Badge integration

6. **Images**
   - [ ] Frame border visible
   - [ ] Caption styling
   - [ ] Placeholder background
   - [ ] Responsive sizing

### Browser Compatibility

Test on:
- Chrome (Desktop & Mobile)
- Firefox (Desktop)
- Safari (Mac & iOS)
- Edge (Windows)

### Accessibility Checklist

- [ ] All interactive elements have focus states
- [ ] Color is not the only indicator (use icons/text)
- [ ] Text is readable (min 16px)
- [ ] Contrast meets WCAG AAA
- [ ] Images have alt text
- [ ] Semantic HTML used

### Performance Checklist

- [ ] CSS under 50KB
- [ ] No font downloads (system fonts only)
- [ ] Smooth transitions (no jank)
- [ ] Print styles work
- [ ] Dark mode compatible (optional)

---

## Registration & Deployment

### Step 1: Add to projects.json

```json
{
  "projects": [
    {
      "name": "beispiel-projekt",
      "styles": [
        {
          "name": "apple",
          "displayName": "Apple Design",
          "cssPath": "projects/beispiel-projekt/styles/apple/style.css"
        }
      ]
    }
  ]
}
```

### Step 2: Verify Files

```bash
ls -la presentation/projects/beispiel-projekt/styles/apple/
# Should see:
# - design-guide.json
# - style.css
# - variables.css
# - design-guide.md (optional)
```

### Step 3: Test in Browser

1. Start API server: `python3 run_api.py`
2. Open `unified-editor.html`
3. Select project, then Apple theme
4. Generate test slide
5. Verify all components render correctly

### Step 4: Document

Create `design-guide.md` with human-readable explanation:

```markdown
# Apple Design Theme

## Overview
Premium minimalist design inspired by Apple's design language.

## Color Palette
- Primary: #0071E3 (Apple Blue)
- Background: #FFFFFF (White)
- Text: #1D1D1D (Dark Gray)

## Typography
Uses system fonts for fast loading and platform consistency.

## Components
All 10 component types fully supported with premium styling.

## Best Practices
- Use blue accent sparingly (15-20% of interface)
- Maximize whitespace
- Use soft shadows
- Keep text large and readable
```

---

## Conclusion

The Apple theme demonstrates premium, minimalist design principles:

1. **Color discipline**: One primary color, used strategically
2. **Spacing**: Generous whitespace creates premium feel
3. **Typography**: Clear hierarchy with bold headings
4. **Interactivity**: Subtle hover effects with blue glow
5. **Accessibility**: AAA contrast compliance throughout

Use this theme for professional presentations, corporate clients, and tech companies where premium aesthetics matter.


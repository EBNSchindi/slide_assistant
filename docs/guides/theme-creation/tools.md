# Design Tools & Resources Reference

A comprehensive guide to tools, services, and resources for creating professional design themes.

---

## Table of Contents

1. [Color & Contrast Tools](#color--contrast-tools)
2. [Typography & Fonts](#typography--fonts)
3. [Design Inspiration](#design-inspiration)
4. [Accessibility Checkers](#accessibility-checkers)
5. [CSS & Code Tools](#css--code-tools)
6. [Browser DevTools Tips](#browser-devtools-tips)
7. [Design Systems](#design-systems)

---

## Color & Contrast Tools

### WebAIM Contrast Checker (⭐ Essential)

**URL:** https://webaim.org/resources/contrastchecker/

**Purpose:** Validate color contrast ratios for WCAG compliance

**How to use:**
1. Paste foreground color: `#0071E3` (Apple Blue)
2. Paste background color: `#FFFFFF` (White)
3. Check contrast ratio (aim for 4.5:1 minimum)
4. Verify it says "AAA" for triple-A compliance

**Why it matters:**
- WCAG AAA = 7:1 contrast ratio (highest accessibility)
- WCAG AA = 4.5:1 contrast ratio (minimum required)
- WCAG AAA for large text = 3:1 (headings)

**Example Results:**
```
Foreground: #0071E3 (Apple Blue)
Background: #FFFFFF (White)
Contrast: 7.2:1 ✅ WCAG AAA Pass
```

### Coolors.co

**URL:** https://coolors.co/

**Purpose:** Generate color palettes and explore color harmony

**Features:**
- Color palette generator (press spacebar to generate)
- Lock colors you like and regenerate others
- Export palettes as JSON, CSS, or images
- Color harmony modes: monochromatic, analogous, triadic, etc.
- Accessibility simulator (simulates colorblindness)

**Workflow:**
1. Start with primary color: `#10A37F` (OpenAI Teal)
2. Lock that color
3. Generate complementary colors
4. Use accessibility simulator to check visibility
5. Export palette

### Color Picker Tools

#### Browser Built-in
Most modern browsers have color pickers in DevTools:
1. Open DevTools (F12)
2. Go to Elements/Inspector
3. Click color swatch next to color value
4. Adjust with slider or enter hex directly

#### Figma Color Picker
- Download Figma desktop or use web
- Use color picker eyedropper tool
- Convert colors between formats (RGB, HSL, hex)

#### VS Code Color Picker
- Install "Color Picker" extension
- Click hex color to open picker
- Adjust on the fly
- See live changes in browser

### Color Blindness Simulators

**Coblis - Color Blindness Simulator**
- URL: https://www.color-blindness.com/coblis-color-blindness-simulator/
- Upload your color palette image
- See how it looks with different types of color blindness

**Accessible Colors**
- URL: https://accessible-colors.com/
- Enter text and background colors
- See various colorblindness simulations

---

## Typography & Fonts

### Google Fonts (⭐ Popular)

**URL:** https://fonts.google.com/

**Purpose:** Free, high-quality web fonts with wide language support

**Recommended Sans-Serif Fonts:**
- **Inter** - Modern, readable, geometric
  - Used in: Microsoft, Discord, Figma
  - Best for: Contemporary designs
- **Open Sans** - Friendly, highly readable
  - Used in: Kickstarter, Medium
  - Best for: Corporate, professional
- **Poppins** - Rounded, geometric, warm
  - Used in: Slack, Mailchimp
  - Best for: Friendly, approachable brands
- **Roboto** - Neutral, versatile, system-like
  - Used in: Google, Android
  - Best for: Tech companies
- **Public Sans** - Accessible by design
  - Used in: U.S. federal government sites
  - Best for: Accessibility-first designs

**How to use:**
1. Search for font
2. Click font name
3. Select weights/styles (400, 500, 600, 700)
4. Click "Get font"
5. Copy `@import` code to your CSS

**Example:**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --font-family: 'Inter', -apple-system, sans-serif;
}
```

### Font Pair (⭐ Pairing Guide)

**URL:** https://fontpair.co/

**Purpose:** Pre-tested font pairings for headings + body

**How to use:**
1. Browse curated pairs
2. Click pair to see example
3. Get import code for both fonts
4. Copy to your stylesheet

**Pro Tip:** Use system fonts for body text (no downloads), Google Fonts for headings only

### Fonts.com

**URL:** https://www.fonts.com/

**Purpose:** Premium fonts with commercial licenses

**Features:**
- High-quality typefaces
- License management
- Type advisor tool
- Free fonts section

### Monospace Fonts for Code

Recommended monospace families:
- **Monaco** (macOS default)
- **SF Mono** (Apple ecosystem)
- **Consolas** (Windows default)
- **Courier New** (universal fallback)
- **JetBrains Mono** (modern, readable)

**Best fallback stack for monospace:**
```css
ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace
```

---

## Design Inspiration

### Apple Design System

**URL:** https://developer.apple.com/design/human-interface-guidelines/

**Resources:**
- Complete design system
- Color guidelines
- Typography scales
- Component patterns
- Accessibility standards

**What to study:**
- Minimalist color approach
- Typography hierarchy
- Generous whitespace
- Subtle shadows and depth

### OpenAI Design

**URL:** https://openai.com/

**What to observe:**
- Color palette (teal primary)
- Warm grays in typography
- Rounded corner radius
- Card-based layouts
- Animation patterns

### Figma Design Systems

**Open source design systems on Figma:**
1. **Material Design** - Google's design system
2. **Carbon Design** - IBM's design system
3. **Spectrum** - Adobe's design system
4. **Human Interface Guidelines** - Apple's system

**How to access:**
1. Create Figma account
2. Search community files
3. Duplicate design system to your workspace
4. Study structure and components

### Design Inspiration Sites

| Site | Purpose | Best For |
|------|---------|----------|
| [Dribbble](https://dribbble.com/) | Showcase design work | UI/UX inspiration |
| [Behance](https://www.behance.net/) | Portfolio platform | Industry trends |
| [Awwwards](https://www.awwwards.com/) | Web design awards | Web design inspiration |
| [Lapa](https://www.lapa.ninja/) | Landing page inspiration | Layout patterns |
| [Design Observer](https://designobserver.com/) | Design criticism | Thinking & theory |
| [Design Systems Repo](https://designsystemsrepo.com/) | Design system collection | System architecture |

---

## Accessibility Checkers

### WAVE (Web Accessibility Evaluation Tool)

**URL:** https://wave.webaim.org/

**Features:**
- Browser extension
- Highlight accessibility issues
- Color contrast checking
- Form labeling verification
- Keyboard navigation testing

**How to use:**
1. Install browser extension
2. Navigate to your page
3. Click WAVE icon
4. Review errors, warnings, and alerts

### Lighthouse (Google Chrome)

**Built into Chrome DevTools:**
1. Open DevTools (F12)
2. Go to "Lighthouse"
3. Select "Accessibility"
4. Run audit
5. Review issues

**Checks:**
- Color contrast
- Form labels
- Alt text
- ARIA attributes
- Keyboard navigation

### Axe DevTools

**URL:** https://www.deque.com/axe/devtools/

**Purpose:** Comprehensive accessibility testing

**Features:**
- Browser extension
- Automated testing
- Manual testing guidelines
- WCAG standards reference
- Issue severity ratings

### Color Contrast Analyzer

**URL:** https://www.tpgi.com/color-contrast-checker/

**Purpose:** Detailed contrast analysis

**Features:**
- Precise contrast ratio calculation
- Large text vs. normal text WCAG levels
- Color blind simulation
- Gradient contrast checking

---

## CSS & Code Tools

### CSS Variables Generator

**URL:** https://htmlhints.com/css-variables-generator

**Purpose:** Convert design tokens to CSS variables

**Workflow:**
1. Paste design tokens (colors, spacing, etc.)
2. Generate CSS custom properties
3. Copy to variables.css

### CSS Grid Generator

**URL:** https://cssgrid-generator.netlify.app/

**Purpose:** Visually create CSS grid layouts

**Features:**
- Drag to define grid
- See code in real-time
- Export CSS
- Responsive grid options

### Flexbox Playground

**URL:** https://www.flexboxgenerator.com/

**Purpose:** Learn and generate flexbox code

**Helps with:**
- Component alignment
- Responsive row/column layouts
- Spacing between items

### CSS Shadow Generator

**URL:** https://www.cssmatic.com/box-shadow

**Purpose:** Create and copy box-shadow code

**Workflow:**
1. Adjust shadow with sliders
2. Preview on sample element
3. Copy CSS code
4. Use in your variables.css

**Tip:** Generate multiple shadow levels (sm, md, lg, xl)

### Spacing Scale Calculator

**URL:** https://spaceandgrids.com/

**Purpose:** Generate consistent spacing scale

**Recommended scale (8px base):**
```
xs: 4px (1 × 4)
sm: 8px (1 × 8)
md: 16px (2 × 8)
lg: 24px (3 × 8)
xl: 32px (4 × 8)
2xl: 48px (6 × 8)
```

### CSS Autoprefixer

**URL:** https://autoprefixer.github.io/

**Purpose:** Add browser prefixes to CSS

**Workflow:**
1. Paste your CSS
2. Select browser versions
3. Get auto-prefixed output

---

## Browser DevTools Tips

### Chrome/Edge DevTools

**Color Picker (F12 → Elements)**
1. Right-click element
2. Select "Inspect"
3. Find color in CSS
4. Click color swatch
5. Adjust with color picker

**Contrast Ratio Checker**
1. Inspect text element
2. Look for color in CSS
3. Hover over color value
4. DevTools shows contrast ratio
5. Green ✅ = WCAG AA/AAA
6. Yellow ⚠️ = Below AA

**Device Emulation**
1. Press F12
2. Click device icon (top-left)
3. Select device or size
4. Test responsive design
5. Test at multiple breakpoints

**CSS Grid Overlay**
1. Inspect grid container
2. Click grid icon in DevTools
3. See grid lines overlay
4. Debug alignment issues

### Firefox DevTools

**Accessibility Inspector**
1. Press F12
2. Go to "Accessibility" tab
3. Select elements to inspect
4. See contrast ratios and issues

**Responsive Design Mode**
1. Press Ctrl+Shift+M (Windows) or Cmd+Shift+M (Mac)
2. Test at different sizes
3. Simulate different devices

### Safari Web Inspector

**Enable Web Inspector**
1. Preferences → Advanced
2. Check "Show Develop menu"
3. Use Develop → Web Inspector

**Color Contrast**
1. Right-click element
2. "Inspect Element"
3. Check color properties
4. Verify contrast ratios manually

---

## Design Systems

### Material Design

**URL:** https://material.io/design/

**Use for inspiration:**
- Color system architecture
- Spacing and layout rules
- Component patterns
- Motion/animation principles
- Accessibility guidelines

**Key concepts:**
- 12-column grid
- 8px base spacing
- Elevation/shadows
- Material guidelines

### Spectrum (Adobe)

**URL:** https://spectrum.adobe.com/

**Use for inspiration:**
- Design tokens structure
- Component documentation
- Accessibility standards
- Design system documentation style

### Carbon Design (IBM)

**URL:** https://www.carbondesignsystem.com/

**Use for inspiration:**
- Enterprise-grade design
- Accessibility focus
- Icon system
- Component variations

### Polaris (Shopify)

**URL:** https://polaris.shopify.com/

**Use for inspiration:**
- Component-driven design
- Design token system
- Color accessibility
- Design for commerce

---

## Color Palettes by Industry

### Tech Companies

**Apple Blue**: `#0071E3`
- Clean, professional, premium
- Best for: Premium tech brands

**OpenAI Teal**: `#10A37F`
- Warm, approachable, innovative
- Best for: AI/ML companies

**GitHub Green**: `#238636`
- Professional, trusted, open-source
- Best for: Developer tools

**Slack Purple**: `#E01E5A`
- Playful, professional, vibrant
- Best for: Collaboration tools

**Stripe Blue**: `#0066CC`
- Premium, trustworthy, financial
- Best for: Finance/payments

### Financial Services

**Traditional Blue**: `#003DA5`
- Corporate, trustworthy, stable
- Best for: Banks, insurance

**Modern Teal**: `#2DB89E`
- Progressive, modern, fintech
- Best for: Fintech startups

### Healthcare

**Medical Green**: `#2E8B57`
- Calming, trustworthy, health-focused
- Best for: Health platforms

**Accessibility Focus**: High contrast, warm grays

### Consumer/Social

**Instagram Pink**: `#E4405F`
- Vibrant, playful, social
- Best for: Consumer brands

**LinkedIn Blue**: `#0077B5`
- Professional, networking, B2B
- Best for: Business platforms

---

## Quick Reference Checklists

### Before You Start Theme

- [ ] Design inspiration gathered
- [ ] Color palette defined (primary + accents)
- [ ] Contrast ratios tested in WebAIM
- [ ] Font selection made (2-3 max)
- [ ] Spacing scale created (6-8 steps)
- [ ] Shadow levels defined (3-4 levels)
- [ ] Border radius values chosen (2-3 values)

### During Theme Creation

- [ ] All 10 component types styled
- [ ] CSS variables defined in variables.css
- [ ] design-guide.json complete
- [ ] All colors tested for contrast
- [ ] Responsive design at 3 breakpoints
- [ ] Hover/active states defined
- [ ] Transitions/animations smooth

### After Theme Creation

- [ ] Color contrast audit (WebAIM)
- [ ] Accessibility audit (WAVE or Lighthouse)
- [ ] Browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsive testing
- [ ] Performance testing
- [ ] Design system documentation
- [ ] Example slides created

---

## Recommended Free Tools Stack

| Task | Tool | URL |
|------|------|-----|
| **Color Testing** | WebAIM Contrast Checker | webaim.org/resources/contrastchecker/ |
| **Color Palette** | Coolors | coolors.co |
| **Fonts** | Google Fonts | fonts.google.com |
| **Font Pairs** | Font Pair | fontpair.co |
| **Accessibility** | WAVE | wave.webaim.org |
| **DevTools** | Chrome DevTools | Built-in (F12) |
| **CSS Shadows** | CSS Matic | cssmatic.com |
| **Design Inspiration** | Dribbble | dribbble.com |

**Total Cost:** $0 (all free tools)

---

## Time Estimates

| Task | Time | Tool(s) |
|------|------|---------|
| Define color palette | 30-60 min | Coolors, WebAIM |
| Select fonts | 15-30 min | Google Fonts, Font Pair |
| Create CSS variables | 30 min | Text editor, reference docs |
| Style 10 components | 2-3 hours | VS Code, DevTools |
| Test accessibility | 30 min | WAVE, WebAIM, DevTools |
| Browser testing | 30 min | Chrome, Firefox, Safari, Edge |
| Documentation | 30-60 min | Markdown editor |
| **Total** | **5-7 hours** | - |

---

## Advanced Topics

### Color Space Conversions

Convert between formats using tools:

1. **Hex to RGB**: `#0071E3` → `rgb(0, 113, 227)`
2. **RGB to HSL**: `rgb(0, 113, 227)` → `hsl(211, 100%, 45%)`
3. **Use online converter**: https://www.rapidtables.com/convert/color/

### WCAG Contrast Levels

- **AAA** = 7:1 ratio (best accessibility)
- **AA** = 4.5:1 ratio (minimum required)
- **Fail** = <4.5:1 ratio (not accessible)

Always aim for **AAA** when possible.

### CSS Custom Properties (Variables) Best Practices

```css
:root {
  /* Color tokens */
  --color-primary: #0071E3;
  --color-text-primary: #1d1d1d;

  /* Spacing tokens */
  --spacing-md: 16px;

  /* Component defaults */
  --component-padding: var(--spacing-md);
}

.component {
  padding: var(--component-padding);
  color: var(--color-text-primary);
}
```

**Benefits:**
- Single source of truth
- Easy theme switching
- Maintainable code
- Design consistency

---

## Conclusion

Using the right tools makes theme creation:
- Faster (2-3 hours instead of days)
- More accessible (verified contrast ratios)
- More professional (tested on multiple browsers)
- More consistent (design systems as reference)

**Start here:** WebAIM + Coolors + Google Fonts + DevTools = Professional results


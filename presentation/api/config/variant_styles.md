# Component Variant Style Guide

> **Living Document**: This style guide defines the visual variants for HTML slide components. Feel free to edit and adapt these profiles to match your brand requirements.

## Purpose

This guide defines **3 distinct visual variants** for each component type. When generating slides with variants enabled, each component should be rendered in all three profiles, giving users a choice between different visual styles while maintaining consistency within each profile.

---

## Variant Profiles

### Profile 1: Corporate (GitHub-Inspired)

**Character**: Professional, technical, trustworthy
**Primary Color**: `#238636` (GitHub green)
**Use Case**: Enterprise presentations, technical documentation, professional pitches

#### Visual Properties
- **Colors**:
  - Primary: `#238636`
  - Text: `#1f2328`
  - Secondary Text: `#59636e`
  - Borders: `#d1d9e0`
  - Background Accent: `#f6f8fa`
  - Hover Accent: `rgba(35, 134, 54, 0.1)`

- **Typography**:
  - Font Family: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', sans-serif`
  - Weights: 400 (normal), 600 (semibold), 700 (bold)
  - Line Height: 1.5

- **Spacing**:
  - Padding: `48px`
  - Gap: `40px`
  - Component Spacing: `32px`

- **Borders & Effects**:
  - Border Width: `2px`
  - Border Radius: `3px`
  - Shadow: `0 1px 3px rgba(35, 134, 54, 0.12), 0 1px 2px rgba(35, 134, 54, 0.08)`
  - Transition: `all 0.2s ease`

---

### Profile 2: Modern (Blue)

**Character**: Contemporary, dynamic, innovative
**Primary Color**: `#0066cc` (Modern blue)
**Use Case**: Startup presentations, product launches, creative industries

#### Visual Properties
- **Colors**:
  - Primary: `#0066cc`
  - Text: `#1a1a1a`
  - Secondary Text: `#666666`
  - Borders: `#e0e0e0`
  - Background Accent: `#f5f7fa`
  - Hover Accent: `rgba(0, 102, 204, 0.1)`

- **Typography**:
  - Font Family: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif`
  - Weights: 400 (normal), 500 (medium), 700 (bold)
  - Line Height: 1.6

- **Spacing**:
  - Padding: `48px`
  - Gap: `40px`
  - Component Spacing: `36px`

- **Borders & Effects**:
  - Border Width: `1px`
  - Border Radius: `4px`
  - Shadow: `0 2px 8px rgba(0, 102, 204, 0.08), 0 1px 4px rgba(0, 102, 204, 0.04)`
  - Transition: `all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`

---

### Profile 3: Minimal (Gray)

**Character**: Clean, focused, elegant
**Primary Color**: `#666666` (Neutral gray)
**Use Case**: Minimalist presentations, design portfolios, executive summaries

#### Visual Properties
- **Colors**:
  - Primary: `#666666`
  - Text: `#000000`
  - Secondary Text: `#777777`
  - Borders: `#dddddd`
  - Background Accent: `#fafafa`
  - Hover Accent: `rgba(0, 0, 0, 0.05)`

- **Typography**:
  - Font Family: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif`
  - Weights: 300 (light), 400 (normal), 600 (semibold)
  - Line Height: 1.65

- **Spacing**:
  - Padding: `48px`
  - Gap: `40px`
  - Component Spacing: `32px`

- **Borders & Effects**:
  - Border Width: `1px`
  - Border Radius: `2px`
  - Shadow: `none` (minimal uses no shadows)
  - Transition: `all 0.2s ease`

---

## Component-Specific Variations

### 1. Stat Grid Components

#### Corporate Profile
```html
<div class="stat-grid">
  <div class="stat-item" style="border: 2px solid #238636; border-radius: 3px; padding: 32px; background: #f6f8fa;">
    <div class="stat-icon" style="color: #238636; font-size: 2em;">📊</div>
    <div class="stat-value" style="color: #238636; font-size: 3em; font-weight: 700;">42%</div>
    <div class="stat-label" style="color: #59636e; font-size: 0.95em;">Growth Rate</div>
  </div>
</div>
```

#### Modern Profile
```html
<div class="stat-grid">
  <div class="stat-item" style="border: 1px solid #0066cc; border-radius: 4px; padding: 32px; background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);">
    <div class="stat-icon" style="color: #0066cc; font-size: 2.2em;">💹</div>
    <div class="stat-value" style="color: #0066cc; font-size: 3.2em; font-weight: 700;">42%</div>
    <div class="stat-label" style="color: #666666; font-size: 1em;">Growth Rate</div>
  </div>
</div>
```

#### Minimal Profile
```html
<div class="stat-grid">
  <div class="stat-item" style="border-top: 1px solid #dddddd; padding: 32px 0; background: transparent;">
    <div class="stat-value" style="color: #000000; font-size: 3em; font-weight: 300; letter-spacing: -1px;">42%</div>
    <div class="stat-label" style="color: #777777; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px;">Growth Rate</div>
  </div>
</div>
```

**Layout Variations**:
- Corporate: Cards with solid borders, icons on top
- Modern: Cards with gradients, icons with emphasis
- Minimal: Border-top only, no icons, typography-focused

---

### 2. Bullet List Components

#### Corporate Profile
```html
<ul class="bullet-list" style="list-style: none; padding: 0;">
  <li style="border-left: 3px solid #238636; padding-left: 20px; margin-bottom: 16px; background: #f6f8fa; padding: 16px; border-radius: 3px;">
    <strong style="color: #238636;">✓</strong> List item text
  </li>
</ul>
```

#### Modern Profile
```html
<ul class="bullet-list" style="list-style: none; padding: 0;">
  <li style="position: relative; padding-left: 36px; margin-bottom: 20px; line-height: 1.6;">
    <span style="position: absolute; left: 0; color: #0066cc; font-size: 1.2em;">→</span>
    List item text
  </li>
</ul>
```

#### Minimal Profile
```html
<ul class="bullet-list" style="list-style: none; padding: 0;">
  <li style="padding-left: 24px; margin-bottom: 16px; position: relative;">
    <span style="position: absolute; left: 0; color: #666666;">•</span>
    List item text
  </li>
</ul>
```

**Symbol Variations**:
- Corporate: Checkmarks (✓), boxes (□), arrows (→)
- Modern: Arrows (→), chevrons (›), circles (●)
- Minimal: Simple bullets (•), en dashes (–), dots (·)

---

### 3. Quote Components

#### Corporate Profile
```html
<blockquote style="border-left: 4px solid #238636; padding: 24px 32px; background: #f6f8fa; border-radius: 3px; font-style: italic;">
  <p style="font-size: 1.2em; color: #1f2328; margin: 0 0 16px 0;">"Quote text here"</p>
  <footer style="color: #59636e; font-size: 0.9em; font-style: normal;">— Author Name</footer>
</blockquote>
```

#### Modern Profile
```html
<blockquote style="position: relative; padding: 32px 48px; background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); border-radius: 4px;">
  <div style="position: absolute; top: 16px; left: 16px; font-size: 3em; color: #0066cc; opacity: 0.2;">"</div>
  <p style="font-size: 1.3em; color: #1a1a1a; margin: 0 0 16px 0; font-style: italic;">"Quote text here"</p>
  <footer style="color: #666666; font-size: 0.95em;">— Author Name</footer>
</blockquote>
```

#### Minimal Profile
```html
<blockquote style="padding: 24px 0; border-top: 1px solid #dddddd; border-bottom: 1px solid #dddddd;">
  <p style="font-size: 1.15em; color: #000000; margin: 0 0 12px 0; font-weight: 300; line-height: 1.65;">"Quote text here"</p>
  <footer style="color: #777777; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px;">— Author Name</footer>
</blockquote>
```

---

### 4. Table Components

#### Corporate Profile
```html
<table style="width: 100%; border-collapse: collapse; border: 2px solid #238636; border-radius: 3px;">
  <thead>
    <tr style="background: #238636; color: white;">
      <th style="padding: 16px; text-align: left; font-weight: 600;">Header</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #d1d9e0;">
      <td style="padding: 16px;">Data</td>
    </tr>
  </tbody>
</table>
```

#### Modern Profile
```html
<table style="width: 100%; border-collapse: collapse; border: 1px solid #e0e0e0; border-radius: 4px; overflow: hidden;">
  <thead>
    <tr style="background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%); color: white;">
      <th style="padding: 20px; text-align: left; font-weight: 500;">Header</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #e0e0e0; transition: background 0.2s;">
      <td style="padding: 18px;">Data</td>
    </tr>
  </tbody>
</table>
```

#### Minimal Profile
```html
<table style="width: 100%; border-collapse: collapse;">
  <thead>
    <tr style="border-bottom: 2px solid #000000;">
      <th style="padding: 16px 8px; text-align: left; font-weight: 600; text-transform: uppercase; font-size: 0.85em; letter-spacing: 1px;">Header</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #dddddd;">
      <td style="padding: 14px 8px; font-weight: 300;">Data</td>
    </tr>
  </tbody>
</table>
```

---

### 5. Process Chain Components

#### Corporate Profile
- **Layout**: Vertical with connecting lines
- **Style**: Numbered steps with solid borders, shadow boxes
- **Icons**: Checkmarks, arrows, numbered circles
- **Connection**: Thick green line (3px) connecting nodes

#### Modern Profile
- **Layout**: Horizontal with flowing curve connectors
- **Style**: Circular numbered badges, gradient backgrounds
- **Icons**: Arrows, progress indicators, animated elements
- **Connection**: Gradient line with arrow heads

#### Minimal Profile
- **Layout**: Simple vertical list
- **Style**: Numbers only, clean typography
- **Icons**: None or simple dots
- **Connection**: Thin gray line (1px) or no line

---

### 6. Feature Grid Components

#### Corporate Profile
```html
<div class="feature-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 32px;">
  <div class="feature-card" style="border: 2px solid #238636; border-radius: 3px; padding: 32px; background: #f6f8fa;">
    <div class="feature-icon" style="font-size: 2.5em; margin-bottom: 16px;">🎯</div>
    <h3 style="color: #238636; font-size: 1.3em; margin: 0 0 12px 0;">Feature Title</h3>
    <p style="color: #59636e; margin: 0; line-height: 1.5;">Feature description text</p>
  </div>
</div>
```

#### Modern Profile
```html
<div class="feature-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 36px;">
  <div class="feature-card" style="border: 1px solid #e0e0e0; border-radius: 4px; padding: 36px; background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%); transition: transform 0.3s, box-shadow 0.3s;">
    <div class="feature-icon" style="font-size: 3em; margin-bottom: 20px; color: #0066cc;">🚀</div>
    <h3 style="color: #0066cc; font-size: 1.4em; margin: 0 0 16px 0;">Feature Title</h3>
    <p style="color: #666666; margin: 0; line-height: 1.6;">Feature description text</p>
  </div>
</div>
```

#### Minimal Profile
```html
<div class="feature-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px;">
  <div class="feature-card" style="border-top: 1px solid #dddddd; padding-top: 24px;">
    <h3 style="color: #000000; font-size: 1.2em; margin: 0 0 12px 0; font-weight: 600;">Feature Title</h3>
    <p style="color: #777777; margin: 0; line-height: 1.65; font-weight: 300;">Feature description text</p>
  </div>
</div>
```

---

### 7. Image Components

#### Corporate Profile
- **Border**: 2px solid border matching primary color
- **Shadow**: Subtle shadow with green tint
- **Corners**: 3px border radius
- **Caption**: Below image, on gray background

#### Modern Profile
- **Border**: 1px border with gradient effect
- **Shadow**: Larger shadow with blue tint
- **Corners**: 4px border radius
- **Caption**: Overlay on hover with transition

#### Minimal Profile
- **Border**: No border
- **Shadow**: No shadow
- **Corners**: 2px border radius or square
- **Caption**: Simple text below, minimal styling

---

## Agent Generation Instructions

### When Generating Variants

1. **Generate 3 Complete Versions**: For each component, create three complete HTML variations following the profiles above.

2. **Maintain Component Type**: All three variants must be the same component type (e.g., if generating a stat-grid, all three variants are stat-grids with different styling).

3. **Medium Differences**: Variants should differ in:
   - Color schemes (following profile colors)
   - Border styles (width, radius)
   - Typography (weights, sizes)
   - Layout arrangements (icon placement, text alignment)
   - Visual effects (shadows, gradients, transitions)
   - Symbol choices (icons, bullets, decorations)

4. **Consistency Within Profile**: All components in a slide using the same profile should maintain visual consistency.

5. **Accessibility**: All variants must maintain proper contrast ratios and semantic HTML structure.

6. **Responsive Design**: All variants should work responsively using similar grid patterns but styled differently.

### Output Format

When variants are requested, return:
```json
{
  "variants": [
    {
      "profile": "corporate",
      "html": "...",
      "components_used": ["stat-grid", "bullet-list"]
    },
    {
      "profile": "modern",
      "html": "...",
      "components_used": ["stat-grid", "bullet-list"]
    },
    {
      "profile": "minimal",
      "html": "...",
      "components_used": ["stat-grid", "bullet-list"]
    }
  ]
}
```

---

## Customization Notes

**For Users**: Feel free to edit this file to:
- Adjust color values to match your brand
- Change typography preferences
- Modify spacing scales
- Add new variant profiles (Profile 4, 5, etc.)
- Customize component-specific rules

**For Agents**: Always parse the latest version of this file before generating variants. Respect the user's customizations and apply them consistently.

---

## Version History

- **v1.0** (Initial): Three profiles based on beispiel-projekt slides 1-8 analysis (Corporate, Modern, Minimal)

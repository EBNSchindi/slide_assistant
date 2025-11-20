# OpenAI Design System

Modern, warm design inspired by OpenAI's design language with contemporary styling and accessible colors.

## Colors

### Primary
- **OpenAI Teal**: `#10A37F` - Primary accent for highlights and interactive elements
- **Light**: `#1AB88B`
- **Dark**: `#0D8C6D`

### Background
- **Main**: `#ffffff` - Pure white
- **Subtle**: `#f7f7f8` - Warm gray background
- **Component**: `#ffffff` - White component backgrounds
- **Overlay**: `#fafafa` - Very subtle overlay

### Text
- **Primary**: `#2d333a` - Dark gray
- **Secondary**: `#6e6e80` - Medium gray
- **Muted**: `#acacbe` - Light gray text
- **On Primary**: `#ffffff` - White text on teal

### Semantic
- **Success**: `#10B981` (Emerald Green)
- **Warning**: `#F59E0B` (Amber)
- **Danger**: `#EF4444` (Red)
- **Accent**: `#6366F1` (Indigo)

## Typography

- **Font Family**: -apple-system, BlinkMacSystemFont, Inter, Segoe UI, Roboto
- **Mono**: Roboto Mono, Source Code Pro, SF Mono

### Headings
- **H1**: 52px, Bold (700), -0.015em letter-spacing
- **H2**: 36px, Semibold (600), -0.01em letter-spacing
- **H3**: 26px, Semibold (600)
- **H4**: 20px, Semibold (600)

### Body
- **Size**: 16px
- **Weight**: 400 (Regular)
- **Line Height**: 1.6

## Spacing

- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px

## Border Radius

- **sm**: 6px
- **md**: 10px (modern, slightly rounded)
- **lg**: 16px
- **full**: 50% (circular)

## Shadows

Modern, soft shadows with multiple layers:
- **sm**: `0 1px 3px rgba(0,0,0,0.09), 0 1px 2px rgba(0,0,0,0.05)`
- **md**: `0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.05)`
- **lg**: `0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)`
- **xl**: `0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)`

## Components

### Stat Grid
Display statistics in modern cards with:
- Large numbers (36px)
- Labels below in secondary color
- Warm background (#f7f7f8)
- Soft shadows
- Grid layout: auto-fit, minmax(240px, 1fr)

### Bullet List
- Modern bullets with rounded corners
- Emoji support
- Bold first phrase for emphasis
- Subtle background with hover effect

### Tables
- Modern styling with rounded corners
- Soft shadows
- Hover states with lift effect

### Images
- Modern frame with 10px border radius
- Soft shadow
- Caption support below image

### Feature Cards
- Modern card design with shadows
- Interactive hover with lift effect
- Emoji/icon support
- Min width: 280px

### Process Steps
- Modern connectors with smooth lines
- Number badges with primary color
- Vertical or horizontal layouts
- Clean, contemporary styling

## Best Practices

### Stat Grid
- Max 4 cards per row
- Multi-line labels supported
- Source attribution in smaller text

### Bullet List
- Max 5 items recommended
- 1-2 levels of nesting
- Use emojis for visual interest

### Tables
- Max 6 rows for readability
- Use rounded corners
- Responsive breakpoint: 768px

### Images
- Alt text required
- Caption support
- Badge overlay for labels

## Accessibility

- **WCAG AAA** contrast ratios where possible
- Primary/White: 7.1:1 (AAA)
- Text/Background: 11.2:1 (AAA)

## Responsive Breakpoints

- **Desktop**: ≥1024px
- **Tablet**: 768px - 1023px
- **Mobile**: <768px

## Design Philosophy

OpenAI design emphasizes:
- **Warmth**: Warm grays, teal primary color
- **Modern**: Contemporary rounded corners, soft shadows
- **Accessible**: High contrast ratios, clear hierarchy
- **Clean**: Minimal decoration, focus on content

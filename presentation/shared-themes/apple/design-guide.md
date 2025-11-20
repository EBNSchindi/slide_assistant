# Apple Design System

Clean, minimalist design inspired by Apple's design principles with subtle styling and SF Pro typography.

## Colors

### Primary
- **Apple Blue**: `#0071E3` - Primary accent for highlights and interactive elements
- **Light**: `#4DA3FF`
- **Dark**: `#0051B3`

### Background
- **Main**: `#ffffff` - Pure white
- **Subtle**: `#f5f5f7` - Light gray background
- **Component**: `#ffffff` - White component backgrounds
- **Overlay**: `#fafafa` - Very subtle overlay

### Text
- **Primary**: `#1d1d1d` - Almost black
- **Secondary**: `#555555` - Medium gray
- **Muted**: `#888888` - Light gray text
- **On Primary**: `#ffffff` - White text on blue

### Semantic
- **Success**: `#34C759` (Apple Green)
- **Warning**: `#FF9500` (Apple Orange)
- **Danger**: `#FF3B30` (Apple Red)
- **Accent**: `#5E5CE6` (Purple)

## Typography

- **Font Family**: -apple-system, BlinkMacSystemFont, SF Pro Text, SF Pro Display, Helvetica Neue
- **Mono**: SF Mono, Menlo, Monaco, Courier New

### Headings
- **H1**: 56px, Bold (700), -0.02em letter-spacing
- **H2**: 40px, Semibold (600), -0.01em letter-spacing
- **H3**: 28px, Semibold (600)
- **H4**: 20px, Semibold (600)

### Body
- **Size**: 17px (Apple standard)
- **Weight**: 400 (Regular)
- **Line Height**: 1.5

## Spacing

- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px

## Border Radius

- **sm**: 4px (buttons, small elements)
- **md**: 8px (cards, components)
- **lg**: 12px (large components)
- **full**: 50% (circular)

## Shadows

Subtle shadows for depth:
- **sm**: `0 1px 3px rgba(0,0,0,0.07)`
- **md**: `0 2px 8px rgba(0,0,0,0.08)`
- **lg**: `0 4px 12px rgba(0,0,0,0.1)`
- **xl**: `0 8px 24px rgba(0,0,0,0.12)`

## Components

### Stat Grid
Display statistics in clean cards with:
- Large numbers (36px)
- Labels below in secondary color
- Subtle background (#f5f5f7)
- 1px borders
- Grid layout: auto-fit, minmax(220px, 1fr)

### Bullet List
- Clean bullets without heavy borders
- Emoji support
- Bold first phrase for emphasis
- Subtle background on hover

### Tables
- Clean styling with subtle borders
- No heavy lines
- Hover states with subtle background change

### Images
- Subtle frame with 1px border
- 8px border radius
- Caption support below image

### Feature Cards
- Subtle background (#f5f5f7)
- Interactive hover with scale transform
- Emoji/icon support
- Min width: 260px

### Process Steps
- Clean connectors
- No heavy lines
- Number badges with primary color
- Vertical or horizontal layouts

## Best Practices

### Stat Grid
- Max 4 cards per row
- Multi-line labels supported
- Source attribution in smaller text

### Bullet List
- Max 5 items recommended
- 1-2 levels of nesting
- Use emojis sparingly

### Tables
- Max 6 rows for readability
- Use emphasis rows for key metrics
- Responsive breakpoint: 768px

### Images
- Alt text required
- Caption support
- Badge overlay for labels

## Accessibility

- **WCAG AAA** contrast ratios
- Primary/White: 8.2:1
- Text/Background: 14.1:1

## Responsive Breakpoints

- **Desktop**: ≥1024px
- **Tablet**: 768px - 1023px
- **Mobile**: <768px

# Troubleshooting Common Theme Issues

Solutions for common problems when creating and deploying design themes.

---

## Table of Contents

1. [Theme Visibility Issues](#theme-visibility-issues)
2. [CSS Not Loading](#css-not-loading)
3. [Components Look Wrong](#components-look-wrong)
4. [Color & Contrast Problems](#color--contrast-problems)
5. [Layout & Spacing Issues](#layout--spacing-issues)
6. [Responsive Design Issues](#responsive-design-issues)
7. [Performance Issues](#performance-issues)

---

## Theme Visibility Issues

### Problem: Theme doesn't appear in dropdown

**Symptoms:**
- Created theme files but don't see it in the UI theme selector
- Only default themes (github, modern, minimal) appear

**Solution Checklist:**

1. **Check projects.json syntax**
   ```json
   {
     "projects": [
       {
         "name": "beispiel-projekt",
         "styles": [
           {
             "name": "my-theme",
             "displayName": "My Custom Theme",
             "cssPath": "projects/beispiel-projekt/styles/my-theme/style.css",
             "default": false
           }
         ]
       }
     ]
   }
   ```
   - Ensure `cssPath` is correct
   - Check for trailing commas
   - Validate JSON syntax

2. **Verify file structure**
   ```bash
   ls -la presentation/projects/beispiel-projekt/styles/my-theme/
   # Should show:
   # - style.css
   # - variables.css
   # - design-guide.json (optional)
   ```

3. **Clear browser cache**
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
   - Or open DevTools → Right-click refresh → "Empty cache and hard refresh"

4. **Restart API server**
   ```bash
   # Stop current server (Ctrl+C)
   # Then restart:
   python3 run_api.py
   ```

5. **Check for JSON errors**
   - Open projects.json in VS Code
   - Look for red squiggly lines
   - Use JSON formatter: https://jsonformatter.org/

**Quick Validation:**
```bash
# Validate projects.json
python3 -c "import json; json.load(open('presentation/projects.json'))" && echo "✅ Valid JSON"
```

---

### Problem: Wrong theme loads by default

**Symptoms:**
- Selected theme changes but wrong one loads
- Default theme overrides selection

**Solutions:**

1. **Check "default" flag in projects.json**
   ```json
   {
     "name": "my-theme",
     "displayName": "My Custom Theme",
     "cssPath": "...",
     "default": false  // ← Make sure this is false
   }
   ```
   Only ONE theme should have `"default": true`

2. **Check HTML file for hardcoded CSS**
   ```html
   <!-- In ai-editor.html or component-viewer.html -->
   <!-- Should NOT have hardcoded theme CSS -->
   <!-- Remove any direct link tags like: -->
   <!-- <link rel="stylesheet" href="...specific-theme..."> -->
   ```

3. **Check for CSS specificity issues**
   - Use browser DevTools to inspect
   - See which CSS file is being loaded
   - Verify correct file is applied

---

## CSS Not Loading

### Problem: Theme CSS not applying any styles

**Symptoms:**
- Components look completely unstyled
- No colors, spacing, or borders
- Text is black on white with no formatting

**Diagnosis Steps:**

1. **Open browser DevTools (F12)**
   - Go to "Elements" tab
   - Right-click on component
   - Select "Inspect"

2. **Look at Styles panel**
   - Find `.component` class
   - Check what CSS is applied
   - Should see color, padding, border-radius

3. **Check Sources → Network**
   - Go to "Network" tab in DevTools
   - Reload page
   - Look for CSS file download
   - Check if status is "200" (success) or "404" (not found)

**Solution:**

**If CSS file is 404 (not found):**

1. **Check file path in projects.json**
   ```json
   // WRONG:
   "cssPath": "styles/my-theme/style.css"  // Missing "projects/..."

   // CORRECT:
   "cssPath": "projects/beispiel-projekt/styles/my-theme/style.css"
   ```

2. **Check file actually exists**
   ```bash
   ls -la presentation/projects/beispiel-projekt/styles/my-theme/style.css
   # Should return file details, not "No such file"
   ```

3. **Check for typos**
   - `my-theme` not `mytheme` or `my_theme`
   - `style.css` not `styles.css` or `Style.css`
   - Case-sensitive on Linux/Mac!

**If CSS file loads but styles don't apply:**

1. **Check CSS Selector Specificity**
   ```css
   /* Too generic - might be overridden */
   p { color: blue; }

   /* Better - more specific */
   .component p { color: blue; }

   /* Best - most specific */
   .component p, .bullet-list li { color: blue; }
   ```

2. **Check for !important usage**
   - Other CSS might be using `!important`
   - Override with: `color: blue !important;`
   - Use sparingly!

3. **Check @import order**
   ```css
   /* In style.css, put imports FIRST */
   @import url('variables.css');
   /* Then put your CSS below */
   ```

4. **Validate CSS syntax**
   - Use CSS validator: https://jigsaw.w3.org/css-validator/
   - Look for syntax errors
   - Check for missing semicolons

---

### Problem: Only some components are styled

**Symptoms:**
- Stat grid looks good, but bullets don't work
- Some components have colors, others don't
- Partial styling applied

**Solution:**

1. **Check CSS class names match components**
   ```css
   /* Make sure all 10 component types have CSS: */
   .stat-grid { ... }      /* ✅ */
   .bullet-list { ... }    /* ✅ */
   .quote { ... }          /* ✅ */
   .text-block { ... }     /* ✅ */
   .table { ... }          /* ✅ */
   .image-container { ... }    /* ✅ */
   .image-grid { ... }     /* ✅ */
   .feature-grid { ... }   /* ✅ */
   .process-chain { ... }  /* ✅ */
   .process-horizontal { } /* ✅ */
   ```

2. **Verify component HTML has correct classes**
   - Open rendered HTML in DevTools
   - Check that classes match CSS selector names
   - Example: `<div class="component stat-grid">` should match `.component.stat-grid` CSS

3. **Check for typos in class names**
   ```css
   /* WRONG: typo in name */
   .stat-grid { ... }
   .stat-card { ... }

   /* Component uses: <div class="stat-card"> */
   /* But CSS is: .stat-gird {} */  /* ← Typo! */
   ```

---

## Components Look Wrong

### Problem: Components are unstyled or broken layout

**Symptoms:**
- Components stack vertically instead of grid
- Text is too large or too small
- Spacing is wrong
- Colors are missing

**Solution:**

1. **Check CSS variables are defined**
   ```css
   /* In variables.css */
   :root {
     --color-primary: #0071E3;
     --spacing-md: 16px;
     --border-radius-md: 8px;
   }

   /* In component CSS, use variables */
   .component {
     padding: var(--spacing-md);  /* ✅ Uses variable */
     color: var(--color-primary); /* ✅ Uses variable */
   }
   ```

2. **Check @import is correct**
   ```css
   /* style.css MUST import variables first */
   @import url('variables.css');

   /* Then use variables */
   .component {
     color: var(--color-primary);
   }
   ```

3. **Check grid column definition**
   ```css
   /* WRONG: */
   .stat-grid {
     display: grid;
     grid-template-columns: 1fr 1fr;  /* ← Fixed 2 columns */
   }

   /* CORRECT: */
   .stat-grid {
     display: grid;
     grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
     /* ↑ Responsive, automatically adjusts */
   }
   ```

4. **Test in browser DevTools**
   ```
   1. Press F12
   2. Go to Elements tab
   3. Inspect .stat-grid element
   4. Look at "Layout" section
   5. See if grid is displayed correctly
   6. Check grid-template-columns value
   ```

### Problem: Stat numbers are wrong color

**Symptoms:**
- Numbers should be primary color (#0071E3) but are black
- Or numbers are using wrong color variable

**Solution:**

1. **Check `.stat-number` CSS**
   ```css
   .stat-number {
     color: var(--color-primary);  /* ✅ Correct */
   }

   /* NOT: */
   .stat-number {
     color: var(--color-text-primary);  /* ✗ Wrong variable */
   }
   ```

2. **Verify variable value**
   ```css
   :root {
     --color-primary: #0071E3;  /* Apple Blue */
     --color-text-primary: #1D1D1D;  /* Dark gray */
   }

   /* For stat numbers, use --color-primary, not --color-text-primary */
   ```

3. **Check for CSS specificity override**
   - More specific CSS might be overriding
   - Use DevTools Styles tab to see what's applied
   - May need to increase specificity

---

### Problem: Buttons/links not styled

**Symptoms:**
- Interactive elements don't have primary color
- Hover effects don't work
- Links look like plain text

**Solution:**

1. **Check button/link CSS**
   ```css
   button, a.btn {
     background: var(--color-primary);
     color: white;
     padding: 8px 16px;
     border-radius: var(--border-radius-md);
     cursor: pointer;
     transition: all 0.2s;
   }

   button:hover, a.btn:hover {
     background: var(--color-primary-light);
     transform: scale(1.02);
   }
   ```

2. **Check HTML uses correct class**
   ```html
   <!-- Use .btn class for styled buttons -->
   <button class="btn">Click me</button>
   <a href="#" class="btn">Link button</a>

   <!-- NOT: -->
   <button>Unstyled</button>
   ```

---

## Color & Contrast Problems

### Problem: Color contrast fails WCAG standards

**Symptoms:**
- WebAIM says contrast is below 4.5:1
- Text is hard to read on background
- Gets accessibility warnings

**Solution:**

1. **Test with WebAIM Contrast Checker**
   - https://webaim.org/resources/contrastchecker/
   - Enter text color and background color
   - Check contrast ratio

2. **If contrast is too low:**

   **Option A: Darken text**
   ```css
   /* WRONG: Gray text on white (low contrast) */
   --color-text: #A9A9B0;  /* 5.4:1 */

   /* BETTER: Darker gray (higher contrast) */
   --color-text: #6E6E73;  /* 8.2:1 AAA */
   ```

   **Option B: Lighten background**
   ```css
   /* WRONG: Light text on light background */
   --color-bg: #F5F5F7;
   --color-text: #CCCCCC;  /* Low contrast */

   /* BETTER: Adjust one or both */
   --color-bg: #FFFFFF;     /* Lighter background */
   --color-text: #666666;   /* Darker text */
   ```

   **Option C: Change primary color**
   ```css
   /* If your primary color has poor contrast on white: */
   --color-primary: #FF9500;  /* Orange: 4.6:1 (AA minimum) */

   /* Consider using darker variant: */
   --color-primary: #E67E00;  /* Darker orange: 5.2:1 (AA+) */
   ```

3. **Create variant colors for different backgrounds**
   ```css
   :root {
     /* For white/light backgrounds */
     --color-primary-on-white: #0071E3;  /* 7.2:1 AAA */

     /* For colored backgrounds */
     --color-primary-on-colored: #FFFFFF;  /* On blue */
   }

   .component {
     color: var(--color-primary-on-white);
   }

   .component.dark-bg {
     color: var(--color-primary-on-colored);
   }
   ```

### Problem: Color looks different in different lighting

**Symptoms:**
- Color looks good on monitor but different when printed
- Monitor brightness affects how color looks

**Solution:**

1. **Test on multiple monitors**
   - Desktop monitor
   - Laptop screen
   - Mobile phone
   - Print preview

2. **Use neutral lighting**
   - Bright room (not dim)
   - Avoid side-lighting on screen
   - Use color checker tool

3. **Test with color blind simulator**
   - https://www.color-blindness.com/coblis-color-blindness-simulator/
   - Upload color palette
   - Ensure it's readable for colorblind users

---

## Layout & Spacing Issues

### Problem: Components are too cramped or too spaced out

**Symptoms:**
- Text is too close together
- Too much white space between elements
- Layout looks unbalanced

**Solution:**

1. **Check spacing scale**
   ```css
   :root {
     --spacing-xs: 4px;   /* Too small */
     --spacing-sm: 8px;   /* Small */
     --spacing-md: 16px;  /* Medium (use most) */
     --spacing-lg: 24px;  /* Large */
     --spacing-xl: 32px;  /* Extra large */
   }
   ```

2. **Adjust spacing consistently**
   ```css
   /* WRONG: Random spacing */
   .component { padding: 12px; }
   .stat-card { padding: 18px; }
   .feature-card { padding: 25px; }

   /* CORRECT: Use spacing scale */
   .component { padding: var(--spacing-md); }  /* 16px */
   .stat-card { padding: var(--spacing-lg); }  /* 24px */
   .feature-card { padding: var(--spacing-lg); } /* 24px */
   ```

3. **Check line-height for readability**
   ```css
   /* WRONG: Too tight */
   .component p { line-height: 1.3; }

   /* CORRECT: Comfortable reading */
   .component p { line-height: 1.6; }

   /* EXTRA SPACE: For important text */
   .component p { line-height: 1.8; }
   ```

4. **Check margins between sections**
   ```css
   .component {
     margin-bottom: var(--spacing-lg);  /* Space after component */
   }

   .component + .component {
     margin-top: var(--spacing-lg);  /* Space between components */
   }
   ```

---

### Problem: Text is too large or too small

**Symptoms:**
- Headings huge or tiny
- Body text hard to read
- Inconsistent font sizes

**Solution:**

1. **Check design-guide.json font sizes**
   ```json
   {
     "tokens": {
       "typography": {
         "headings": {
           "h1": {"fontSize": "48px"},  // Headline
           "h2": {"fontSize": "32px"},  // Subheading
           "h3": {"fontSize": "24px"},  // Section
           "h4": {"fontSize": "20px"}   // Subsection
         },
         "body": {
           "fontSize": "16px"           // Body text (16px minimum)
         }
       }
     }
   }
   ```

2. **Check CSS matches design-guide**
   ```css
   .component h1 { font-size: 48px; }  /* Match design-guide */
   .component h2 { font-size: 32px; }
   .component h3 { font-size: 24px; }
   .component h4 { font-size: 20px; }
   .component p { font-size: 16px; }  /* Minimum 16px for readability */
   ```

3. **Use relative sizing for responsiveness**
   ```css
   /* Desktop */
   .component h1 { font-size: 48px; }

   /* Tablet */
   @media (max-width: 1024px) {
     .component h1 { font-size: 40px; }
   }

   /* Mobile */
   @media (max-width: 768px) {
     .component h1 { font-size: 32px; }
   }
   ```

---

## Responsive Design Issues

### Problem: Components don't stack on mobile

**Symptoms:**
- Grid layout doesn't reflow on small screens
- Horizontal scroll needed on mobile
- Components overflow screen width

**Solution:**

1. **Check responsive grid**
   ```css
   /* WRONG: Fixed columns */
   .stat-grid {
     grid-template-columns: 1fr 1fr 1fr 1fr;
   }

   /* CORRECT: Responsive */
   .stat-grid {
     grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
   }
   /* ↑ Automatically stacks on mobile */
   ```

2. **Add media queries for small screens**
   ```css
   @media (max-width: 768px) {
     .stat-grid {
       grid-template-columns: 1fr;  /* Stack vertically */
       gap: 12px;  /* Reduce gap on mobile */
     }

     .component {
       padding: 16px;  /* Reduce padding on mobile */
     }
   }
   ```

3. **Test on actual mobile device**
   ```bash
   # Chrome DevTools Device Mode
   F12 → Click device icon → Select device

   # Or test on real phone:
   # 1. Run local server: python3 -m http.server 8000
   # 2. Get your IP: ipconfig getifaddr en0 (Mac)
   # 3. Visit: http://YOUR_IP:8000/page.html
   ```

### Problem: Text is too large on mobile

**Symptoms:**
- Font sizes are huge on phone
- Text overflows container
- Can't fit on screen

**Solution:**

```css
/* Mobile first approach */
.component h1 {
  font-size: 24px;  /* Mobile size */
}

/* Larger on desktop */
@media (min-width: 768px) {
  .component h1 {
    font-size: 48px;  /* Desktop size */
  }
}
```

### Problem: Images don't fit on mobile

**Symptoms:**
- Images overflow screen
- Horizontal scroll on mobile
- Images cut off

**Solution:**

```css
.image-wrapper img {
  max-width: 100%;      /* Never wider than container */
  height: auto;         /* Maintain aspect ratio */
  width: auto;          /* Let browser calculate */
  display: block;       /* Inline images add extra space */
}
```

---

## Performance Issues

### Problem: CSS file is too large

**Symptoms:**
- Load time is slow
- Network tab shows CSS > 100KB
- Page feels sluggish

**Solution:**

1. **Check file size**
   ```bash
   ls -lh presentation/projects/beispiel-projekt/styles/my-theme/style.css
   # Size should be < 50KB
   ```

2. **Remove unused CSS**
   - Check for duplicate rules
   - Remove commented-out code
   - Delete unused component styles

3. **Minify CSS**
   ```bash
   # Use CSS minifier: https://cssminifier.com/
   # Or build tool: PostCSS, Sass, etc.
   ```

4. **Use CSS variables to reduce duplication**
   ```css
   /* WRONG: Repeat values */
   .component { color: #0071E3; }
   .button { color: #0071E3; }
   .link { color: #0071E3; }

   /* CORRECT: Use variables */
   :root { --color-primary: #0071E3; }
   .component { color: var(--color-primary); }
   .button { color: var(--color-primary); }
   .link { color: var(--color-primary); }
   ```

### Problem: Animations are jerky (not 60fps)

**Symptoms:**
- Hover effects feel sluggish
- Transitions are not smooth
- Browser lags when hovering

**Solution:**

1. **Use hardware-accelerated properties**
   ```css
   /* BAD: Layout thrashing */
   .feature-card:hover {
     width: 110%;  /* ✗ Recalculates layout */
     height: 110%; /* ✗ Recalculates layout */
   }

   /* GOOD: GPU accelerated */
   .feature-card:hover {
     transform: scale(1.1);  /* ✅ No layout recalc */
     box-shadow: 0 8px 16px rgba(0,0,0,0.1);
   }
   ```

2. **Reduce shadow complexity**
   ```css
   /* WRONG: Complex shadow */
   box-shadow: 0 0 10px rgba(0,0,0,0.2),
               0 4px 8px rgba(0,0,0,0.1),
               0 2px 4px rgba(0,0,0,0.05);

   /* BETTER: Simple shadow */
   box-shadow: 0 4px 12px rgba(0,0,0,0.1);
   ```

3. **Use appropriate transition duration**
   ```css
   /* WRONG: Too slow */
   transition: all 1s linear;

   /* CORRECT: 150-300ms */
   transition: all 200ms ease-out;

   /* Different speeds for different properties */
   transition: background 150ms, transform 200ms, box-shadow 200ms;
   ```

---

## Quick Debugging Checklist

### When theme doesn't work:

- [ ] Check projects.json for syntax errors
- [ ] Verify CSS file path is correct
- [ ] Hard refresh browser (Ctrl+Shift+R)
- [ ] Open DevTools → Network tab
- [ ] Check CSS file loads (status 200, not 404)
- [ ] Inspect component, check applied styles
- [ ] Verify CSS variables are defined
- [ ] Check @import for variables.css
- [ ] Restart API server
- [ ] Test on different browser

### When components look wrong:

- [ ] Check all 10 component types have CSS
- [ ] Verify class names match selectors
- [ ] Check CSS variables are in variables.css
- [ ] Verify @import url('variables.css') is first
- [ ] Test in Chrome DevTools Device Mode
- [ ] Check for typos in class names
- [ ] Verify color contrast with WebAIM

### When styles aren't applying:

- [ ] Check CSS specificity
- [ ] Look for !important overrides
- [ ] Verify selector syntax
- [ ] Check for typos in property names
- [ ] Use browser DevTools Styles tab
- [ ] Try adding !important temporarily (for debugging)
- [ ] Clear browser cache

---

## Getting Help

### If you're still stuck:

1. **Check the examples**
   - Read apple-walkthrough.md
   - Read openai-walkthrough.md
   - Copy their CSS structure

2. **Use browser DevTools**
   - F12 → Elements → Inspect
   - Look at Styles panel
   - See what CSS is applied
   - See what's overriding it

3. **Validate your files**
   - https://jsonformatter.org/ (projects.json)
   - https://jigsaw.w3.org/css-validator/ (CSS)
   - Markdown linter for docs

4. **Test with sample data**
   - Generate simple test slide
   - Use theme on it
   - See if it works
   - Then test with real content


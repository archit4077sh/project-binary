"""
snippets/q_css.py — BATCH 3: 28 brand-new CSS/Styling questions
Zero overlap with batch1 or batch2 archives.
"""

Q_CSS = [

"""**Task (Code Generation):**
Implement a pure CSS animated gradient border that works without JavaScript:

```css
.gradient-border {
  --gradient: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899, #6366f1);
  background-size: 200% auto;
  animation: borderSpin 3s linear infinite;
}
```

Show: using `background-clip: padding-box` and `border: 2px solid transparent` to create a transparent border that reveals an animated gradient background layer, the `::before` pseudo-element technique as an alternative, `@property` for animating gradient positions in Chrome, and accessibility considerations for users with `prefers-reduced-motion`.""",

"""**Debug Scenario:**
A Next.js app with CSS Modules generates class names like `_heading_1a2b3c` in development but `_1a2b3c` in production (the class name is truncated). Some CSS specificity conflicts arise because two unrelated components generate the same truncated hash.

Show: configuring `localIdentName` in the CSS Modules Webpack config to include `[name]` in production builds, the Next.js `experimental.cssModulesClassNamePrefix` option, and how to audit for CSS class name collisions using PostCSS plugins. Explain the tradeoff between shorter class names (smaller CSS bundle) and collision risk.""",

"""**Task (Code Generation):**
Build a container-aware responsive layout system using CSS Container Queries:

```css
.card-grid {
  container-type: inline-size;
  container-name: card-grid;
}

@container card-grid (min-width: 600px) {
  .card { display: flex; }
}

@container card-grid (min-width: 900px) {
  .card { grid-template-columns: 2fr 1fr; }
}
```

Show: the difference between `container-type: inline-size` vs `size`, `container-name` for nesting multiple containers, `@container style()` queries for styling based on custom properties, browser support detection with `@supports (container-type: inline-size)`, and a JavaScript polyfill setup for older browsers.""",

"""**Debug Scenario:**
A dashboard component uses CSS Grid with `auto-rows: minmax(200px, auto)`. On Firefox, rows expand beyond 200px as expected when content overflows. On Chrome, rows are exactly 200px and content overflows out of the grid cell.

Investigation reveals Chrome interprets `minmax(200px, auto)` differently for items with `overflow: hidden`. Show the exact CSS behavior difference, the fix (`min-height: 0` on the grid item), and how `grid-template-rows: masonry` (experimental) interacts with `minmax`.""",

"""**Task (Code Generation):**
Implement a fully keyboard-navigable CSS-only dropdown navigation menu:

```html
<nav>
  <ul>
    <li>
      <a href="/products">Products</a>
      <ul class="dropdown">
        <li><a href="/products/web">Web Apps</a></li>
        <li><a href="/products/mobile">Mobile</a></li>
      </ul>
    </li>
  </ul>
</nav>
```

Show: `:focus-within` to show dropdown when any child has focus, CSS transitions for smooth open/close, `visibility: hidden` vs `display: none` for accessibility (screen readers can still discover `visibility: hidden` content when parent is `:focus-within`), and `tabindex="-1"` management for proper tab order.""",

"""**Debug Scenario:**
A CSS `transition` on `height: auto` doesn't animate — the box snaps from height 0 to the full height instantly.

```css
.accordion-content {
  height: 0;
  overflow: hidden;
  transition: height 0.3s ease;
}
.accordion-content.open {
  height: auto; /* Doesn't animate */
}
```

CSS can't interpolate between `0` and `auto`. Show four solutions: (1) `max-height` hack (risk: clipping), (2) `grid-template-rows: 0fr → 1fr` (Chrome 107+ only, animates grid tracks), (3) JavaScript `scrollHeight` measurement with inline style, (4) the new `interpolate-size: allow-keywords; height: auto` experimental CSS property.""",

"""**Task (Code Generation):**
Implement a design system's spacing scale using CSS `calc()` and `var()` with a mathematical baseline:

```css
:root {
  --space-unit: 4px;
  --space-1: calc(var(--space-unit) * 1);   /* 4px */
  --space-2: calc(var(--space-unit) * 2);   /* 8px */
  --space-4: calc(var(--space-unit) * 4);   /* 16px */
  --space-8: calc(var(--space-unit) * 8);   /* 32px */
  --space-16: calc(var(--space-unit) * 16); /* 64px */
}
```

Show: the complete 12-step scale, a `@layer` setup for the token definitions, a Sass/PostCSS build step that generates the scale from a single `$space-unit` variable, and `env()` CSS function for accessing system-level spacing (iOS safe areas, etc.).""",

"""**Debug Scenario:**
A popup overlay uses `backdrop-filter: blur(8px)` for a frosted glass effect. The blur works on Chrome and Safari but has no effect on Firefox.

```css
.overlay {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  background: rgba(255, 255, 255, 0.5);
}
```

Firefox supports `backdrop-filter` from v103+ but requires enabling it. Show: `@supports (backdrop-filter: blur(8px))` for feature detection, a solid semi-transparent background as the fallback, and the progressive enhancement strategy where the blur is an enhancement (not required for usability). Also show `isolation: isolate` requirement for the blur to work correctly on stacking contexts.""",

"""**Task (Code Generation):**
Build a CSS-only tabbed interface using `:has()` (no JavaScript):

```html
<div class="tabs">
  <input type="radio" name="tab" id="tab1" checked>
  <input type="radio" name="tab" id="tab2">
  <label for="tab1">Tab 1</label>
  <label for="tab2">Tab 2</label>
  <div class="panel" id="panel1">Content 1</div>
  <div class="panel" id="panel2">Content 2</div>
</div>
```

Using `:has()`:
```css
.tabs:has(#tab2:checked) #panel2 { display: block; }
.tabs:has(#tab1:checked) #panel1 { display: block; }
```

Show: the complete CSS tabs using `:has()`, the checkbox hack fallback for browsers without `:has()` support, and the accessibility implications (screen reader behavior, ARIA-less tabpanel navigation).""",

"""**Debug Scenario:**
A table component has `position: sticky` on column headers AND sticky first column, but the first-column sticky cells don't appear above other cells when scrolling horizontally — they appear behind them.

```css
th:first-child { position: sticky; left: 0; z-index: 2; }
thead th { position: sticky; top: 0; z-index: 2; }
thead th:first-child { z-index: 3; } /* Should be on top */
```

The `z-index: 3` on the corner cell doesn't work because sticky cells create their own stacking context within the table. Show: using `z-index` within the table stacking context hierarchy, the specific CSS fix for table-layout sticky cells, and an alternative JavaScript-based sticky solution using `IntersectionObserver` that avoids the z-index issue entirely.""",

"""**Task (Code Generation):**
Implement a CSS `@layer` architecture for a design system that prevents specificity wars:

```
@layer reset, tokens, base, components, patterns, utilities, overrides;
```

Map each layer to a responsibility:
- `reset`: normalize.css / modern-normalize
- `tokens`: CSS custom property definitions
- `base`: element defaults (h1, p, a)
- `components`: BEM component styles
- `utilities`: single-purpose utility classes
- `overrides`: context-specific overrides

Show: how to import third-party styles into specific layers, `@layer` with separate files using `@import "file.css" layer(reset)`, and why a utility class in `utilities` layer always beats a component style in `components` regardless of selector specificity.""",

"""**Debug Scenario:**
A `position: absolute` element inside a `transform: rotate(45deg)` parent is being positioned incorrectly. The developer expects the absolute child to be positioned relative to the `<body>`, but it's positioned relative to the rotated parent.

```css
.parent { transform: rotate(45deg); position: relative; }
.child { position: absolute; top: 0; left: 0; } /* positioned relative to .parent */
```

CSS transforms create a new containing block for absolutely positioned descendants. Show: this interaction between `transform` and position (containing blocks), how `will-change: transform` has the same effect even without an active transform value, and workarounds (render child in a portal or using fixed positioning with JavaScript coordinates).""",

"""**Task (Code Generation):**
Build a CSS-only carousel/slider with infinite looping and snap points:

```css
.carousel {
  display: flex;
  overflow-x: scroll;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}
.slide {
  scroll-snap-align: start;
  flex: 0 0 100%;
}
```

Show: CSS `scroll-snap-align: center` for centered snapping vs `start`, using `scroll-padding` for offset snapping (accounting for sticky headers), infinite loop using JS + `scrollTo` (pure CSS can't infinite loop), and `scrollend` event (new 2023) for detecting when snap animation completes versus `scroll` event throttling.""",

"""**Debug Scenario:**
A CSS animation using `perspective` for a 3D card flip effect looks different on different monitors. On monitors with high-resolution (4K), the perspective appears smaller (the 3D effect is less dramatic). On 1080p monitors it looks right.

`perspective: 800px` is a fixed pixel value. On 4K displays, 800px is proportionally smaller relative to the element's visual size (due to device pixel ratio). Show: using `perspective: 80vw` for viewport-relative perspective, or calculating perspective relative to the element's own size using `perspective: 500%`, and the `perspective-origin` property for the vanishing point.""",

"""**Task (Code Generation):**
Implement a complete CSS theming system using `@layer` and custom properties for a SaaS product with white-labeling:

```css
@layer tokens {
  :root {
    /* Default theme */
    --brand-primary: #6366f1;
    --brand-secondary: #8b5cf6;
  }
  
  [data-brand="acme"] {
    --brand-primary: #dc2626;
    --brand-secondary: #ea580c;
  }
}
```

Show: the token hierarchy (brand → semantic → component), how white-label themes are applied via `data-brand` attribute set in middleware, runtime theme switching without flash, and a TypeScript `getThemeVar(key: keyof ThemeTokens)` function that provides autocomplete for CSS variable names.""",

"""**Debug Scenario:**
A multi-column form layout uses CSS Grid with `grid-template-areas`. On a narrow screen, the form should switch to a single column. But on narrow screens, some fields overlap each other instead of wrapping:

```css
.form {
  display: grid;
  grid-template-areas:
    "name email"
    "phone address";
  grid-template-columns: 1fr 1fr;
}
@media (max-width: 600px) {
  .form { grid-template-areas: "name" "email" "phone" "address"; } /* forgot to reset columns */
}
```

The responsive fix forgets to reset `grid-template-columns`. Show: the complete responsive grid fix, `grid-template` shorthand that sets both areas AND columns in one declaration, and using `auto-fit`/`auto-fill` as an alternative to eliminate the need for media queries entirely.""",

"""**Task (Code Generation):**
Implement a CSS color system using `oklch()` color space for perceptually uniform colors:

```css
:root {
  /* Primary color scale in oklch: */
  --primary-50:  oklch(97% 0.015 265);  /* near-white */
  --primary-500: oklch(60% 0.2 265);    /* brand color */
  --primary-900: oklch(25% 0.1 265);    /* near-black */
}
```

Show: the `oklch(lightness chroma hue)` syntax, why `oklch` produces more perceptually uniform scales than `hsl` (equal lightness steps look equal to human eyes), a Sass/PostCSS function that generates a full 10-step scale from a single base color, and the `color-mix(in oklch, ...)` function for creating tints/shades.""",

"""**Debug Scenario:**
A card component has a `:hover` state that changes `box-shadow` and scales the card up. The transition fires correctly on hover-in but the shadow doesn't transition on hover-out — it snaps back instantly.

```css
.card {
  transition: transform 0.2s ease;
  /* Missing: box-shadow not in transition list */
}
.card:hover {
  transform: scale(1.02);
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}
```

The `transition` property only applies to `transform`. Show: adding `box-shadow` to the transition list, the `transition: all 0.2s` shorthand (with performance warning — `all` can trigger unnecessary transitions on inherited properties), and a CSS custom property approach that transitions the shadow opacity instead of the shadow value itself (for better performance).""",

"""**Task (Code Generation):**
Build a CSS-only star rating component that works without JavaScript:

```html
<div class="star-rating">
  <input type="radio" name="rating" id="star5" value="5">
  <label for="star5">★</label>
  <!-- 4, 3, 2, 1 stars (in reverse DOM order) -->
</div>
```

Show: the reverse-order input trick (CSS can only select subsequent siblings, so stars are in reverse DOM order), `:has()` as the modern alternative without reverse ordering, making stars fill based on hover and selection using `~` sibling combinator, and the accessibility version with proper ARIA `role="radiogroup"` and `aria-label`.""",

"""**Debug Scenario:**
A responsive navigation bar uses CSS Grid. The logo is in the left, navigation in the center, and CTA button on the right. On mobile, the layout collapses but the center element (nav links) overflows instead of hiding.

```css
.navbar { display: grid; grid-template-columns: auto 1fr auto; }
```

The `1fr` column expands to fill space but the nav links inside don't wrap or hide when the viewport is too narrow. Show: `min-width: 0` on the `1fr` column to prevent expansion, `overflow: hidden` + `text-overflow: ellipsis` for graceful overflow, the mobile pattern using `@media` to switch to a Column Grid for the hamburger menu, and `@container` queries for component-level responsiveness.""",

"""**Task (Code Generation):**
Implement a complete dark mode system using CSS custom properties with NO JavaScript flash:

```html
<!-- In <head>, before CSS loads: -->
<script>
  // Synchronously read preference before first paint:
  document.documentElement.dataset.theme = 
    localStorage.theme ?? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
</script>
```

Show: the inline script placement (must be first in `<head>`, before `<link rel="stylesheet">`), the CSS custom property definitions for both themes, why this beats `@media (prefers-color-scheme)` alone (user override capability), and integrating with Next.js's `<Script strategy="beforeInteractive">` for the App Router.""",

"""**Debug Scenario:**
A CSS Grid layout has `grid-template-columns: repeat(3, 1fr)`. When an item uses `grid-column: span 2`, the next item wraps to the next row, leaving a visual gap in the grid.

```css
.grid { display: grid; grid-template-columns: repeat(3, 1fr); }
.wide { grid-column: span 2; }
/* Gap visible to the right of .wide item */
```

CSS Grid places items sequentially and won't backfill gaps by default. Show: `grid-auto-flow: dense` to enable packing (fills gaps with smaller items), why `dense` changes the visual order (may not match DOM order, hurting accessibility), and the explicit placement alternative that avoids gaps without `dense`.""",

"""**Task (Code Generation):**
Build a CSS animation system for page transitions in a Next.js App Router application:

```css
/* Entry/exit animations per route: */
@keyframes slideInFromRight  { from { transform: translateX(100%); opacity: 0; } }
@keyframes slideOutToLeft    { from { transform: translateX(0); opacity: 1; } to { transform: translateX(-100%); opacity: 0; } }
```

Show: the `View Transition API` for browser-native page transitions (`document.startViewTransition()`), Next.js App Router integration using `router.push` wrapped in `startViewTransition`, `::view-transition-old(root)` and `::view-transition-new(root)` CSS targets, and the `@supports` fallback for browsers without View Transition API support.""",

"""**Debug Scenario:**
A CSS-in-JS library (`emotion`) generates class names that interfere with a user-installed browser extension that injects its own CSS. The extension targets `.emotion-class` patterns and accidentally overrides button styles.

Show: using a custom class name prefix in Emotion config (`@emotion/cache` with `key` option), scoping all component styles with a unique container class (`[data-app="my-app"] .button { ... }`), and the `important: true` option in `StylesProvider` (MUI) to ensure styled component styles take precedence. Explain the ethical and UX considerations of using `!important` at scale.""",

"""**Task (Code Generation):**
Implement a `@theme` block using the new CSS `@scope` rule for scoped component theming:

```css
@scope (.card-primary) {
  :scope { background: var(--color-primary-light); }
  .card-title { color: var(--color-primary-dark); }
  .card-cta { background: var(--color-primary); color: white; }
}

@scope (.card-ghost) {
  :scope { background: transparent; border: 1px solid currentColor; }
}
```

Show: `@scope` basic syntax, the scoping limit (lower boundary of scope), how `@scope` prevents style leakage into nested components, browser support and the PostCSS `@csstools/postcss-scope-selector` polyfill, and comparison with CSS Modules and Shadow DOM for style isolation.""",

"""**Debug Scenario:**
A CSS transition is applied to a button's `color` and `background-color`. The button's text transitions smoothly, but the developer notices the transition doesn't fire when the button is in a `:disabled` state and is then re-enabled.

```css
.button { transition: background-color 0.2s ease, color 0.2s ease; }
.button:disabled { background-color: #ccc; color: #999; pointer-events: none; }
```

When `disabled` attribute is removed, the transition from gray to primary color fires but the text color transition doesn't. Investigation shows `color` is being inherited from a parent that already updated. Show: explicit `color` on both `.button` and `.button:not(:disabled)` states, and why CSS transitions only fire when the computed value changes from a previous explicitly set value (not inherited changes).""",

"""**Task (Code Generation):**
Build a responsive CSS calendar component using Grid without JavaScript for layout:

```css
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr); /* 7 days */
}

.day-offset-1 { grid-column-start: 2; } /* Month starts on Tuesday */
.day-offset-6 { grid-column-start: 7; } /* Month starts on Sunday */
```

Show: the complete calendar grid CSS, how to implement week number column (8 columns: week number + 7 days), current day highlighting with `::today-like` styling using custom data attribute `data-today`, event dots using absolute positioning, and how `grid-row: span X` handles multi-day events with overflow to next row.""",

"""**Debug Scenario:**
An SVG icon system uses `currentColor` to inherit text color, but icons inside buttons with `color: white` text appear white correctly — except on hover, where the button has `filter: brightness(0.9)` applied and icons appear dimmed more than the text.

```css
.button:hover { filter: brightness(0.9); }
.button svg { fill: currentColor; } /* Icon also gets brightness filter */
```

CSS `filter` applies to the entire element and its subtree. Show: applying `filter` only to the background using a pseudo-element (`::before` with the background color), using `backdrop-filter` on the button's overlay, and `mix-blend-mode` as an alternative for hover effects that don't affect child element colors.""",

]

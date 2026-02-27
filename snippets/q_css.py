"""
snippets/q_css.py — 28 FRESH CSS/Styling questions (mix of debugging + code generation)
Zero overlap with archived set.
"""

Q_CSS = [

"""**Task (Code Generation):**
Implement a pure CSS responsive card grid that:
- Shows 1 column on mobile, 2 on tablet, 3 on desktop with NO media queries
- Uses CSS Grid's `auto-fill` + `minmax` for intrinsic responsiveness
- Cards have equal height per row (no orphan short cards)
- Has a "featured" card variant that spans 2 columns on larger grids
- Works with dynamic card count (0 to N cards)

Show the CSS and explain why `auto-fill` vs `auto-fit` behaves differently when there are fewer items than columns.""",

"""**Debug Scenario:**
A sticky table header stops being sticky when the parent container has `overflow: auto`. The header is set to `position: sticky; top: 0` but scrolls with the content instead of sticking.

```css
.table-wrapper { overflow: auto; } /* breaks sticky */
.table-header { position: sticky; top: 0; }
```

Explain why `overflow: auto/scroll/hidden` on a parent creates a new scroll container and breaks `position: sticky`. Show the correct architecture for a scrollable table with a sticky header that doesn't require JavaScript positioning.""",

"""**Task (Code Generation):**
Build a CSS-only dark mode theme system for a Next.js app using CSS custom properties (no Tailwind, no CSS-in-JS):

```css
:root { --color-bg: #ffffff; --color-text: #1a1a1a; }
[data-theme="dark"] { --color-bg: #0f0f0f; --color-text: #f0f0f0; }
```

Requirements:
- Respects `prefers-color-scheme: dark` by default (no JS needed)
- Can be overridden by user preference (stored in a `data-theme` attribute on `<html>`)
- No Flash Of Unstyled Content (FOUC) when the user's preference loads
- Shows how to apply the CSS variables to Next.js's `<body>` without hydration mismatch""",

"""**Debug Scenario:**
A loading spinner animation (`@keyframes` rotation) causes the entire page to jank every frame on a mid-tier Android device. Chrome DevTools Performance tab shows the animation is on the main thread, not the compositor.

```css
.spinner {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg) translateX(10px); } /* ← problem */
  to { transform: rotate(360deg) translateX(10px); }
}
```

Explain why `transform` animations should be GPU-composited but this specific animation isn't, and rewrite it to animate only compositor-friendly properties.""",

"""**Task (Code Generation):**
Implement a responsive typography system using CSS `clamp()` for fluid font sizes:

```css
/* Font scale that smoothly transitions between mobile and desktop breakpoints */
--text-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
--text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
--text-xl: clamp(1.25rem, 1rem + 1.25vw, 1.875rem);
--text-4xl: clamp(2rem, 1.5rem + 2.5vw, 3.5rem);
```

Show how to calculate the `clamp()` values for any font size/viewport range using a formula, implement an 8-level type scale, and explain when fluid typography is better vs worse than breakpoint-based sizing.""",

"""**Debug Scenario:**
A CSS Grid layout has items that overflow their cells horizontally on Firefox but not Chrome. The cells have `min-width: 0` but child elements with `white-space: nowrap` cause overflow.

```css
.grid { display: grid; grid-template-columns: 1fr 1fr; }
.cell { min-width: 0; overflow: hidden; }
.content { white-space: nowrap; } /* overflows in Firefox */
```

Explain the browser difference in how `min-width: 0` interacts with `1fr` columns between Chrome and Firefox. Show additional CSS needed to contain the overflow and why `text-overflow: ellipsis` requires an additional `display: block` in some browsers.""",

"""**Task (Code Generation):**
Build a CSS scroll-driven animation (no JavaScript) that:
- Reveals a progress bar at the top of the page as the user scrolls
- Fades in section headings as they enter the viewport
- Applies a parallax effect to a hero image

Use the CSS `@scroll-timeline` / `scroll()` and `view()` animation timeline features. Show browser support fallbacks using `@supports` and a JavaScript `IntersectionObserver` fallback for browsers that don't support scroll-driven animations.""",

"""**Debug Scenario:**
A user reports that on their high-contrast Windows system, the app's custom checkbox styles are invisible. Custom checkboxes use `appearance: none` to replace the native checkbox with a CSS-only design.

```css
input[type="checkbox"] {
  appearance: none;
  width: 16px;height: 16px;
  background: white;
  border: 2px solid #666;
}
```

Explain Windows High Contrast Mode (now called "Forced Colors Mode") and how it overrides custom CSS colors with system colors. Show how to use `@media (forced-colors: active)` to restore checkbox visibility.""",

"""**Task (Code Generation):**
Implement a CSS-only accordion component (no JavaScript) that:
- Expands/collapses panel content
- Animates height from 0 to auto (CSS-only, no fixed heights)
- Has smooth easing for open and close
- Works with keyboard navigation (tab/enter)
- Maintains accessibility (aria-expanded, aria-controls)

Use the HTML `<details>` + `<summary>` elements with CSS `::details-content` or a checkbox hack as fallback. Show both approaches and their accessibility tradeoffs.""",

"""**Debug Scenario:**
A CSS Grid dashboard layout breaks on a 1280px viewport — a column appears to be 10px narrower than expected, causing a horizontal scrollbar.

The grid is:
```css
.grid {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 20px;
  padding: 20px;
}
```

On a 1280px container, `240 + 20 (gap) + 40 (padding) = 300px` leaves `980px` for `1fr`. But the horizontal scrollbar appears at exactly 1280px viewport. Investigate: is this a scrollbar width issue (scrollbar takes 15px, making the viewport 1265px), a box-sizing issue, or a `vw` vs `%` width issue?""",

"""**Task (Code Generation):**
Build a design token system using CSS custom properties with TypeScript type safety:

```ts
// tokens.ts → generates tokens.css
const tokens = defineTokens({
  colors: {
    primary: { 50: '#eff6ff', 500: '#3b82f6', 900: '#1e3a8a' },
    neutral: { 100: '#f5f5f5', 900: '#171717' },
  },
  spacing: { 1: '4px', 2: '8px', 4: '16px', 8: '32px' },
  radii: { sm: '4px', md: '8px', full: '9999px' },
});

type ColorToken = typeof tokens.colors; // Type-safe color access
```

Show the `defineTokens` function, the CSS variable name generation (`--color-primary-500`), and a TypeScript-typed `token()` helper for use in styled-components or vanilla-extract.""",

"""**Debug Scenario:**
A CSS animation using `transform: scale()` on a card component causes sibling cards to shift/relayout on every frame. The animation is supposed to be GPU-composited and not affect layout.

```css
.card:hover {
  animation: pulse 1s infinite;
}
@keyframes pulse {
  50% { transform: scale(1.05); }
}
```

Despite `transform` not affecting layout, siblings are shifting. Diagnose: is this a `transform-origin` issue (the card expands into sibling space), a `box-shadow` side-effect, or a `border-width` animation that accidentally crept in? Show the fix using `outline` instead of shadow animation.""",

"""**Task (Code Generation):**
Implement CSS Layers (`@layer`) to manage specificity in a Next.js app that combines:
- A third-party component library (high specificity utility classes)
- Global CSS resets
- App-specific component styles
- Utility classes

```css
@layer reset, base, components, utilities, overrides;
```

Show how to assign each style source to a layer, how layer order determines specificity (not selector specificity), and a concrete example where layers solve a conflict that `!important` would otherwise require.""",

"""**Debug Scenario:**
A `<Tabs>` component has active tab indicator that uses an animated underline. The underline animates smoothly between tabs on Chromium but snaps instantly on Safari, ignoring the CSS transition.

```css
.tab-indicator {
  position: absolute;
  bottom: 0;
  left: var(--indicator-left);
  width: var(--indicator-width);
  transition: left 0.3s ease, width 0.3s ease;
}
```

`--indicator-left` is a CSS custom property updated via inline styles. Explain why CSS transitions don't animate CSS custom property changes in older Safari, and show the alternative: using `transform: translateX()` (which does animate) instead of `left`.""",

"""**Task (Code Generation):**
Build a composable CSS utility class system (Tailwind-inspired) for a design system WITHOUT Tailwind:

```css
/* Generated utilities: */
.p-4 { padding: 1rem; }
.text-primary-500 { color: var(--color-primary-500); }
.flex { display: flex; }
.gap-2 { gap: 0.5rem; }
```

Show a Node.js build script that generates utility classes from the design token system, a PostCSS plugin that tree-shakes unused utilities by scanning JSX files, and how to scope utilities to avoid conflicts with third-party styles using CSS Layers.""",

"""**Debug Scenario:**
A multi-column CSS layout using `column-count: 3` breaks newspaper-style columns by orphaning a heading at the bottom of one column, separated from its content which flows into the next column.

```css
.content { column-count: 3; column-gap: 2rem; }
h2 { /* heading at bottom of column, content in next */ }
```

Show the CSS `break-after`, `break-before`, and `break-inside: avoid` properties that control column breaks, and explain why `page-break-*` is the legacy equivalent. Also show `column-span: all` for full-width elements inside a multi-column layout.""",

"""**Task (Code Generation):**
Implement a CSS-only skeleton loading animation for a card grid:

```html
<div class="card skeleton">
  <div class="skeleton-image"></div>
  <div class="skeleton-title"></div>
  <div class="skeleton-text"></div>
</div>
```

Requirements:
- Shimmer animation using `linear-gradient` + CSS animation (no JS)
- Respects `prefers-reduced-motion: reduce` (stops animation for accessibility)
- Matches the exact dimensions of real content (prevents layout shift when content loads)
- Works in both light and dark mode using CSS variables

Show the complete CSS.""",

"""**Debug Scenario:**
A `position: fixed` element (a cookie banner) is appearing behind a modal overlay on iOS Safari. Both elements are in the same stacking context. The modal has `z-index: 1000` and the banner has `z-index: 999`.

On desktop Chrome the layering is correct. On iOS Safari, the banner appears on top despite lower z-index.

Diagnose iOS Safari's stacking context behavior with `-webkit-overflow-scrolling: touch` and show the fix. Explain why iOS Safari creates new stacking contexts for `-webkit-overflow-scrolling` elements and which properties trigger this.""",

"""**Task (Code Generation):**
Build a theme switcher component that supports light, dark, and system themes with no flash on page load:

Requirements:
- Theme preference stored in localStorage
- On first paint, reads localStorage synchronously via an inline `<script>` in `<head>` (before React hydrates)
- Applies theme by setting `data-theme` on `<html>` element
- Falls back to `prefers-color-scheme` if no localStorage preference
- TypeScript hook `useTheme()` returns current theme and a `setTheme` function

Show the inline script, the Next.js `<head>` integration, and the React hook.""",

"""**Debug Scenario:**
A complex CSS animation involving multiple `@keyframes` runs smoothly in Chrome DevTools but shows choppy frame drops when the browser tab is in the background and returns to foreground.

Explain what happens to `requestAnimationFrame` and CSS animations when a browser tab is backgrounded (throttled to 1fps in most browsers), and how to correctly pause and resume animations using `animation-play-state` combined with the Page Visibility API. Show the JavaScript + CSS combination.""",

"""**Task (Code Generation):**
Implement a responsive data table with CSS that handles:
- Horizontal scrolling on mobile devices
- A frozen (sticky) first column for row labels
- Alternating row colors
- Highlighted "active" row
- Column sorting indicator (CSS-only arrow icons)

```html
<div class="table-container">
  <table class="data-table">...</table>
</div>
```

Show the complete CSS for all requirements and explain the `overscroll-behavior` property for mobile horizontal scroll containment.""",

"""**Debug Scenario:**
A CSS animation using `clip-path` to reveal content is causing layout invalidation on every frame in the Chrome Performance panel. The `clip-path` changes from `inset(100% 0 0 0)` to `inset(0 0 0 0)`.

```css
@keyframes reveal {
  from { clip-path: inset(100% 0 0 0); }
  to { clip-path: inset(0 0 0 0); }
}
```

Determine if `clip-path` animation is compositor-friendly (runs off main thread). Explain which `clip-path` shapes trigger layout/paint vs. which only trigger composite, and show how to profile this in Chrome's Layers panel. Offer an alternative approach using `transform: translateY` + `overflow: hidden` parent.""",

"""**Task (Code Generation):**
Implement a masonry layout in CSS (Pinterest-style) that works without JavaScript for item placement:

Approach 1: CSS Grid with `grid-template-rows: masonry` (Firefox experimental)
Approach 2: CSS Multi-column layout
Approach 3: CSS Flexbox with column direction

Show all three approaches, their browser support, and the tradeoff: Approach 3 (flexbox columns) forces reading-order to go top-to-bottom per column instead of left-to-right per row. How do you fix the reading order while maintaining visual masonry?""",

"""**Debug Scenario:**
A production dashboard's CSS animations are smooth in development but stutter in production. Bundle analysis shows the CSS for animations is the same in both environments. Chrome DevTools shows the production build has significantly more painted layers.

The production build uses CSS Modules with class name shortening (`_a13x4`, `_b5k2z`, etc.) — these short class names collide with CSS Modules from different components, causing unintended style sharing between components.

Verify this diagnosis: show how CSS Module name hashing works, why short hashes increase collision probability, and how to configure CSS Modules to use longer hashes with the file path included.""",

"""**Task (Code Generation):**
Build a CSS-in-JS alternative using the CSS Houdini Paint API to draw custom borders:

```css
.card {
  --border-radius: 8px;
  --border-color: blue;
  --border-width: 2px;
  border: none;
  background: paint(fancy-border);
}
```

Show the Paint Worklet JavaScript (runs in the browser's paint thread), how to register it with `CSS.paintWorklet.addModule()`, how to pass CSS custom properties to the worklet, and the browser support status with a CSS fallback.""",

"""**Debug Scenario:**
A `::before` pseudo-element is used to add decorative content to a component. The pseudo-element appears in Chrome but is missing in Firefox and Safari. The component uses CSS Modules.

```css
/* card.module.css */
.card::before {
  content: '';
  display: block;
  height: 4px;
  background: linear-gradient(to right, blue, purple);
}
```

Investigation shows the CSS compiles correctly. The `.card` class is applied. DevTools in Firefox shows the `::before` rule matched but the element is not rendering. What are the common reasons a `::before` pseudo-element renders in Chrome but not in Firefox/Safari, and how do you systematically debug pseudo-element rendering?""",

"""**Task (Code Generation):**
Create a complete print stylesheet for a Next.js dashboard report page that:
- Hides navigation, sidebar, action buttons, and tooltips
- Shows a print-only header with the company logo and report title
- Breaks pages at sensible points (between sections, not mid-table)
- Forces black-and-white printing for charts (replaces colors with patterns)
- Shows URLs next to all links
- Uses `cm`/`mm` units for print layout (not `px`)

Show the CSS `@media print` stylesheet and how to apply it in Next.js's App Router without affecting screen styles.""",

"""**Task (Code Generation):**
Implement a CSS logical properties migration for an existing RTL (right-to-left) language support project. The existing codebase uses physical properties (`margin-left`, `padding-right`, `border-left`, `float: left`).

```css
/* Before (physical): */
.nav { margin-left: auto; border-right: 1px solid; }
/* After (logical): */
.nav { margin-inline-start: auto; border-inline-end: 1px solid; }
```

Show:
1. The mapping table: physical → logical property equivalents
2. A PostCSS plugin configuration (`postcss-logical`) that auto-converts physical to logical
3. How to test RTL layout using Chrome DevTools' forced RTL direction
4. Which properties have no logical equivalent and need manual handling (e.g., `float`)""",

]

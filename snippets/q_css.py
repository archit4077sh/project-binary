"""
snippets/q_css.py — BATCH 5: 28 brand-new CSS/Styling questions
Zero overlap with batch1, batch2, batch3, or batch4 archives.
"""

Q_CSS = [

"""**Task (Code Generation):**
Implement a design token system using CSS layers (`@layer`) for cascade control:

```css
/* Establish layer order — lower layers lose to higher: */
@layer reset, tokens, base, components, utilities, overrides;

@layer tokens {
  :root {
    --space-1: 4px;  --space-2: 8px; --space-4: 16px;
    --color-brand: hsl(240 80% 60%);
    --radius-md: 8px;
  }
}

@layer components {
  .card {
    padding: var(--space-4);
    border-radius: var(--radius-md);
    background: var(--color-surface);
  }
}

@layer utilities {
  .mt-4 { margin-top: var(--space-4); }
  /* Utilities win over components without !important: */
  .p-0 { padding: 0; } /* overrides card's padding when both applied */
}
```

Show: layer ordering (later in `@layer` = higher priority), unlayered styles beating all layered styles, `@import` with layers, and the `@layer` overrides layer for third-party CSS override isolation.""",

"""**Debug Scenario:**
A developer uses `display: grid` with `auto-fill` and `minmax`, but the grid items are too wide on mobile because the minimum size is too large:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}
/* On a 320px screen: 300px min > 320px container → items overflow */
```

When the container is narrower than the `min` in `minmax`, items overflow the grid container. Show: using `min(300px, 100%)` as the minimum to prevent overflow:

```css
grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr));
```

The difference between `auto-fill` (creates empty columns) and `auto-fit` (collapses empty columns), and the inspector showing the grid track breakdown.""",

"""**Task (Code Generation):**
Build a CSS typing animation for a hero section:

```css
.hero-text {
  font-size: clamp(2rem, 5vw, 4rem);
  overflow: hidden;
  white-space: nowrap;
  border-right: 3px solid var(--color-brand); /* cursor */
  width: 0;
  animation:
    typing 3s steps(30, end) forwards,      /* text reveal */
    blink  0.8s step-end infinite;          /* cursor blink */
}

@keyframes typing {
  from { width: 0; }
  to   { width: 100%; }
}

@keyframes blink {
  0%, 100% { border-color: transparent; }
  50%       { border-color: var(--color-brand); }
}
```

Show: `steps(n, end)` for discrete character-by-character animation (not continuous), calculating the right `n` value (equal to character count), the cursor element removal using `animation-fill-mode: forwards` after the text finishes typing, and `prefers-reduced-motion` disabling the animation.""",

"""**Debug Scenario:**
A developer adds a dark mode toggle using `data-theme="dark"` on the `<html>` element, but the CSS custom properties don't cascade into shadow DOM of web components:

```css
/* Light mode: */
:root { --bg: white; --text: black; }

/* Dark mode: */
[data-theme="dark"] { --bg: #1a1a1a; --text: white; }
```

CSS custom properties DO inherit through shadow DOM boundaries (they're inherited properties). The issue is the web component uses Shadow DOM with `mode: 'closed'` — closed shadow roots may not inherit from the document in some implementations.

Show: using `mode: 'open'` for inheritable custom properties, the `@media (prefers-color-scheme)` inside shadow DOM for respecting OS dark mode, and the CSS `color-scheme` property for browser chrome (scrollbars, form inputs) to match dark mode.""",

"""**Task (Code Generation):**
Implement accessible skip links and focus management for a single-page application:

```css
/* Skip link — visually hidden but focusable: */
.skip-link {
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.skip-link:focus {
  position: fixed;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  width: auto;
  height: auto;
  padding: 0.5rem 1rem;
  background: var(--color-brand);
  color: white;
  z-index: 9999;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
}
```

Show: the skip link HTML (`<a href="#main-content" class="skip-link">Skip to content</a>`), the `<main id="main-content" tabindex="-1">` target (tabindex for programmatic focus), multiple skip links for navigation, search, and main content, and SPA routing focus management (focus `<main>` on route change).""",

"""**Debug Scenario:**
A developer uses `@font-face` for a custom font, but the font renders in bold on some Windows machines even though the font weight is set to `400`:

```css
@font-face {
  font-family: 'MyFont';
  src: url('myfont.woff2');
  /* Missing: font-weight and font-style descriptors! */
}

h1 { font-family: 'MyFont'; font-weight: 400; }
```

Without `font-weight` and `font-style` descriptors in `@font-face`, the browser applies **faux bold** (algorithmically thickens the font) when the CSS requests a non-default weight. Show: adding `font-weight: 400; font-style: normal;` descriptors to the `@font-face` declaration, declaring separate `@font-face` blocks for each weight/style combination, and using `font-display: swap` for improved perceived performance.""",

"""**Task (Code Generation):**
Build a CSS-only responsive data table that converts to card layout on mobile:

```css
/* Desktop: standard table */
@media (min-width: 768px) {
  .data-table { display: table; width: 100%; }
}

/* Mobile: each row becomes a card */
@media (max-width: 767px) {
  .data-table         { display: block; }
  .data-table thead   { display: none; }  /* hide headers */
  .data-table tr      { display: block; margin-bottom: 1rem; border: 1px solid; }
  .data-table td      { display: flex; justify-content: space-between; }
  .data-table td::before {
    content: attr(data-label);  /* show column name from data-label attribute */
    font-weight: bold;
  }
}
```

Show: the `data-label` HTML attribute on each `<td>`, CSS `content: attr()` to display it, semantic HTML table preservation for accessibility (screen readers read it as a table), and `role="table"` overrides when using `display: block` (which removes table semantics).""",

"""**Debug Scenario:**
A web component's internal `<button>` styles don't reflect the page's CSS theme variable changes even though CSS custom properties should pierce shadow DOM:

```js
// Web component shadow root:
this.shadowRoot.innerHTML = `
  <style>
    button { background: var(--color-primary, blue); }
  </style>
  <button>Click me</button>
`;
```

The component correctly uses `var(--color-primary)` with a fallback. Investigation reveals the page sets `--color-primary` on a descendant element, not on `:root`. CSS custom properties are inherited but only from ancestors. Show: setting custom properties on `:root` or `html` (ancestors of ALL elements including shadow hosts), using `::part()` for external styling without custom properties, and the `@property` rule within shadow DOM for independent registered properties.""",

"""**Task (Code Generation):**
Implement a responsive sidebar navigation with CSS `has()` for state management:

```css
/* Sidebar state stored in a hidden checkbox: */
input#nav-toggle { display: none; }

/* Layout adjusts when checkbox is checked: */
html:has(#nav-toggle:checked) .sidebar {
  transform: translateX(0);
}

html:has(#nav-toggle:checked) .main-content {
  margin-left: 280px;
}

html:has(#nav-toggle:checked) .nav-overlay {
  display: block;
  opacity: 1;
}
```

Show: the full nav structure with `<label>` for the toggle button, CSS `has()` for parent-conditional styling, smooth transition on the sidebar, keyboard accessibility (the `<label>` must have associated text or aria-label), `prefers-reduced-motion` disabling the slide animation, and why this technique works without JavaScript.""",

"""**Debug Scenario:**
A developer uses `box-shadow` for a card elevation effect, but the shadow is clipped by a parent element with `overflow: hidden`:

```css
.parent { overflow: hidden; }
.card   { box-shadow: 0 8px 24px rgba(0,0,0,0.2); } /* shadow clipped! */
```

`overflow: hidden` clips ALL content outside the element bounds, including `box-shadow`. Show: three solutions — (1) `filter: drop-shadow(0 8px 24px rgba(0,0,0,0.2))` is not clipped by `overflow: hidden` (applies after clipping), (2) add `padding` to the parent so the shadow fits within bounds, (3) add an inner wrapper inside the overflow parent that applies the shadow. Comparison: `box-shadow` vs `filter: drop-shadow` performance (drop-shadow requires compositing the entire element).""",

"""**Task (Code Generation):**
Build a CSS accordion component using the `<details>` element without JavaScript:

```css
details { border: 1px solid var(--color-border); border-radius: 8px; }

summary {
  padding: 1rem;
  cursor: pointer;
  list-style: none;          /* remove default arrow */
  display: flex;
  justify-content: space-between;
  align-items: center;
}

summary::after {
  content: '+';
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

details[open] summary::after {
  content: '−';
  transform: rotate(180deg);
}

.accordion-content {
  padding: 0 1rem;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, padding 0.3s ease;
}

details[open] .accordion-content {
  max-height: 500px;
  padding: 1rem;
}
```

Show: `::-webkit-details-marker` removal for cross-browser, `details[open]` state selector, the `max-height` animation trick for smooth open/close, and the new `interpolate-size: allow-keywords` + `max-height: calc-size(auto)` for true height-to-auto animation in modern browsers.""",

"""**Debug Scenario:**
A complex CSS animation jank appears on mobile devices — the animation is defined with `transform` and `opacity`, which should be GPU-accelerated, but DevTools shows "Paint" events during the animation:

```css
.card {
  animation: slideIn 0.5s ease;
  will-change: transform, opacity; /* should be GPU composited */
}
@keyframes slideIn {
  from { transform: translateY(20px); opacity: 0; }
  to   { transform: translateY(0); opacity: 1; }
}
```

Investigation with DevTools "Layers" panel shows the card renders in the same layer as 200 other elements. Show: `will-change: transform` promoting the element to its own compositing layer (but only when animation is about to start, not always), the memory cost of too many composited layers, and using `@starting-style` (new CSS property) for the enter animation instead of `@keyframes` for elements that animate in from `display: none`.""",

"""**Task (Code Generation):**
Implement CSS container-style queries for adapting component appearance to its container's style:

```css
/* Container with a style query: */
.product-grid {
  container-type: style;
  container-name: product-grid;
  --layout: grid;
}

/* Apply different styles based on container's --layout value: */
@container product-grid style(--layout: list) {
  .product-card {
    display: flex;
    flex-direction: row;
  }
  .product-card img {
    width: 100px;
  }
}

@container product-grid style(--layout: grid) {
  .product-card {
    display: block;
  }
}
```

Show: CSS style queries (querying custom property values of a container), the `container-type: style` declaration, toggling `--layout` value via JavaScript or a sibling `<input>`, and the `@supports (container-type: style)` progressive enhancement check.""",

"""**Debug Scenario:**
A developer uses `transform: scale(0)` to hide an element instead of `display: none`, then animates `scale` to 1. But the hidden element (scale: 0) is still accessible via keyboard Tab navigation:

```css
.hidden { transform: scale(0); }
.visible { transform: scale(1); transition: transform 0.3s; }
```

`transform: scale(0)` makes the element invisible but keeps it in the accessibility tree and tab order — the 0-size element still receives focus. Show: combining `transform: scale(0)` with `pointer-events: none; visibility: hidden; tab-index: -1` for proper hiding, or using `opacity: 0` + `visibility: hidden` (which removes from tab order), and the `inert` HTML attribute (standards-based way to remove an element from interaction and accessibility tree).""",

"""**Task (Code Generation):**
Build a multi-column text layout with balanced columns and hyphenation:

```css
.article-body {
  /* 2-3 columns depending on screen width: */
  column-count: 2;
  column-gap: 2rem;
  column-rule: 1px solid var(--color-border);

  /* Prevent content from breaking across columns mid-element: */
  & h2, & h3, & figure {
    break-before: column;   /* always start on a new column */
    break-inside: avoid;   /* don't split across columns */
  }
  
  /* Hyphenation for justified text in narrow columns: */
  hyphens: auto;
  text-align: justify;
  overflow-wrap: break-word;
}
```

Show: `column-span: all` for full-width headings within a multi-column layout, `column-fill: balance` vs `auto`, `widows` and `orphans` CSS properties for controlling line breaks at column tops/bottoms, and `hyphenate-character` for custom hyphen character.""",

"""**Debug Scenario:**
A CSS Grid layout where one column should be `auto` width (shrink to content) and the remaining space goes to another column. The developer uses `1fr` and `auto`, but `auto` isn't working — both columns are equal:

```css
.layout {
  display: grid;
  grid-template-columns: auto 1fr; /* should be: shrink-fit | fill-remaining */
}
```

`auto` in a grid track resolves to `minmax(auto, max-content)` — it can GROW if space is available, not just shrink. Show: using `fit-content(250px)` for the auto column (shrinks to content but doesn't exceed 250px), `min-content` to force the column to be as narrow as possible, and `minmax(0, 1fr)` vs `1fr` in the fill column (the `0` prevents content-driven minimum size from affecting the 1fr calculation).""",

"""**Task (Code Generation):**
Implement a CSS-only smooth page transition using the View Transition API:

```css
/* Default cross-fade: */
::view-transition-old(root) { animation: 0.3s ease fade-out; }
::view-transition-new(root) { animation: 0.3s ease fade-in; }

/* Named view transition for specific elements: */
.hero-image { view-transition-name: hero; }

::view-transition-old(hero) {
  animation: 200ms ease-out slide-out;
}
::view-transition-new(hero) {
  animation: 200ms ease-in slide-in;
}

@keyframes slide-out { to { transform: translateX(-100%); } }
@keyframes slide-in  { from { transform: translateX(100%); } }
```

Show: triggering `document.startViewTransition(() => updateDOM())`, the full lifecycle (paint → snapshot → transition), the `navigation` API for SPA transitions, and `prefers-reduced-motion: reduce` disabling all transitions (`::view-transition-group(*) { animation-duration: 0.001ms; }`).""",

"""**Debug Scenario:**
A developer uses `position: sticky` on a table header but it stops working after a certain scroll position and the header scrolls away with the content:

```css
th { position: sticky; top: 0; }
/* Works initially, then breaks after 500px of scroll */
```

Investigation reveals a `transform` on a parent wrapper element (a scroll-based parallax effect) that creates a new stacking context, which confines the sticky element's scroll tracking to the transformed parent rather than the viewport. Show: removing `transform` from the sticky parent (use `top`/`left` for positioning instead), using `will-change` as a `transform` alternative for layer promotion without breaking sticky, and a JavaScript `IntersectionObserver` fallback for sticky behavior in complex layout situations.""",

"""**Task (Code Generation):**
Build a print-optimized CSS stylesheet:

```css
@media print {
  /* Remove navigation, ads, and interactive elements: */
  nav, aside, .ad-banner, button, .print-hidden { display: none; }

  /* Show full URLs for links: */
  a[href]::after { content: ' (' attr(href) ')'; font-size: 0.8em; color: #666; }
  a[href^='#']::after { content: ''; } /* hide fragment links */

  /* Page breaks: */
  h1, h2            { break-before: page; }
  figure, blockquote { break-inside: avoid; }
  p, li              { orphans: 3; widows: 3; }

  /* Content width: */
  body   { max-width: 100%; }
  .content { width: 100%; padding: 0; }
  
  /* Page setup: */
  @page { size: A4; margin: 2cm; }
  @page :first { margin-top: 3cm; } /* extra top margin on first page */
}
```

Show: `@page` with custom page size, `break-before` / `break-after` / `break-inside`, printing URLs in links, and a `.print-visible` utility class for print-only elements (e.g., a QR code, print header).""",

"""**Debug Scenario:**
A `<button>` inside a `<form>` is submitting the form even though the developer intended it to just trigger a JavaScript action:

```html
<form onSubmit={handleSubmit}>
  <input name="email" />
  <button onClick={handleOtherAction}>Do Something</button>
  <button type="submit">Submit</button>
</form>
```

The default `type` for `<button>` is `"submit"` — any button inside a form will submit it unless explicitly typed. Show: adding `type="button"` to buttons that shouldn't submit (`<button type="button" onClick={handleOtherAction}>`), the `type="reset"` variant that clears form fields, and the fact that pressing **Enter** in any text input also submits the form (the first submit button is activated) — useful to know when designing multi-action forms.""",

"""**Task (Code Generation):**
Implement a CSS scroll-snap photo gallery:

```css
.gallery {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: 1rem;
  scroll-behavior: smooth;
  
  /* Hide scrollbar visually but keep functionality: */
  scrollbar-width: none;        /* Firefox */
  &::-webkit-scrollbar { display: none; } /* Chrome/Safari */
}

.gallery-item {
  flex: 0 0 100%;            /* each item fills the container */
  scroll-snap-align: center;
  scroll-snap-stop: always;  /* don't skip items on fast swipe */
}
```

Show: `scroll-snap-type: x mandatory` vs `proximity`, `scroll-snap-align: start | center | end`, pagination dots using CSS `counter()` and `:scroll-marker-group` (CSS scroll progress API), and `scroll-padding-left` for accounting for a fixed sidebar when snapping.""",

"""**Debug Scenario:**
A CSS `position: fixed` navigation bar renders BELOW a `<dialog>` element in Chrome but ABOVE it in Firefox. The `<dialog>` has `z-index: 100` and the nav has `z-index: 999`:

```css
nav    { position: fixed; z-index: 999; }
dialog { z-index: 100; }   /* but appears above nav in Firefox! */
```

HTML `<dialog>` elements are rendered in the top layer — a special browser rendering layer above all other content regardless of `z-index`. Show: the `top-layer` concept (dialog, fullscreen elements, popover=auto elements all paint above everything), why `z-index` has no effect against top-layer elements, and the workaround: render the nav inside the dialog as a sibling, or use `popover` attribute on the nav to also put it in the top layer.""",

"""**Task (Code Generation):**
Build a dark mode system using CSS custom properties with OS, app, and per-component overrides:

```css
/* Layer 1: OS preference (lowest priority): */
@media (prefers-color-scheme: dark) {
  :root { --theme: dark; }
}

/* Layer 2: App-level override (via JS): */
[data-theme="light"] { --bg: #ffffff; --text: #0f172a; }
[data-theme="dark"]  { --bg: #0f172a; --text: #f8fafc; }

/* Layer 3: Component-level override: */
.marketing-hero {
  /* Force light mode for this section regardless of global theme: */
  color-scheme: light;
  --bg: var(--color-brand-light);
}
```

Show: all three override layers, the `color-scheme: light dark` meta tag for browser chrome, `transition: color 0.3s, background-color 0.3s` smooth theme change, and the `localStorage` + React context integration for persisting the app-level override.""",

"""**Debug Scenario:**
A developer sets `line-height: 24px` (absolute pixels) on text, but after the user increases browser font size for accessibility (to 150% of default), the text becomes cramped and lines overlap:

```css
p {
  font-size: 16px;    /* 24px after user zoom */
  line-height: 24px;  /* stays 24px — cramped! */
}
```

Absolute `line-height` values don't scale with `font-size` changes. Show: using unitless `line-height: 1.5` (relative to font-size — scales with zoom), the W3C recommendation for body text (`1.5`) and headings (`1.1-1.3`), how `line-height: 150%` differs from `1.5` for inherited values (percentage is computed first, then inherited as a fixed value; unitless is inherited as the multiplier and each element computes its own), and `font-size: 1rem` to respect the user's browser base font size.""",

"""**Task (Code Generation):**
Implement a CSS grid-based magazine layout with named areas:

```css
.magazine {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: auto;
  gap: 1.5rem;
  grid-template-areas:
    "hero hero hero hero hero hero hero hero hero hero hero hero"
    "lead lead lead lead feat feat feat feat aside aside aside aside"
    "art1 art1 art1 art2 art2 art2 art2 art3 art3 art3 art3 art3";
}

.hero  { grid-area: hero;  }
.lead  { grid-area: lead;  }
.feat  { grid-area: feat;  }
.aside { grid-area: aside; }

@media (max-width: 768px) {
  .magazine {
    grid-template-columns: 1fr;
    grid-template-areas:
      "hero"
      "lead"
      "feat"
      "aside"
      "art1" "art2" "art3";
  }
}
```

Show: the full CSS including the art article areas, responsive reflow with a single media query that redefines `grid-template-areas`, and `minmax` on rows to prevent content overflow.""",

"""**Debug Scenario:**
A CSS linear gradient `rgba(0,0,0,0)` to `rgba(0,0,0,1)` shows a gray "muddy" midpoint instead of a smooth fade-to-black on most browsers:

```css
.overlay {
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0),    /* transparent black */
    rgba(0, 0, 0, 1)     /* solid black */
  );
}
```

CSS `rgba(0,0,0,0)` is transparent black. When interpolating between transparent black and solid black in sRGB color space, the midpoint is a semi-transparent gray (because black = 0,0,0 and transparent = also 0,0,0, but mixing in perceptual sRGB smoothly still appears muddy). Show: using `linear-gradient(in oklch, transparent, black)` (oklch interpolation produces perceptually uniform gradients), `transparent` keyword as a shorthand for `rgba(0,0,0,0)` (same issue), and why gradient designers use actual semi-transparent colors at easing waypoints.""",

"""**Task (Code Generation):**
Implement a CSS `@scope` rule for encapsulated component styling without Shadow DOM:

```css
/* Scope styles to the .card component, preventing bleed: */
@scope (.card) to (.card-footer) {
  a { color: var(--color-brand); text-decoration: none; }
  h2 { font-size: 1.25rem; margin: 0; }
  /* These styles don't affect links/headings outside .card */
  /* And don't affect links/headings inside .card-footer */
}

/* Donut scope — applies between outer and inner boundary: */
@scope (.card) to (.section) {
  p { line-height: 1.6; color: var(--color-body); }
}
```

Show: `@scope` syntax with upper and lower scope boundaries, the `:scope` pseudo-class to reference the root element within the scope, nesting `@scope` inside a selector, the `@supports (selector(:scope))` progressive enhancement check, and comparing `@scope` vs CSS Modules vs Shadow DOM for component style encapsulation.""",

"""**Debug Scenario:**
A developer uses font icons (`<i class="icon icon-search">`) and reports that screen readers are announcing "search" or reading random Unicode characters to visually impaired users:

```html
<button class="btn-icon"><i class="icon icon-search"></i></button>
```

Font icon characters are in the Unicode Private Use Area — screen readers may read them as empty or as the Unicode codepoint. Show: adding `aria-hidden="true"` to the icon element, providing accessible label on the parent (`aria-label="Search"` on the button), using SVG icons with `aria-hidden="true"` on the SVG (screen readers see the button label only), and `role="img"` + `aria-label` as alternative on standalone decorative icons.""",

]

"""
snippets/q_css.py — BATCH 7: 55 brand-new CSS/Styling questions
Zero overlap with batches 1-6 archives.
"""

Q_CSS = [

'''**Task (Code Generation):**
Implement a CSS `@layer` architecture for a design system with external overrides:

```css
/* Define layer order FIRST (lowest to highest priority): */
@layer reset, base, tokens, components, utilities, overrides;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}

@layer tokens {
  :root {
    --color-primary: oklch(60% 0.15 250);
    --space-4: 1rem;
    --radius-md: 0.5rem;
  }
}

@layer components {
  .btn {
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-md);
    background: var(--color-primary);
  }
}

/* External theme override — higher priority because 'overrides' comes last: */
@layer overrides {
  .btn { background: var(--brand-color, var(--color-primary)); }
}
```

Show: the `@layer` ordering rule (declaration order determines specificity regardless of source order), importing third-party CSS into a layer (`@import 'normalize.css' layer(reset)`), unlayered styles having highest priority (highest specificity), and combining `@layer` with `@scope` for component encapsulation.''',

'''**Task (Code Generation):**
Build a `scroll-driven` animation system for a reading progress indicator:

```css
@keyframes grow-progress {
  0%   { width: 0%; }
  100% { width: 100%; }
}

.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 4px;
  background: oklch(65% 0.2 280);
  animation: grow-progress linear;
  animation-timeline: scroll(root);   /* document scroll */
  animation-range: 0% 100%;
}

/* Section-scoped progress: */
.chapter-progress {
  animation-timeline: scroll(nearest);
  animation-range: entry 0% exit 100%;
}
```

Show: `animation-timeline: scroll(root)` vs `scroll(nearest)` vs a named `scroll-timeline`, `animation-range: entry-crossing 0% exit 100%` for element-relative ranges, `view()` timeline for intersection-based animations (fade in as element enters viewport), and the `@scroll-timeline` named declaration approach.''',

'''**Task (Code Generation):**
Implement a CSS-only `color-mix()` theming system:

```css
:root {
  --color-brand: #6366f1;

  --color-brand-50:  color-mix(in oklch, var(--color-brand) 10%, white);
  --color-brand-100: color-mix(in oklch, var(--color-brand) 20%, white);
  --color-brand-200: color-mix(in oklch, var(--color-brand) 40%, white);
  --color-brand-500: var(--color-brand);
  --color-brand-700: color-mix(in oklch, var(--color-brand) 70%, black);
  --color-brand-900: color-mix(in oklch, var(--color-brand) 30%, black);

  /* Semi-transparent: */
  --color-brand-overlay: color-mix(in srgb, var(--color-brand) 20%, transparent);
}

.card { background: var(--color-brand-50); border: 1px solid var(--color-brand-200); }
.btn-primary { background: var(--color-brand-500); }
.btn-primary:hover { background: var(--color-brand-700); }
```

Show: `color-mix(in oklch, ...)` vs `in srgb` (oklch for perceptually uniform mixing), the percentage control (% of the first color), mixing with `transparent` for alpha variants, and the `relative color syntax` (`oklch(from var(--color-brand) calc(l + 0.1) c h)`).''',

'''**Task (Code Generation):**
Build an advanced CSS Grid layout with `subgrid` for perfectly aligned card components:

```css
/* Parent grid: */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* Card uses subgrid to align internal rows across siblings: */
.product-card {
  display: grid;
  grid-row: span 4;             /* Takes 4 rows in parent */
  grid-template-rows: subgrid;  /* Aligns to parent's row tracks */
}

/* Card sections automatically align across cards: */
.product-card .image   { grid-row: 1; } /* Row 1: all images same height */
.product-card .title   { grid-row: 2; } /* Row 2: all titles aligned */
.product-card .price   { grid-row: 3; } /* Row 3: all prices aligned */
.product-card .actions { grid-row: 4; } /* Row 4: all buttons at same level */
```

Show: `grid-template-rows: subgrid` aligning child rows to the parent grid (no need for fixed heights), combining subgrid with `auto-fill` columns, the masonry grid layout (`grid-template-rows: masonry` — currently behind a flag), and contrast with `align-items: stretch` for simpler equal-height cards.''',

'''**Task (Code Generation):**
Implement a CSS `@scope` block for component-scoped styles without naming conventions:

```css
/* Scope styles to .card — no BEM required: */
@scope (.card) {
  /* These styles only apply to elements INSIDE .card: */
  :scope { border: 1px solid #e2e8f0; border-radius: 0.5rem; padding: 1rem; }
  h2 { font-size: 1.125rem; font-weight: 600; }
  p  { color: #64748b; }
  .btn { background: #6366f1; }

  /* Don't apply inside .nested-card (scope boundary): */
  @scope (:scope) to (.nested-card) {
    p { color: #1e293b; } /* Only direct card paragraphs */
  }
}
```

Show: `@scope (.component) to (.nested-component)` for donut scope (apply inside outer, stop at inner), `:scope` pseudo-class referencing the scope root, `@scope` in `<style>` tags for shadow-DOM-like scoping in regular HTML, and how this compares to CSS Modules, BEM, and Shadow DOM.''',

'''**Task (Code Generation):**
Build a CSS `@property` animated custom property with spring-like easing:

```css
/* Register typed custom property for animation: */
@property --gradient-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

@property --shimmer-position {
  syntax: '<percentage>';
  initial-value: -100%;
  inherits: false;
}

.gradient-border {
  background: conic-gradient(from var(--gradient-angle), #6366f1, #8b5cf6, #6366f1);
  animation: spin-gradient 3s linear infinite;
}

@keyframes spin-gradient {
  to { --gradient-angle: 360deg; }
}

.shimmer {
  background: linear-gradient(
    90deg,
    transparent,
    color-mix(in srgb, white 60%, transparent) var(--shimmer-position),
    transparent
  );
  animation: shimmer 2s ease-in-out infinite;
}

@keyframes shimmer {
  to { --shimmer-position: 200%; }
}
```

Show: `@property` enabling CSS transition/animation of custom properties (without it, `transition: --angle` doesn't interpolate), `syntax` types (`<number>`, `<color>`, `<length>`, `<percentage>`, `<angle>`), `initial-value` requirement for animatability, and performance (runs on compositor thread).''',

'''**Task (Code Generation):**
Implement a `field-sizing: content` form layout for auto-growing textareas:

```css
/* Modern auto-growing textarea — no JavaScript: */
textarea {
  field-sizing: content;   /* Chrome 123+: auto-resizes to content */
  min-height: 80px;
  max-height: 400px;
  resize: none;            /* Browser resize handle not needed */
  overflow-y: auto;        /* Show scrollbar when at max-height */
}

/* Input that grows with its value: */
input[type="text"] {
  field-sizing: content;
  min-width: 5ch;
  max-width: 100%;
}

/* Fallback for older browsers: */
@supports not (field-sizing: content) {
  textarea { resize: vertical; }
}
```

Show: the `field-sizing: content` CSS property (standardized 2024), the JavaScript `setScaleValue` / `scrollHeight` approach as the widespread fallback, `field-sizing: fixed` (default behavior), and the `columns` property width on selects.''',

'''**Task (Code Generation):**
Build a CSS `text-wrap: balance` and `text-wrap: pretty` typographic system:

```css
/* Headlines: balanced line lengths */
h1, h2, h3 {
  text-wrap: balance;   /* Makes last line not dramatically shorter */
  max-width: 25ch;      /* Works best with defined max width */
}

/* Body text: orphan/widow prevention */
p {
  text-wrap: pretty;    /* Chrome 117+: prevents single-word last lines */
}

/* Combined with hyphenation for narrow columns: */
.narrow-column {
  hyphens: auto;
  hyphenate-character: '\2010'; /* Hyphen, not en-dash */
  text-wrap: pretty;
  overflow-wrap: break-word;    /* Long URLs */
}

/* Stable text for UI elements (no shift on hover): */
.menu-item { text-wrap: nowrap; }
.tag { text-wrap: nowrap; white-space: nowrap; }
```

Show: `balance` (slow but beautiful for headings, max 6 lines), `pretty` (faster, targets widow prevention), `stable` (prevents layout shift from bold on hover), `initial` (default), and browser support via `@supports (text-wrap: balance)`.''',

'''**Task (Code Generation):**
Implement an anchor positioning system for tooltips without JavaScript positioning:

```css
/* Anchor definition: */
.tooltip-trigger {
  anchor-name: --my-tooltip-anchor;
}

/* Positioned element references the anchor: */
.tooltip {
  position: absolute;    /* Required for anchor-pos */
  position-anchor: --my-tooltip-anchor;

  /* Position above the anchor: */
  bottom: anchor(top);          /* tooltip bottom = anchor top */
  left: anchor(center);         /* tooltip left = anchor center */
  translate: -50% 0;             /* Center-align horizontally */

  /* Auto-flip if not enough space: */
  position-try-fallbacks: flip-block, flip-inline;
}
```

Show: `anchor-name` defining anchors, `anchor()` function for positioning relative to the anchor, `position-try-fallbacks` for auto-flipping, `anchor-size()` for sizing relative to the anchor (`width: anchor-size(width)`), and combining with `@starting-style` for enter animations.''',

'''**Task (Code Generation):**
Build an advanced CSS `display: grid` masonry layout with variable row heights:

```css
/* True masonry grid (behind flag in Chrome, native in Firefox): */
.masonry-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: masonry;  /* Firefox: native masonry */
  gap: 1rem;
}

/* Cross-browser fallback using CSS columns: */
@supports not (grid-template-rows: masonry) {
  .masonry-grid {
    display: block;
    columns: 3;
    column-gap: 1rem;
  }
  .masonry-grid > * {
    break-inside: avoid;     /* Don't split items across columns */
    margin-bottom: 1rem;
  }
}
```

Show: the CSS `columns` property for multi-column layout (masonry fallback), `break-inside: avoid` for intact items, `column-span: all` for full-width items inside columns, the native `grid-template-rows: masonry` spec status, and `@media (prefers-reduced-motion)` for disabling layout animations.''',

'''**Task (Code Generation):**
Implement a CSS `@starting-style` enter animation for dynamically added elements:

```css
/* When a dialog opens, it enters from scale 0.95 + opacity 0: */
dialog[open] {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.2s ease, transform 0.2s ease;
}

/* Starting style — before the element's first style calculation: */
@starting-style {
  dialog[open] {
    opacity: 0;
    transform: scale(0.95);
  }
}

/* Close animation using popover: */
[popover] {
  transition: display allow-discrete 0.3s, overlay allow-discrete 0.3s, opacity 0.3s;
  opacity: 1;
}

@starting-style {
  [popover]:popover-open {
    opacity: 0;
  }
}
```

Show: `@starting-style` for entry animations (Chrome 117+), the `allow-discrete` transition for `display` and `overlay` (enables exit animations for removed elements), `[popover]` API, `<dialog>` open/close transitions, and `@supports (transition-behavior: allow-discrete)` feature detection.''',

'''**Task (Code Generation):**
Build a CSS custom highlight API for highlighting search results:

```js
// JavaScript registers the highlight:
const range = new Range();
range.setStart(textNode, startOffset);
range.setEnd(textNode, endOffset);

CSS.highlights.set('search-result', new Highlight(range));
CSS.highlights.set('selected-result', new Highlight(selectedRange));
```

```css
/* Style the registered highlights: */
::highlight(search-result) {
  background-color: oklch(90% 0.15 90);
  color: #1e293b;
}

::highlight(selected-result) {
  background-color: oklch(70% 0.2 250);
  color: white;
}
```

Show: `CSS.highlights` API for non-destructive text highlighting (no DOM manipulation needed), the Range API for defining highlight positions, `::highlight()` pseudo-element for styling, and using the Custom Highlight API with `Selection` for virtual text selection highlights.''',

'''**Task (Code Generation):**
Implement a CSS `view-transition` for page-level transitions with the View Transitions API:

```css
/* Global page transition: */
::view-transition-old(root) {
  animation: slide-out 300ms ease-in forwards;
}
::view-transition-new(root) {
  animation: slide-in 300ms ease-out forwards;
}

@keyframes slide-out { to { translate: -100% 0; opacity: 0; } }
@keyframes slide-in  { from { translate: 100% 0; opacity: 0; } }

/* Named element transitions (hero animation): */
.product-image { view-transition-name: var(--product-id); }
/* The image smoothly morphs between list view and detail view */
```

```js
document.startViewTransition(() => {
  navigate('/product/123');
});
```

Show: `document.startViewTransition()`, `::view-transition-old/new` pseudo-elements, `view-transition-name` for element-level transitions (hero animations), `view-transition-group()` for cross-document transitions (MPA View Transitions), and the `meta` tag for same-document MPA transitions.''',

'''**Task (Code Generation):**
Build a CSS `logical properties` layout for bi-directional (RTL/LTR) support:

```css
/* Instead of physical (left/right/top/bottom): */
.card {
  /* Physical: */
  /* margin-left: 1rem; padding-right: 1.5rem; border-left: 2px solid; */

  /* Logical (works in LTR and RTL): */
  margin-inline-start: 1rem;
  padding-inline-end: 1.5rem;
  border-inline-start: 2px solid;

  /* Also logical for block direction: */
  margin-block: 1rem 2rem;    /* top bottom */
  padding-inline: 1rem 2rem;  /* start end = left right in LTR */
  inset-block-start: 0;        /* top in horizontal writing mode */
}

:root { direction: ltr; }
[dir="rtl"] { direction: rtl; } /* All logical properties flip automatically */
```

Show: the full set of logical properties (`inline-start/end`, `block-start/end`, `border-inline`, `padding-block`), `writing-mode: vertical-lr` for vertical scripts, `overflow-inline` and `overflow-block`, and the DevTools logical property toggle for testing RTL.''',

'''**Task (Code Generation):**
Implement a CSS `has()` selector for complex parent-state styling:

```css
/* Style form based on what it CONTAINS: */
form:has(input:invalid) .submit-btn {
  opacity: 0.5;
  cursor: not-allowed;
}

form:has(input[type="file"]) .file-preview {
  display: block;
}

/* Card layout changes if it has a hero image: */
.card:has(> img.hero) {
  grid-template-rows: auto 1fr auto;
}

.card:not(:has(img)) .placeholder {
  display: block;
}

/* Navigation link current page highlight: */
nav a:has(> [aria-current="page"]),
nav a:is(:hover, :focus-visible) {
  background: var(--color-brand-50);
}
```

Show: `:has()` as a parent selector (Chrome 105+), combining with `:not(:has())`, `:has()` performance considerations (no look-forward from inside loops), and the `:has()` argument restriction (no pseudo-elements, only simple selectors in some browsers).''',

'''**Task (Code Generation):**
Build a CSS `oklch` color system for uniform perceptual contrast:

```css
:root {
  /* Define HSL-like but perceptually uniform: oklch(lightness chroma hue) */
  --color-blue-400: oklch(65% 0.17 260);  /* Lightness 65%, medium chroma, blue hue */
  --color-blue-500: oklch(55% 0.20 260);
  --color-blue-600: oklch(45% 0.19 260);

  /* Automatic dark mode variant: */
  --color-bg: oklch(100% 0 0);     /* White */
  --color-text: oklch(18% 0 0);    /* Near black */
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: oklch(18% 0 0);
    --color-text: oklch(95% 0 0);
    /* Blues stay perceptually similar brightness — just flip L: */
    --color-blue-400: oklch(80% 0.17 260);  /* Light on dark bg */
  }
}

/* Gamut-safe colors: */
.vibrant { color: oklch(70% 0.32 140); } /* Checks if P3 display available */
@media (color-gamut: p3) {
  .vibrant { color: oklch(70% 0.35 140); /* Wider gamut on P3 displays */ }
}
```

Show: OKLCH advantages over HSL (uniform lightness — `oklch(50% x h)` always looks equally bright across hues), P3 wide gamut colors (impossible in sRGB), `@supports (color: oklch(0% 0 0))` detection, and the `Oklch.js` library for programmatic palette generation.''',

'''**Task (Code Generation):**
Implement a CSS nesting-based component library with BEM-like structure:

```css
/* Native CSS nesting (Chrome 120+, Firefox 117+): */
.product-card {
  display: grid;
  border-radius: 0.5rem;

  & .image {
    aspect-ratio: 4/3;
    object-fit: cover;
  }

  & .body {
    padding: 1rem;

    & .title { font-size: 1.125rem; }
    & .price { color: #6366f1; }
  }

  /* State variants via nesting: */
  &:hover { box-shadow: 0 4px 12px oklch(0% 0 0 / 15%); }
  &[aria-selected="true"] { outline: 2px solid #6366f1; }

  /* Media query inside component: */
  @media (width > 640px) {
    & .body { padding: 1.5rem; }
  }
}
```

Show: native CSS nesting (`&` selector), nesting `@media` inside rules, the `& > .direct-child` vs `& .descendant` difference, `@layer` integration with nesting, and the PostCSS `postcss-nesting` plugin for older browser support.''',

'''**Task (Code Generation):**
Build a responsive layout using `container` queries with named containers:

```css
/* Named containers: */
.sidebar { container: sidebar / inline-size; }
.main    { container: main    / inline-size; }

/* Component adapts to ITS container, not viewport: */
@container sidebar (width < 200px) {
  .nav-item { flex-direction: column; }
  .nav-item span { display: none; }  /* Icon-only in narrow sidebar */
}

@container main (width > 800px) {
  .article-grid { columns: 2; }
}

/* Container style queries (Chrome 111+): */
@container style(--card-variant: compact) {
  .card { padding: 0.5rem; font-size: 0.875rem; }
}

/* Named container with size query: */
@container sidebar (block-size > 600px) {
  .nav { display: flex; flex-direction: column; }
}
```

Show: `container: name / type` shorthand, `container-name` and `container-type` longhand, `@container name (condition)` syntax, container style queries for prop-based variants, and `cqw`/`cqh` container query units.''',

'''**Task (Code Generation):**
Implement a CSS `backdrop-filter` glassmorphism card system:

```css
.glass-card {
  background: oklch(100% 0 0 / 10%);   /* 10% opaque white */
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border: 1px solid oklch(100% 0 0 / 20%);
  border-radius: 1rem;
  box-shadow:
    0 4px 6px oklch(0% 0 0 / 7%),
    0 0 0 1px oklch(100% 0 0 / 5%) inset;

  /* Ensure content behind is blurable: */
  /* Parent must NOT have overflow: hidden (clips the backdrop) */
}

@supports not (backdrop-filter: blur(1px)) {
  .glass-card {
    background: oklch(100% 0 0 / 85%);  /* Solid fallback */
    border-color: oklch(100% 0 0 / 50%);
  }
}
```

Show: `backdrop-filter` vs `filter` (applies to what's behind vs the element itself), the `saturate`, `brightness`, `contrast` filter functions composable with `blur`, the macOS/iOS Vibrancy effect — `backdrop-filter: blur(20px) saturate(150%) brightness(80%)`, and why the parent/stacking context must not clip the blur.''',

'''**Task (Code Generation):**
Build a CSS custom counter system for complex ordered lists:

```css
/* Multi-level legal document numbering: 1. → 1.1. → 1.1.1. */
.legal-doc {
  counter-reset: section;
}
.section {
  counter-increment: section;
  counter-reset: subsection;
}
.section > h2::before {
  content: counter(section) '. ';
}
.subsection {
  counter-increment: subsection;
  counter-reset: clause;
}
.subsection > h3::before {
  content: counters(section, '.') '.' counter(subsection) ' ';
}

/* Custom counter styles: */
@counter-style thumbs {
  system: cyclic;
  symbols: '👍' '✅' '⭐';
  suffix: ' ';
}
ol.reactions { list-style: thumbs; }
```

Show: `counter-reset`, `counter-increment`, `counter()` vs `counters()` (nested), `@counter-style` for custom symbols (system: cyclic, numeric, alphabetic, additive), and the `list-style: custom` shorthand.''',

'''**Task (Code Generation):**
Implement a CSS `overflow: clip` layout strategy for precise clipping:

```css
/* overflow: clip — clips without creating a scroll container */
.card-image-wrapper {
  overflow: clip;                 /* Clips visual overflow */
  overflow-clip-margin: 8px;     /* Allow slight overflow (rings, shadows) */
  border-radius: 0.5rem;
}

/* Use case: badge overflowing a stack without scroll containment */
.avatar-stack {
  overflow-x: clip;               /* Clip horizontal, allow vertical overflow */
  overflow-y: visible;
}

/* Clipping path for cutout shapes: */
.hexagon {
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}

.circle-cutout {
  clip-path: circle(40% at center);
}
```

Show: `overflow: clip` vs `hidden` (clip creates no scroll container — no sticky positioning issues, no clipping of fixed descendants), `overflow-clip-margin` for content-box expansion, `clip-path` with `path()`, `inset()`, and `polygon()`, and `shape-outside` for text flow around shapes.''',

'''**Task (Code Generation):**
Build a CSS pure `grid` based on `minmax` and `fit-content` for proportional layouts:

```css
/* Holy grail layout with named areas: */
.app-shell {
  display: grid;
  grid-template-columns: min(200px, 30%) 1fr min(200px, 30%);
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header header"
    "aside  main   panel "
    "footer footer footer";
  min-height: 100dvh;
}

.app-shell > header { grid-area: header; }
.app-shell > main   { grid-area: main; }
.app-shell > aside  { grid-area: aside; min-width: 0; } /* Prevent overflow */

/* Sidebar collapses at narrow widths: */
@media (width < 768px) {
  .app-shell {
    grid-template-columns: 1fr;
    grid-template-areas: "header" "main" "footer";
  }
  .app-shell > aside { display: none; }
}
```

Show: `grid-template-areas` for readable layout, `min()` for responsive column sizing, `100dvh` vs `100vh` (dynamic viewport height — accounts for mobile browser chrome), `min-width: 0` for preventing Grid blowout, and `fit-content()` for clamped-size tracks.''',

'''**Debug Scenario:**
A developer's CSS Grid `auto-fill` and `auto-fit` produce identical results in most cases but differ in an edge case:

```css
/* When there are fewer items than columns fill: */
.auto-fill { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
.auto-fit  { grid-template-columns: repeat(auto-fit,  minmax(200px, 1fr)); }

/* With 2 items in a 1200px container (fits 5 columns): */
/* auto-fill: 5 columns created, 2 filled, 3 empty — items don't stretch */
/* auto-fit:  empty columns COLLAPSED to 0 — 2 items stretch to fill space */
```

Show: the visual difference (items in a `min-width: 0` column vs collapsed), when to use each (`auto-fill` for fixed card sizes, `auto-fit` for fewer items that should stretch), and combining with `max-width` on items to prevent over-stretching with `auto-fit`.''',

'''**Debug Scenario:**
A developer's CSS `position: sticky` stops working when a parent has `overflow: hidden`:

```css
.container { overflow: hidden; }   /* Clips the sticky element! */
.sticky-header { position: sticky; top: 0; }
/* The sticky element is clipped inside the container — never sticks */
```

`position: sticky` requires all ancestors to have `overflow: visible` (the default). Setting `overflow: hidden/auto/scroll` on any ancestor creates a scroll container, clipping the sticky element inside it. Show: removing `overflow: hidden` from the container (use `overflow: clip` which doesn't create a scroll container), or using `clip-path` instead of `overflow: hidden` for visual clipping, and the DevTools checklist for debugging sticky positioning.''',

'''**Debug Scenario:**
A developer's CSS `:focus-visible` styles don't show on keyboard navigation in a custom button:

```tsx
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  style={{ outline: 'none' }} // Removed all focus styles!
>
  Custom button
</div>
```

```css
.custom-btn:focus-visible { outline: 2px solid #6366f1; } /* Not applied! */
```

The inline `style={{ outline: 'none' }}` overrides the CSS class with higher specificity. Also, `<div>` with `role="button"` may not trigger `:focus-visible` in all browsers (it depends on how focus was triggered). Show: removing the inline style override, using `outline: none` only via `&:focus:not(:focus-visible)` (and keeping `:focus-visible` styles), and wrapping in a real `<button>` which correctly supports `:focus-visible`.''',

'''**Debug Scenario:**
A developer's `transition` doesn't animate between `display: none` and `display: block`:

```css
.modal {
  display: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.modal.open {
  display: block;
  opacity: 1;
}
/* No animation — jumps from hidden to visible */
```

`display: none` removes the element from layout — there's no in-between to transition from/to. Show: transitioning `opacity` + `visibility: hidden` (takes space but invisible), using `transition-behavior: allow-discrete` with `display` (Chrome 116+), `@starting-style` for entry animation, `height: 0 → height: auto` workaround using `max-height`, and the `popover` API + `[popover]:popover-open` transitions with `@starting-style`.''',

'''**Debug Scenario:**
A developer's `z-index` stacking doesn't work as expected because elements are in different stacking contexts:

```css
.parent { position: relative; z-index: 1; }
.child  { position: absolute; z-index: 9999; }
.sibling{ position: relative; z-index: 2; } /* covers the child despite child's z-index: 9999! */
```

The `parent` creates a stacking context with `z-index: 1`. The `child` (z-index: 9999) stacks within the parent's context. The `sibling` (z-index: 2) is in the root stacking context and is compared to `parent` (z-index: 1) — sibling wins. Show: identifying stacking context creators (`z-index` + position, `transform`, `opacity < 1`, `filter`, `will-change`, `isolation: isolate`), `isolation: isolate` for creating explicit stacking contexts without `z-index`, and the DevTools Layers panel for visualizing stacking contexts.''',

'''**Debug Scenario:**
A developer's SVG icon `currentColor` doesn't pick up the parent's color because of specificity:

```tsx
// SVG loaded as <img> — currentColor doesn't work:
<img src="/icons/arrow.svg" alt="" className="text-blue-500" />

// SVG loaded inline — correct approach:
<svg className="text-blue-500" fill="currentColor">
  <path d="..." />  {/* fill="currentColor" inherits from text-blue-500 */}
</svg>
```

`<img>` loads SVG as an external resource — CSS from the host document can't reach inside. Show: using inline SVGs, `<use>` with an external sprite, CSS `mask-image: url(icon.svg)` with `background-color: currentColor` for true color control, and the Shadow DOM isolation that prevents cross-document CSS (same reason `<iframe>` CSS is isolated).''',

'''**Debug Scenario:**
A developer's `text-overflow: ellipsis` doesn't show the ellipsis on multi-line text:

```css
.truncated {
  text-overflow: ellipsis;
  overflow: hidden;
  /* Missing: white-space: nowrap — won't truncate multi-line! */
}
```

`text-overflow: ellipsis` only works for single-line overflow (requires `white-space: nowrap` to prevent wrapping). Show: adding `white-space: nowrap` for single-line truncation, the CSS multi-line truncation approach with `-webkit-line-clamp`:

```css
display: -webkit-box;
-webkit-box-orient: vertical;
-webkit-line-clamp: 3;
overflow: hidden;
```

And the newer standard `line-clamp: 3` (still in development), and `overflow: hidden + max-height` as the most compatible approach.''',

'''**Debug Scenario:**
A developer's CSS animation causes a layout shift because it animates `width` and `height`:

```css
.loading-bar {
  width: 0%;
  transition: width 1s linear;
}
.loading-bar.complete { width: 100%; }
```

Animating `width` triggers layout recalculation on every frame — 60 times/second. Show: using `transform: scaleX()` (GPU compositor — no layout): 

```css
.loading-bar { transform: scaleX(0); transform-origin: left center; transition: transform 1s linear; }
.complete     { transform: scaleX(1); }
```

And avoiding layout-triggering properties in animations (width, height, top, left, padding, margin), the Chrome DevTools "Rendering" tab for visualizing paint/layout, and the `will-change: transform` hint for promoting to GPU layer pre-animation.''',

'''**Debug Scenario:**
A developer's CSS custom property fallback doesn't work because the variable resolves to an empty string:

```css
:root { --color-brand: ; }  /* Defined but empty — NOT the same as undefined! */

.btn {
  background: var(--color-brand, blue); /* Fallback 'blue' NOT used — empty string is valid! */
  /* Result: background: ; (invalid value — element gets background: initial) */
}
```

`var(--prop, fallback)` only uses the fallback when the custom property is UNDEFINED. If it's defined but empty (or invalid for the context), the fallback is NOT used. Show: using `@property` with `initial-value` for typed custom properties (empty becomes the initial value), checking for registered vs unregistered custom properties, and setting sensible defaults at `:root` instead of empty values.''',

'''**Debug Scenario:**
A developer's `scrollbar-gutter: stable` doesn't prevent layout shift when a scrollbar appears:

```css
body {
  scrollbar-gutter: stable; /* Reserve space for scrollbar */
  /* But layout still shifts! */
}
```

`scrollbar-gutter: stable` reserves space for the scrollbar on the element it's applied to. If the page has `margin: auto` centering on `<main>`, the reserved space is on `<body>` but `<main>`'s centering recalculates when the scrollbar appears (the centering considers the full width including the gutter). Show: applying `scrollbar-gutter: stable both-edges` (reserves space on both sides, keeping content centered), using `overflow-y: scroll` (always shows scrollbar, no shift), and setting `scrollbar-gutter` on the scroll container, not a parent.''',

]

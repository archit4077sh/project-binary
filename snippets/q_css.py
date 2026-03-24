"""
snippets/q_css.py — BATCH 6: 55 brand-new CSS/Styling questions
Zero overlap with batches 1-5 archives.
"""

Q_CSS = [

"""**Task (Code Generation):**
Implement a CSS design token system using CSS custom properties with dark/light mode:

```css
:root {
  /* Primitive tokens */
  --color-blue-500: #3b82f6;
  --color-gray-900: #111827;
  --spacing-4: 1rem;

  /* Semantic tokens — light mode defaults */
  --color-background: var(--color-white);
  --color-text-primary: var(--color-gray-900);
  --color-interactive: var(--color-blue-500);
  --shadow-card: 0 1px 3px rgba(0,0,0,0.12);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-background: var(--color-gray-950);
    --color-text-primary: var(--color-gray-50);
    --shadow-card: 0 1px 3px rgba(0,0,0,0.5);
  }
}

[data-theme="dark"] { /* Manual override */ }
```

Show: the three-tier token structure (primitive → semantic → component), theme switching via `data-theme` attribute, and the TypeScript equivalent for CSS-in-JS systems (`const tokens = { background: 'var(--color-background)' }`).""",

"""**Task (Code Generation):**
Build a CSS `@layer` architecture for a scalable component library:

```css
@layer reset, base, tokens, components, utilities, overrides;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  /* Normalize browser defaults */
}

@layer base {
  body { font-family: var(--font-sans); color: var(--color-text); }
  h1, h2, h3 { font-weight: 700; line-height: 1.2; }
}

@layer components {
  .card { background: var(--color-surface); border-radius: 8px; }
  .btn  { cursor: pointer; border: none; border-radius: 4px; }
}

@layer utilities {
  .flex  { display: flex; }
  .sr-only { position: absolute; width: 1px; overflow: hidden; clip: rect(0,0,0,0); }
}
```

Show: the layer declaration order (lower layers have lower specificity), layer-free styles having the highest specificity, `@import` with `layer()`, and the practical benefit of always-safe utility overrides without `!important`.""",

"""**Task (Code Generation):**
Implement a CSS-only accordion component with smooth height animation:

```css
.accordion-item {
  overflow: hidden;
}

.accordion-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 300ms ease;
}

.accordion-item:has(.accordion-toggle:checked) .accordion-content {
  grid-template-rows: 1fr;
}

.accordion-content > div {
  overflow: hidden; /* Required: grid 0fr trick */
}
```

Show: the `grid-template-rows: 0fr → 1fr` animation trick (animates height without JavaScript), the `:has()` selector for state-driven CSS, `<input type="checkbox">` as the state toggle, the `details`/`summary` semantic alternative, and `@starting-style` for entry animations (Chrome 117+).""",

"""**Task (Code Generation):**
Build a responsive card grid with container queries and intrinsic sizing:

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr));
  gap: 1.5rem;
  container-type: inline-size;
}

@container (min-width: 600px) {
  .card { flex-direction: row; } /* Side-by-side layout when container is wide enough */
}

@container (min-width: 900px) {
  .card-title { font-size: 1.5rem; }
}
```

Show: `container-type: inline-size` vs `size`, `container-name` for targeting specific containers in nested scenarios, the `minmax(min(300px, 100%), 1fr)` intrinsic sizing trick to prevent overflow, and comparing container queries vs media queries (container = component-level, media = viewport-level).""",

"""**Task (Code Generation):**
Implement a glassmorphism card component with CSS:

```css
.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 16px;
  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

@supports not (backdrop-filter: blur(1px)) {
  .glass-card { background: rgba(255, 255, 255, 0.85); }
}
```

Show: `backdrop-filter` browser support (Safari needs `-webkit-` prefix), `@supports` feature detection for progressive enhancement, the frosted glass visual recipe (background opacity + blur + border + inset highlight), and performance considerations (`backdrop-filter` creates a compositing layer — use sparingly).""",

"""**Task (Code Generation):**
Build a CSS scroll-driven animation that reveals sections as they enter the viewport:

```css
@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

.reveal-on-scroll {
  animation: fadeSlideIn linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}
```

Show: `animation-timeline: view()` (scroll-driven animation API), `animation-range` for controlling when the animation plays relative to the element's visibility, the JavaScript `IntersectionObserver` equivalent for browsers that don't support scroll-driven animations, and `@supports (animation-timeline: scroll())` feature detection.""",

"""**Task (Code Generation):**
Implement a CSS custom checkbox and radio button with Tailwind-style focus and state management:

```css
.custom-checkbox {
  appearance: none;
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid var(--color-border);
  border-radius: 4px;
  cursor: pointer;
  transition: border-color 150ms, background-color 150ms;
  display: grid;
  place-content: center;
}

.custom-checkbox::before {
  content: '';
  width: 0.65rem;
  height: 0.65rem;
  background: var(--color-primary);
  clip-path: polygon(14% 44%, 0 65%, 50% 100%, 100% 16%, 80% 0%, 43% 62%);
  transform: scale(0);
  transition: transform 150ms ease;
}

.custom-checkbox:checked::before { transform: scale(1); }
.custom-checkbox:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
```

Show: `appearance: none` to reset browser default, the `::before` checkmark using `clip-path`, `:checked`, `:focus-visible`, `:disabled`, and `:indeterminate` states, and the `<label>` association for click area.""",

"""**Task (Code Generation):**
Build a CSS masonry layout using CSS Grid (where supported) with a column-count fallback:

```css
/* Fallback: column-count masonry */
.masonry {
  column-count: 3;
  column-gap: 1.5rem;
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: 1.5rem;
}

/* Progressive enhancement: native CSS masonry (Chrome 126+) */
@supports (grid-template-rows: masonry) {
  .masonry {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: masonry;
    align-tracks: start;
    column-gap: 1.5rem;
  }
}
```

Show: `column-count` masonry (top-to-bottom column ordering), native CSS grid masonry (`grid-template-rows: masonry` — left-to-right row ordering), the `@supports` progressive enhancement, and the JavaScript `masonry.js` library approach for full compatibility.""",

"""**Task (Code Generation):**
Implement a CSS `clamp()` fluid typography system:

```css
:root {
  /* Fluid type scale: scales between min and max viewport widths */
  --text-sm:   clamp(0.75rem,  0.7rem  + 0.25vw, 0.875rem);
  --text-base: clamp(1rem,     0.9rem  + 0.5vw,  1.125rem);
  --text-lg:   clamp(1.125rem, 1rem    + 0.6vw,  1.25rem);
  --text-xl:   clamp(1.25rem,  1.1rem  + 0.75vw, 1.5rem);
  --text-2xl:  clamp(1.5rem,   1.25rem + 1.25vw, 2rem);
  --text-4xl:  clamp(2rem,     1.5rem  + 2.5vw,  3.5rem);
}

h1 { font-size: var(--text-4xl); }
```

Show: the `clamp(min, preferred, max)` formula, calculating the `vw`-based preferred value using a linear interpolation formula, the Utopia.fyi fluid type calculator, and the benefit of fluid type vs breakpoint-based font sizes (smooth scaling, fewer media queries).""",

"""**Task (Code Generation):**
Build a CSS skeleton loading animation with content-aware shapes:

```css
.skeleton {
  --skeleton-bg: #e5e7eb;
  --skeleton-highlight: #f3f4f6;
}

.skeleton-rect,
.skeleton-circle,
.skeleton-text {
  background: linear-gradient(
    90deg,
    var(--skeleton-bg) 25%,
    var(--skeleton-highlight) 50%,
    var(--skeleton-bg) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-text  { height: 1em; border-radius: 4px; }
.skeleton-circle { aspect-ratio: 1; border-radius: 50%; }
```

Show: the shimmer gradient animation (moving highlight from right to left), dark mode variants (replacing --skeleton-bg with darker colors), and the React `<Skeleton>` component wrapper that accepts `width`, `height`, and `variant` props.""",

"""**Task (Code Generation):**
Implement a CSS `@property` declared custom property for animated gradients:

```css
@property --gradient-angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

.animated-gradient {
  background: conic-gradient(from var(--gradient-angle), #7c3aed, #3b82f6, #06b6d4, #7c3aed);
  animation: rotate-gradient 4s linear infinite;
}

@keyframes rotate-gradient {
  to { --gradient-angle: 360deg; }
}
```

Show: `@property` syntax, the `syntax` descriptor (types: `<color>`, `<length>`, `<percentage>`, `<angle>`, etc.), `inherits` and `initial-value`, why `@property` allows animating gradient angles (browsers can interpolate typed values), and `CSS.registerProperty()` as the JS equivalent.""",

"""**Task (Code Generation):**
Build a CSS scrollbar styling system that works across browsers:

```css
/* WebKit/Blink (Chrome, Safari, Edge) */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--color-surface); }
::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 100vw;
  border: 2px solid var(--color-surface); /* Creates padding effect */
}
::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }

/* Firefox */
html {
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) var(--color-surface);
}
```

Show: `scrollbar-width` Firefox API (only `auto`, `thin`, `none`), the WebKit pseudo-elements (fine-grained), no current support for consistent cross-browser custom scrollbars in standards, `overflow: overlay` as a Chrome-only alternative, and `scroll-behavior: smooth` for animated scrolling.""",

"""**Task (Code Generation):**
Implement a CSS-only tooltip with smart positioning using `calc` and CSS Anchor Positioning:

```css
/* Modern: CSS Anchor Positioning (Chrome 125+) */
.tooltip-trigger {
  anchor-name: --tooltip-anchor;
}

.tooltip {
  position: absolute;
  position-anchor: --tooltip-anchor;
  bottom: calc(anchor(top) + 8px);
  left: anchor(center);
  translate: -50% 0;
  /* Auto-flip when near viewport edge: */
  position-try: flip-block;
}
```

Also show: the legacy CSS-only approach using `:hover` + sibling combinator + `position: absolute` relative to nearest positioned parent, the `inset-area` property shorthand for anchor positioning, and the fallback for non-supporting browsers.""",

"""**Task (Code Generation):**
Build a responsive navigation that morphs from horizontal to a hamburger menu with CSS only:

```css
.nav-menu {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.hamburger-toggle { display: none; }

@media (max-width: 768px) {
  .hamburger-label  { display: block; cursor: pointer; }
  .hamburger-toggle:checked ~ .nav-menu {
    display: flex;
    flex-direction: column;
  }
  .nav-menu { display: none; }
}
```

Show: the `<input type="checkbox" id="nav-toggle"> <label for="nav-toggle">` CSS-only toggle trick, aria attributes needed for accessibility (`aria-expanded`, `aria-controls`), the CSS `@starting-style` for smooth open/close animation, and why a `<details>` / `<summary>` approach is more semantic.""",

"""**Task (Code Generation):**
Implement a multi-column text layout with balanced columns and pull quotes:

```css
.article-body {
  columns: 2;
  column-gap: 3rem;
  column-rule: 1px solid var(--color-border);
}

.pull-quote {
  column-span: all;   /* Spans across all columns */
  border-top: 2px solid var(--color-primary);
  border-bottom: 2px solid var(--color-primary);
  padding: 1.5rem 0;
  text-align: center;
  font-size: 1.5rem;
  font-style: italic;
}

.figure { break-inside: avoid; } /* Prevent image from splitting across columns */
```

Show: `column-count` vs `columns` shorthand, `column-rule` (like border between columns), `column-span: all` for spanning elements, `break-inside: avoid` and `break-before`/`break-after`, and `column-fill: balance` vs `auto`.""",

"""**Task (Code Generation):**
Build a CSS scroll-snap carousel with momentum and accessibility:

```css
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  overscroll-behavior-x: contain;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.carousel-slide {
  min-width: 100%;
  scroll-snap-align: start;
  scroll-snap-stop: always; /* Prevents fast swipe from skipping slides */
}
```

Show: `scroll-snap-type` (mandatory vs proximity), `scroll-snap-align` (start/center/end), `scroll-snap-stop: always` (prevents skipping), `overscroll-behavior-x: contain` (prevents page scroll while swiping carousel), ARIA roles (`role="region"`, `aria-roledescription="carousel"`), and keyboard navigation with JavaScript next/prev buttons.""",

# ── Debugging ─────────────────────────────────────────────────────────────────

"""**Debug Scenario:**
A developer's CSS Grid layout has an unexpected third column appearing with just two children:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-columns: 200px; /* Unintended explicit column definition! */
}
```

`grid-auto-columns` sets the size of implicitly created columns — but combined with `auto-fill`, it causes confusion. Investigation shows the items wrap unexpectedly. Show: removing `grid-auto-columns` (let `auto-fill` handle it), `auto-fill` vs `auto-fit` (auto-fill keeps empty tracks, auto-fit collapses them), and inspecting the grid with DevTools > Layout > CSS Grid overlay.""",

"""**Debug Scenario:**
A developer's flexbox layout shows items overflowing the container on mobile despite `flex-wrap: wrap`:

```css
.flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.flex-item {
  flex: 1 1 300px;     /* Min content width is 300px */
  min-width: 300px;    /* Explicit min-width doubles the constraint */
}
```

On a 280px viewport, the 300px min-width causes overflow. `flex-wrap` wraps based on the `flex-basis` but `min-width` can still cause overflow if the container is smaller than the min-width. Show: replacing `min-width: 300px` with `min-width: min(300px, 100%)` (intrinsic), using `width: min(300px, 100%)` instead of `flex-basis`, and checking the flex algorithm order (min-width is a hard constraint that overrides flex-shrink).""",

"""**Debug Scenario:**
A CSS transition is not playing when a class is added via JavaScript:

```js
element.classList.add('animated'); // adds transition property
element.style.opacity = '1';       // Changes immediately! No transition.
```

```css
.animated { transition: opacity 300ms ease; }
```

The class and the property change happen in the same browser paint frame — the browser collapses them. Show: forcing a reflow before changing the property (`element.getBoundingClientRect()` causes reflow), using `requestAnimationFrame(() => { /* change */ })`, or adding the class FIRST and the style change NEXT in separate JS tick, and the `Web Animations API` as a more reliable alternative.""",

"""**Debug Scenario:**
A developer's `position: sticky` element stops sticking halfway through a scrollable section:

```css
.sidebar {
  position: sticky;
  top: 2rem;
}
```

The sticky element "sticks" fine at the top but stops before the bottom of its parent container — sticky stops at the parent's bottom edge. The parent container ends before the viewport, so the sidebar un-sticks when the parent ends. Show: making the `.sidebar`'s parent container taller (or using `height: 100%`), removing `overflow: hidden/auto` from ancestors, and understanding that sticky only works within the parent's bounds.""",

"""**Debug Scenario:**
A CSS `calc()` expression returns an unexpected `0` in a legacy browser:

```css
.element {
  width: calc(100% - 2rem); /* Works in modern browsers */
  /* Internet Explorer 11: needs whitespace around the minus operator */
}
```

IE 11 (and some older browsers) require spaces around `calc` operators, especially `-` (minus). `calc(100%-2rem)` is parsed as `100%minus2rem` — invalid. Show: always using spaces (`calc(100% - 2rem)`), the `@supports` check for calc (`@supports (width: calc(1px + 1%)) { ... }`), and CSS custom properties with `calc` (IE 11 doesn't support custom properties at all).""",

"""**Debug Scenario:**
A developer's CSS animation is jank on mobile because it animates `width` instead of `transform`:

```css
.expanding-panel {
  width: 0;
  overflow: hidden;
  animation: expand 300ms ease-in-out forwards;
}

@keyframes expand {
  to { width: 300px; }
}
```

Animating `width` triggers layout recalculation (reflow) on every frame — expensive on mobile. Show: using `transform: scaleX()` instead (GPU-composited, no reflow), the `max-width: 0 → max-width: 300px` trick for animating height/width with transitions, and the compositor-only properties safe to animate (`transform`, `opacity`, `filter`, `will-change`).""",

"""**Debug Scenario:**
A developer's CSS custom properties don't inherit into Shadow DOM:

```css
/* Global CSS: */
:root { --primary-color: #3b82f6; }

/* Web Component Shadow DOM: */
/* Inside shadow root: */
.button { background: var(--primary-color); } /* undefined in shadow root! */
```

CSS custom properties DO inherit through Shadow DOM by default (they leak through the shadow boundary). But `--primary-color` is defined on `:root` which is outside the shadow host. Show: custom properties defined on `:root` DO inherit into Shadow DOM, the actual bug is likely that the custom property is defined on a non-ancestor element, and using `::part()` for theming Shadow DOM elements from outside.""",

"""**Debug Scenario:**
A developer's `line-clamp` CSS isn't working as expected:

```css
.description {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
```

This works in most browsers. The bug: `display: -webkit-box` conflicts with surrounding flex/grid layout (the parent uses `display: flex`). `-webkit-box` takes precedence in some browser versions. Show: wrapping the text in a separate `<div>` purely for the line-clamp, the new `line-clamp: 3` standard (without `-webkit-` prefix — Chrome 126+), and `display: -webkit-box` vs `overflow: hidden + max-height + line-height` fallback method.""",

"""**Debug Scenario:**
A developer's `z-index` value of 99999 still gets covered by another element with `z-index: 1`:

```css
.modal   { position: fixed; z-index: 99999; }
.overlay { position: relative; z-index: 1; transform: translateZ(0); }
/* The overlay covers the modal! */
```

`z-index` only works within the same stacking context. `transform: translateZ(0)` creates a new stacking context on `.overlay`, and `.modal` is inside that stacking context. Even `z-index: 99999` within a lower-priority stacking context loses to `z-index: 1` in a higher one. Show: removing the `transform` from `.overlay`, moving `.modal` to be a direct child of `<body>` (a React Portal), and identifying all stacking context creators (`transform`, `opacity < 1`, `filter`, `will-change`, `isolation: isolate`).""",

"""**Debug Scenario:**
A CSS `@media print` stylesheet isn't hiding navigation elements when printing:

```css
@media print {
  .navbar, .sidebar, .footer { display: none; }
}
```

The elements are still visible when printing. Investigation: the elements have `display: flex !important` in the main stylesheet — `!important` wins over `@media print` rules. Show: adding `!important` to the print styles (`display: none !important;`), using `@layer` to give print styles higher priority, and checking that the stylesheet is properly loading with `<link media="all">` (not `media="screen"`).""",

"""**Debug Scenario:**
A developer's CSS animation using `steps()` shows frames in the wrong order on iOS Safari:

```css
.sprite-animation {
  width: 64px;
  height: 64px;
  background-image: url('sprites.png');
  animation: walk 1s steps(8, end) infinite;
}

@keyframes walk {
  from { background-position: 0 0; }
  to   { background-position: -512px 0; }
}
```

On iOS Safari, `background-position` animation with `steps()` may have off-by-one errors. Show: using `steps(8, start)` vs `steps(8, end)` (start shows frame 1 immediately, end shows frame 0 first then jumps), switching to CSS Grid animation with `will-change: transform` using actual `<img>` frames, and the `animation-fill-mode: both` interaction with `steps`.""",

"""**Debug Scenario:**
A developer's CSS variables defined in a component stylesheet don't apply when the component is used in a different context:

```css
/* button.css */
.btn {
  --btn-bg: var(--color-primary, #3b82f6);
  background: var(--btn-bg);
}
```

The `--color-primary` variable fallback correctly uses `#3b82f6`. But in a dark theme context where `--color-primary` is `#93c5fd` (lighter blue), the button doesn't update. Investigation: the component CSS is loaded before the theme CSS, but variable resolution is lazy (`var()` resolves at paint time with inherited values). Show: variable resolution is actually correct — check that `--color-primary` is defined on an ancestor element (not just `:root` if the component renders outside the body).""",

"""**Debug Scenario:**
A developer's CSS `object-fit: cover` on an `<img>` causes the image to be positioned incorrectly — always showing the top of the image instead of the center:

```css
img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  /* No object-position specified — defaults to 50% 50% (center) */
}
```

The image IS centered (default `object-position: 50% 50%`). The bug is actually that the `<img>` has `vertical-align: top` from reset CSS that changes the baseline, visually appearing like top-aligning. Show: this is a diagnosis exercise — checking the actual vs perceived alignment, using `object-position: center top` for intentional top framing, and the editorial control of `object-position: 0% 20%` to show the subject of a portrait photo.""",

"""**Debug Scenario:**
A developer's CSS `backdrop-filter` isn't working on a modal overlay:

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  backdrop-filter: blur(8px);
  background: rgba(0, 0, 0, 0.3);
}
```

The blur isn't visible. Investigation: the parent container of `.modal-overlay` has `overflow: hidden`, which clips the backdrop-filter region. Show: removing `overflow: hidden` from ancestors, using `-webkit-backdrop-filter` for Safari alongside `backdrop-filter`, and the browser support check (`@supports (backdrop-filter: blur(1px))`). Also note that `backdrop-filter` blurs content BEHIND the element — if the element has an opaque background, the blur is invisible.""",

"""**Debug Scenario:**
A developer's CSS custom property value with a space is rejected when used in a `calc()`:

```css
:root {
  --spacing: 1rem;         /* Works */
  --col-count: 3;          /* Works in calc */
  --border: 1px solid red; /* Complex value — not usable in calc */
}

.element {
  width: calc(100% / var(--col-count)); /* Works */
  border: var(--border);               /* Works — used as full property value */

  /* Bug attempt: */
  width: calc(var(--spacing) * var(--col-count));
  /* '1rem * 3' = invalid — can't multiply two non-number values */
}
```

Show: the correct usage — `calc(var(--spacing) * 3)` works (unitless number × length), `calc(3 * var(--spacing))` also works, but `var(--col-count)` must be unitless and `var(--spacing)` must be a length — can't multiply two `<length>` values, and `@property { syntax: '<integer>'; }` for typed custom properties.""",

"""**Debug Scenario:**
A CSS Grid auto-placement algorithm creates unexpected holes in the grid:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-flow: row;
}

.wide-item {
  grid-column: span 3; /* Takes 3 columns */
}
```

When a 3-wide item can't fit in the current row (only 2 slots left), the browser leaves those 2 slots empty and places the item on the next row — creating holes. Show: `grid-auto-flow: row dense` which fills holes by moving smaller items into gaps, the explicit placement alternative (`grid-column: 1 / span 3` to always start at column 1), and DevTools grid overlay to visualize the auto-placement algorithm.""",

"""**Debug Scenario:**
A developer's `aspect-ratio` CSS property causes a jump in layout when the image loads:

```css
.image-container {
  aspect-ratio: 16 / 9;
  background: #e5e7eb; /* Placeholder color */
}

img {
  width: 100%;
  height: auto;
  object-fit: cover;
}
```

The container has `aspect-ratio: 16/9` and the image has `height: auto`. When the image loads, it overrides the container's height because the `<img>` element's intrinsic aspect ratio conflicts with the parent's `aspect-ratio`. Show: setting `height: 100%` on the `<img>` inside the ratio-locked container, the `width` and `height` HTML attributes on `<img>` (tells browser the intrinsic ratio before the image loads), and why this doesn't cause CLS.""",

"""**Debug Scenario:**
A developer's Tailwind CSS purging removes used classes in production:

```tsx
// Dynamic class names — WRONG:
const color = condition ? 'text-red-500' : 'text-green-500';
<div className={`text-${color}`}> // Tailwind can't detect this!

// Correct: use full class names:
const color = condition ? 'text-red-500' : 'text-green-500';
<div className={color}>
```

Tailwind's purge (now: content) scans for class name strings. Template literals with partial class names (`text-${color}`) aren't recognized. Show: using full class names in conditionals, the `safelist` config option for dynamic class names, `clsx`/`cn` utility for conditional class merging, and the Tailwind `content` configuration to include all template files.""",

"""**Debug Scenario:**
A developer's CSS `transition` on `display` doesn't work (toggling `display: none` is always instant):

```css
.menu {
  display: none;
  opacity: 0;
  transition: opacity 300ms ease;
}

.menu.open {
  display: block;
  opacity: 1;
  /* But the transition doesn't play! display change is instant */
}
```

`display` is not animatable — switching from `none` removes the element from rendering immediately, preventing the opacity transition from playing. Show: the `visibility: hidden` + `opacity: 0` approach (visibility is animatable with `transition-delay`), the `@starting-style` rule (Chrome 117+) for transition-on-first-paint, `max-height: 0 → max-height: 999px` trick, and the Web Animations API `element.animate()` for programmatic control.""",

"""**Debug Scenario:**
A developer's responsive image `<picture>` is not switching sources at the expected breakpoint:

```html
<picture>
  <source srcset="image-mobile.jpg" media="(max-width: 768px)">
  <img src="image-desktop.jpg" alt="Hero">
</picture>
```

On a 600px viewport, the desktop image loads instead of mobile. Investigation: the browser has already downloaded the desktop image from cache (previous larger viewport), or the `media` query doesn't match because the viewport DPR is factored in. Show: adding `type` and `sizes` attributes for resolution-aware loading, the `<picture>` element's image selection priority (format first, then media), and verifying the media query matches using DevTools device simulation.""",

"""**Debug Scenario:**
A developer's SVG icon inherits the wrong color when used inline:

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path d="..." fill="#000000" /> <!-- Hardcoded black! -->
</svg>
```

The SVG path has a hardcoded `fill="#000000"` attribute which overrides CSS `color` inheritance. Show: replacing `fill="#000000"` with `fill="currentColor"` so the SVG path inherits the parent's CSS `color` value (`<path fill="currentColor">`), using `svg { color: inherit; }` in CSS, and the SVG sprite approach (`<use href="#icon-name">`) for reusable icons with CSS theming.""",

"""**Debug Scenario:**
A developer's `@font-face` declaration causes invisible text (FOIT) for 3 seconds on slow connections:

```css
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  /* No font-display — defaults to 'auto' (browser-specific, often FOIT) */
}
```

Without `font-display`, Chrome defaults to a 3-second block period (invisible text while loading). Show: adding `font-display: swap` (flash of unstyled text then swap — best for body text), `font-display: optional` (load font from cache only, fallback if not cached — best for performance), `font-display: fallback` (100ms block, then fallback), and `rel="preload"` for critical fonts.""",

"""**Debug Scenario:**
A developer's CSS `text-overflow: ellipsis` isn't showing the ellipsis on a flex child:

```css
.flex-parent { display: flex; }

.flex-child {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  /* No width or max-width — flex child grows! */
}
```

`text-overflow: ellipsis` requires the element to have a constrained width (`overflow: hidden` alone isn't sufficient if the element can grow). In a flex container, the child grows to accommodate content. Show: adding `min-width: 0` to the flex child (overrides the default `min-width: auto` which prevents shrinking), or `max-width: 100%`, and why `min-width: 0` is the standard fix for `text-overflow` in flex containers.""",

"""**Debug Scenario:**
A developer's CSS `filter: drop-shadow()` on a PNG image creates a shadow around the entire rectangular bounding box instead of the image shape:

```css
.icon {
  filter: drop-shadow(2px 4px 8px rgba(0,0,0,0.3));
}
```

Actually, `drop-shadow()` DOES create shadows around the actual pixel shape (including transparent areas of a PNG). The real bug: the developer used `box-shadow` instead:

```css
.icon {
  box-shadow: 2px 4px 8px rgba(0,0,0,0.3); /* Box shadow — follows bounding box! */
}
```

Show: `filter: drop-shadow()` vs `box-shadow` behavior difference, `filter: drop-shadow` following the alpha channel of the element including child elements, and using `drop-shadow` on SVGs (works per-path, not per bounding box).""",

"""**Debug Scenario:**
A developer's CSS Grid layout produces different results in Safari vs Chrome for auto-placement with named grid areas:

```css
.grid {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main";
  grid-template-columns: 200px 1fr;
}

.content { grid-area: main; }
/* In Safari, content ends up in the wrong cell */
```

Safari has historically had differences in grid area name resolution, especially with hyphenated names (`grid-area: main-content` vs `grid-area: main`). Show: verifying grid area names match exactly in `template-areas` and `grid-area` declarations, using `grid-column` and `grid-row` as explicit alternatives (more verbose but unambiguous), and testing with the CSS Grid inspector in Safari's Web Inspector.""",

"""**Debug Scenario:**
A developer's `animation-fill-mode: forwards` causes elements to disappear when applying an exit animation:

```css
.element {
  animation: fadeOut 300ms ease forwards;
}

@keyframes fadeOut {
  from { opacity: 1; }
  to   { opacity: 0; }
}
```

After the animation, `forwards` keeps the element at `opacity: 0` (the last keyframe state) — the element is invisible but still takes up space in the layout. Show: removing the element with JavaScript after the animation ends (`element.addEventListener('animationend', () => element.remove())`), using `visibility: hidden` instead of `opacity: 0` in the final keyframe (also preserves space but makes the element non-interactive), and `display: none` removal.""",

"""**Debug Scenario:**
A developer's CSS scroll behavior is inconsistently smooth across browsers after setting `scroll-behavior: smooth`:

```css
html { scroll-behavior: smooth; }
```

Smooth scrolling works in Chrome but not in iOS Safari (partial support). Also, `prefers-reduced-motion` users should not get smooth scrolling. Show: respecting `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: no-preference) {
  html { scroll-behavior: smooth; }
}
```

Show: the JavaScript `window.scrollTo({ behavior: 'smooth' })` equivalent, the `scroll-behavior: smooth` support table (Safari 15.4+ for CSS), and when to use JavaScript `scrollIntoView({ behavior: 'smooth' })` for programmatic smooth scrolling with reduced-motion support.""",

"""**Debug Scenario:**
A developer notices their CSS specificity is unexpectedly high because of auto-generated class names:

```css
/* CSS Modules generate: */
.button__primary--large { background: blue; }  /* specificity: 0-1-0 */

/* But the following override doesn't work: */
.button-override { background: red !important; }

/* The problem: both have (0,1,0) specificity, and !important escalates */
```

Actually `!important` SHOULD win here. The real bug is a common specificity issue in CSS Modules where the same component is styled in multiple places. Show: the correct specificity comparison, using `@layer` to manage CSS Module specificity, the CSS Modules `:global` escape hatch for overrides, and why `!important` in CSS Modules should be avoided (it escalates to the `!important` cascade layer).""",

"""**Debug Scenario:**
A developer's CSS `transform: rotate()` causes a blurry rendering of text on retina displays:

```css
.card {
  transform: rotate(15deg); /* Text inside becomes blurry on high-DPI */
}
```

CSS transforms can cause sub-pixel rendering of text, especially at non-90deg angles. On Retina displays, diagonal transforms cause anti-aliasing artifacts. Show: using `transform: rotate(15deg) translateZ(0)` to promote to GPU layer (may help), `-webkit-font-smoothing: antialiased` and `-moz-osx-font-smoothing: grayscale` for text within transforms, rounding transforms to multiples of 90deg where possible, and accepting that diagonal text rotation will always have some anti-aliasing.""",

"""**Debug Scenario:**
A developer's CSS custom property containing a `url()` value fails in Firefox:

```css
:root {
  --icon-url: url('/icons/arrow.svg');
}

.element::before {
  content: var(--icon-url); /* Works in Chrome, fails in Firefox */
}
```

Firefox has stricter CSS custom property value handling — `url()` values in custom properties behave differently, especially when used in `content`. Show: using the `url()` directly in `content` rather than via a custom property, using a background-image approach instead (`background-image: var(--icon-url)` works in Firefox), and the `@property` declaration with `syntax: '<url>'` for typed URL custom properties.""",

"""**Debug Scenario:**
A developer uses `vh` units for a mobile full-screen layout but the layout breaks when the address bar shows/hides:

```css
.hero { height: 100vh; } /* 100vh includes browser chrome on mobile! */
```

On mobile, `100vh` is computed when the page loads (including the address bar), but the address bar hides when scrolling — causing the hero to be taller than the visible area, then shorter when the bar hides. Show: using `height: 100dvh` (dynamic viewport height — changes as browser UI shows/hides), `svh` (small viewport height — always includes browser UI), `lvh` (large viewport height — excludes browser UI), and the fallback for older browsers (`height: 100vh; height: 100dvh`).""",

]

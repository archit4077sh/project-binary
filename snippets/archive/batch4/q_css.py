"""
snippets/q_css.py — BATCH 4: 28 brand-new CSS/Styling questions
Zero overlap with batch1, batch2, or batch3 archives.
"""

Q_CSS = [

"""**Task (Code Generation):**
Implement a CSS-only accessible tooltip using the `popover` API (no JavaScript):

```html
<button popovertarget="my-tooltip" popovertargetaction="show">Hover for info</button>
<div id="my-tooltip" popover>This is the tooltip content</div>
```

Show: the Popover API's `popover` attribute (auto/manual), `popovertarget` binding, CSS `:popover-open` pseudo-class for styling the open state, `::backdrop` for manual popovers, anchoring the tooltip relative to the trigger using CSS `anchor-name` and `anchor()` (experimental), and `@supports (anchor-name: --foo)` fallback to traditional CSS positioning.""",

"""**Debug Scenario:**
A component library uses `:focus` styles for keyboard navigation but users report seeing focus rings on mouse clicks. Non-keyboard users find the focus rings distracting.

```css
button:focus { outline: 3px solid blue; } /* shows on mouse click too */
```

Show: replacing `:focus` with `:focus-visible` (only shows focus ring for keyboard navigation, not mouse/touch), the browser heuristic for when `:focus-visible` applies (keyboard events, programmatic focus on text inputs), the `focus-visible` polyfill for older browsers, and why removing focus styles entirely (`:focus { outline: none }`) is an accessibility violation under WCAG 2.1 AA.""",

"""**Task (Code Generation):**
Build a CSS design token system using CSS Houdini's `@property` for animatable custom properties:

```css
@property --brand-hue {
  syntax: '<number>';
  inherits: false;
  initial-value: 265;
}

@property --progress {
  syntax: '<percentage>';
  inherits: false;
  initial-value: 0%;
}

/* Now can animate: */
.button { transition: --brand-hue 0.3s ease; }
.button:hover { --brand-hue: 280; }
```

Show: `@property` for numeric, color, percentage, and length types, how registered properties enable animated custom properties (unregistered custom properties can't be animated), the `animation` shorthand on a registered property, and browser support with `@supports (syntax: '<color>')`.""",

"""**Debug Scenario:**
A `<Modal>` component positioned with `position: fixed` is clipped by a parent element with `transform: translateX(0)`, meaning it doesn't overlay the full screen:

```css
.sidebar { transform: translateX(0); /* or any transform */ }
.sidebar .modal { position: fixed; /* clipped to sidebar! */ }
```

`position: fixed` normally positions relative to the viewport. But if any ancestor has `transform`, `perspective`, `filter`, or `will-change: transform`, it creates a new containing block — `position: fixed` becomes relative to that element.

Show: the solution of rendering the modal in a `<Portal>` (via `createPortal`) into `document.body`, why this escapes the transformed ancestor, and the same issue with `position: sticky` (also affected by transformed ancestors).""",

"""**Task (Code Generation):**
Implement a fluid typography system using CSS `clamp()` and viewport units:

```css
:root {
  /* Fluid: scales from 16px @ 320px viewport to 20px @ 1440px viewport */
  --font-body: clamp(1rem, calc(0.9rem + 0.5vw), 1.25rem);
  
  /* Heading scales from 32px to 72px */
  --font-h1: clamp(2rem, calc(1.5rem + 2.5vw), 4.5rem);
}
```

Show: the `clamp(min, preferred, max)` formula derivation (preferred = `m*vw + b` where m calculates slope and b calculates intercept), a Sass mixin that generates the clamp from `minSize`, `maxSize`, `minWidth`, `maxWidth` parameters, the accessibility consideration that users who zoom can override viewport-based `vw` units (use `rem` as the base), and the `font-size-adjust` property for cross-font comparisons.""",

"""**Debug Scenario:**
A CSS Grid layout with `grid-template-columns: 1fr 1fr 1fr` renders three equal columns. After adding a 4th item, it wraps below but takes up the full width (stretching to fill the 3-column row). The developer wants the 4th item to be 1/3 width:

```css
.grid { display: grid; grid-template-columns: 1fr 1fr 1fr; }
/* Item 4 wraps and stretches to full width of the implicit row */
```

Implicit rows still use `1fr` per column — so item 4 sitting alone in the 3rd implicit row stretches to fill 3/3 of available space (since there's no sibling in the row to share it). Show: using `justify-items: start` to prevent stretching, using `grid-auto-columns` to set the width of implicit columns, and the `grid-template: repeat(...)` explicit placement alternative.""",

"""**Task (Code Generation):**
Build a responsive sidebar layout that transitions between overlay (mobile) and fixed (desktop) modes using CSS only:

```css
/* Mobile: sidebar overlays content */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    transform: translateX(-100%); /* hidden off-screen */
    transition: transform 0.3s ease;
  }
  .sidebar.open { transform: translateX(0); }
  .backdrop { display: block; } /* clicking closes sidebar */
}

/* Desktop: sidebar is always visible, content flows beside it */
@media (min-width: 769px) {
  .layout { display: grid; grid-template-columns: 280px 1fr; }
}
```

Show: the complete layout CSS, the CSS `:has()` technique to toggle `open` class without JavaScript (`nav:has(:checked) .sidebar { transform: translateX(0) }`), the backdrop overlay, and smooth focus management when opening/closing.""",

"""**Debug Scenario:**
A developer applies `animation-fill-mode: forwards` to keep the end state of an animation:

```css
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.element { animation: fadeIn 0.5s ease forwards; }
```

The element stays visible after the animation. But later, trying to apply `opacity: 0` with inline style doesn't hide it — the animation value overrides the inline style.

CSS animations have higher cascade precedence than styles without `!important`. Show: removing `animation-fill-mode: forwards` and instead setting the initial opacity via class toggle (no animation override issue), using `animation-fill-mode: none` and then adding a CSS class to maintain the end state, and the `style.animation = ''` JavaScript reset to release the animation.""",

"""**Task (Code Generation):**
Implement a CSS custom property-based theming system with runtime theme generation from a brand color:

```ts
// Given a single brand hex color, generate a full theme:
function applyBrandTheme(brandColor: string) {
  const hsl = hexToHsl(brandColor);
  document.documentElement.style.setProperty('--brand-h', String(hsl.h));
  document.documentElement.style.setProperty('--brand-s', `${hsl.s}%`);
  document.documentElement.style.setProperty('--brand-l', `${hsl.l}%`);
}
```

Show: the CSS custom property architecture where all semantic tokens derive from `--brand-h`, `--brand-s`, `--brand-l`:
- `--color-primary: hsl(var(--brand-h) var(--brand-s) var(--brand-l))`
- `--color-primary-light: hsl(var(--brand-h) var(--brand-s) calc(var(--brand-l) + 20%))`
- `--color-on-primary: hsl(var(--brand-h) 10% 98%)` (for text on primary background)

And the contrast ratio check to ensure WCAG AA compliance.""",

"""**Debug Scenario:**
A developer uses `word-break: break-all` to prevent text overflow in a card component. All text wraps correctly, but URLs in the text wrap in strange places:

```
https://www.example.com/
very-long-path/that/sho
uld-wrap-nicely
```

`break-all` breaks at any character position. `overflow-wrap: break-word` is more appropriate — it only breaks words that would overflow (leaves normal word boundaries intact). Show: `overflow-wrap: break-word` (old: `word-wrap: break-word`), the difference from `word-break: break-word` (non-standard, same as break-all in most browsers), `hyphens: auto` for grammatically correct line breaks with soft hyphens, and the combination that handles both long URLs and text gracefully.""",

"""**Task (Code Generation):**
Build an accessible color contrast checker component:

```tsx
<ContrastChecker
  foreground="#ffffff"
  background="#6366f1"
  sizes={['normal', 'large', 'ui']}
/>
// Output:
// Contrast ratio: 4.54:1
// Normal text (4.5:1): ✓ AA | ✗ AAA
// Large text (3:1):  ✓ AA | ✓ AAA
// UI components (3:1): ✓ AA
```

Show: the WCAG relative luminance formula (linearize sRGB, weight by perception: R×0.2126, G×0.7152, B×0.0722), the contrast ratio formula `(L1 + 0.05) / (L2 + 0.05)`, WCAG AA vs AAA thresholds, and a color picker that suggests darker/lighter variants to achieve the required contrast ratio.""",

"""**Debug Scenario:**
A CSS grid item uses `place-self: center` to center itself within its grid cell. On Firefox, it appears centered. On Chrome, it's stretched to fill the cell.

Investigation reveals the grid item is a `<div>` with `display: flex`. When a flex container is a grid item, `align-self: stretch` (the default) overrides `place-self: center` in Chrome's older rendering engine.

Show: explicitly setting `align-self: center` and `justify-self: center` separately (instead of `place-self`), why the shorthand behaves inconsistently across versions, and `width: fit-content; height: fit-content` as a robust alternative that doesn't rely on grid self-alignment.""",

"""**Task (Code Generation):**
Implement a CSS scroll-driven animation — a reading progress bar:

```css
@keyframes grow-progress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--brand-primary);
  transform-origin: left;
  animation: grow-progress linear;
  animation-timeline: scroll(root block);
}
```

Show: the `animation-timeline: scroll()` syntax, `scroll(root block)` for the document root's block (vertical) scroll axis, `view()` timeline for element-in-viewport animations, `animation-range: entry 0% entry 100%` for playing an animation as an element enters the viewport, and `@supports (animation-timeline: scroll())` fallback using a JavaScript `IntersectionObserver` + CSS variable update.""",

"""**Debug Scenario:**
A developer creates a CSS animation but `animation-play-state: paused` set from JavaScript doesn't pause it. The animation continues running:

```ts
element.style.animationPlayState = 'paused'; // doesn't work
```

Investigation shows the animation is defined in a CSS class, and inline styles have lower specificity than `!important` rules in the stylesheet that override `animation-play-state`.

Actually, inline styles have HIGHER specificity than class rules. The real issue is the property name — JavaScript uses camelCase: `animationPlayState`, not kebab-case. Show: `element.style.animationPlayState = 'paused'` (correct camelCase), how `getComputedStyle(element).animationPlayState` reads the current value, and toggling via CSS class vs inline style (the class approach requires `!important` in the class rule to beat inline styles).""",

"""**Task (Code Generation):**
Build a CSS-only accessible mega-menu with keyboard navigation:

```html
<nav aria-label="Main Navigation">
  <ul role="menubar">
    <li role="none">
      <button role="menuitem" aria-haspopup="true" aria-expanded="false">Products</button>
      <div role="menu" aria-label="Products Submenu">
        <a role="menuitem" href="/web">Web Apps</a>
        <a role="menuitem" href="/mobile">Mobile Apps</a>
      </div>
    </li>
  </ul>
</nav>
```

Show: `:focus-within` for opening the mega-menu when any child has focus, CSS transitions for smooth open/close, keyboard navigation implementation via JavaScript (arrow keys, Escape to close, Tab order), proper ARIA states (`aria-expanded`, `aria-haspopup`), and why using the HTML `<details>`/`<summary>` elements is a simpler accessible alternative.""",

"""**Debug Scenario:**
A developer uses CSS custom properties for a dark/light theme switch. The `prefers-color-scheme` media query works correctly on initial load, but the JavaScript theme toggle doesn't change the custom property values immediately — there's a 1-frame flicker:

```ts
document.documentElement.classList.toggle('dark-mode');
// Takes ~1 frame to apply — causes visible flash
```

Adding/removing a class causes a style recalculation. The CSS custom property transition is triggered but the browser batches style changes. Show: using `document.startViewTransition(() => document.classList.toggle('dark'))` for a smooth theme transition using the View Transition API, a CSS `::view-transition-*` rule to customize the theme-switch animation, and disabling the transition for users with `prefers-reduced-motion`.""",

"""**Task (Code Generation):**
Implement a CSS masonry layout (before native CSS masonry is available cross-browser):

```css
/* Option 1: CSS columns (column masonry) */
.masonry-columns {
  columns: 3;
  column-gap: 1rem;
}
.masonry-item { break-inside: avoid; margin-bottom: 1rem; }

/* Option 2: Grid + JavaScript height measurement */
.masonry-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 1px; /* fine grain for span calculation */
}
```

Show: the CSS columns approach (items flow column-by-column, not row-by-row), the JavaScript grid span approach (`grid-row: span N` where N = itemHeight / rowGap), and the native `grid-template-rows: masonry` experimental syntax (behind flag in Firefox), with feature detection to use native when available.""",

"""**Debug Scenario:**
A CSS module has a style that works in development (Webpack dev server) but not in production (Vite build):

```css
/* button.module.css */
:global(.primary-theme) .button { background: blue; } /* works in dev, breaks in prod */
```

Vite uses Lightning CSS (not PostCSS) for production CSS processing. `:global()` is a CSS Modules syntax for opting out of scoping — Lightning CSS processes it differently. In production output, the rule becomes `.primary-theme .button_abc123` instead of `.primary-theme .button`.

Show: the correct CSS Modules syntax for global ancestor selectors (`@global { ... }` or `.button:global(.active)`), the Vite config to ensure CSS Modules settings match between dev and production, and using `composes` for cross-file class composition as an alternative.""",

"""**Task (Code Generation):**
Build a CSS animation library with 12 entrance animations as CSS classes:

```css
.animate-fade-in     { animation: fadeIn 0.4s ease forwards; }
.animate-slide-up    { animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.animate-zoom-in     { animation: zoomIn 0.3s ease forwards; }
.animate-bounce-in   { animation: bounceIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }
```

Show: the 12 `@keyframes` definitions (fade, slide up/down/left/right, zoom, bounce, flip, rotate, blur, shake, heartbeat), CSS custom properties for `--duration` and `--delay` overrides, `prefers-reduced-motion` reducing all animations to simple opacity fade, and the `data-animate="in-view"` attribute pattern using Intersection Observer to apply the animation class when the element enters the viewport.""",

"""**Debug Scenario:**
A design system uses CSS logical properties (`margin-block-start`, `padding-inline`) for internationalization (RTL language support). In Safari 14, the properties are not recognized and margins are applied incorrectly.

Show: the Safari 14 support timeline for CSS logical properties (shipped in Safari 15), a PostCSS plugin (`postcss-logical`) that transforms logical properties to physical fallbacks for older Safari, the `@supports (margin-block: 0)` feature detection to progressively enhance, and `writing-mode: horizontal-tb` (the default, where logical and physical properties produce identical results) vs `writing-mode: vertical-rl` where logical properties shine.""",

"""**Task (Code Generation):**
Implement a glassmorphism card component with correct browser support:

```css
.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}
```

Show: the `@supports (backdrop-filter: blur(1px))` check with a solid background fallback for Firefox, the performance warning (`backdrop-filter` triggers GPU compositing — avoid on frequently-repainting elements), and why glassmorphism requires a colorful and textured background behind the card to look good (using a CSS gradient background or blurred image).""",

"""**Debug Scenario:**
A developer sets an SVG icon's `fill` to `currentColor` but in Safari, the icon appears black even though the surrounding text is white:

```html
<button style="color: white">
  <svg viewBox="0 0 24 24">
    <path fill="currentColor" d="..." />
  </svg>
  Label
</button>
```

In Safari, `currentColor` works correctly. The issue is the SVG file was pasted with an explicit `fill="black"` attribute on the `<svg>` element that overrides the `fill="currentColor"` on `<path>`:

```html
<svg viewBox="0 0 24 24" fill="black"> <!-- overrides path's fill -->
```

Show: removing the explicit `fill` attribute from the `<svg>` parent, setting `fill="inherit"` on the SVG root as a CSS-agnostic fix, and linting SVG files with a custom ESLint rule that warns about hardcoded `fill` values.""",

"""**Task (Code Generation):**
Build a responsive CSS timeline component:

```html
<ol class="timeline">
  <li class="timeline-item timeline-item--left">
    <div class="timeline-marker"></div>
    <div class="timeline-content"><h3>2020</h3><p>Founded</p></div>
  </li>
  <li class="timeline-item timeline-item--right">...</li>
</ol>
```

Show: the CSS Grid timeline (center line using a grid column, alternating left/right placement), the vertical line using `::before` on `.timeline` (`position: absolute; left: 50%; width: 2px`), the animated marker circles using `::before` with `scale()` transition on hover, mobile layout where all items are on one side, and `@media (prefers-reduced-motion)` disabling timeline animations.""",

"""**Debug Scenario:**
A table component has `position: sticky` headers. When the user scrolls, the sticky header works but text in the header appears semi-transparent — the table rows below are visible through the header:

```css
thead th {
  position: sticky;
  top: 0;
  background: white; /* should block rows below */
}
```

The style looks correct. Investigation reveals the `<table>` has `border-collapse: collapse` set. `border-collapse: collapse` removes rounded borders but also prevents the sticky cell from creating its own stacking context for background painting — in older browsers and some edge cases, this causes background rendering artifacts.

Show: switching to `border-collapse: separate; border-spacing: 0` (same visual result, fixes sticky background), adding `z-index: 1` to sticky headers, and the CSS `isolation: isolate` workaround.""",

"""**Task (Code Generation):**
Implement a CSS-first form validation styling without JavaScript using `:has()`:

```css
/* Real-time validation using :has() and :invalid */
.form-group:has(:invalid:not(:placeholder-shown)) .error-message {
  display: block; /* show error only after user has typed (not :placeholder-shown) */
}

.form-group:has(:valid) .success-icon {
  display: block;
}

input:invalid:not(:placeholder-shown) {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}
```

Show: HTML5 native validation attributes (`required`, `pattern`, `minlength`, `type="email"`), the `:placeholder-shown` trick to detect untouched inputs, `:has()` for parent-conditional styling (show error in the parent `.form-group` when child input is invalid), and the submit button state: `form:invalid button[type="submit"] { opacity: 0.5; cursor: not-allowed; }`.""",

"""**Debug Scenario:**
A developer adds `transition: all 0.3s ease` to a component for convenience but reports React performance issues — every state update causes long paints.

`transition: all` transitions EVERY animatable CSS property, including `opacity`, `transform`, `width`, `height`, and also `max-height`, `padding`, `margin`, `color`, etc. Even trivial state changes that trigger class updates cause full transition computations.

Show: listing only the specific properties needed (`transition: opacity 0.3s ease, transform 0.3s ease`), categorizing CSS properties by transition cost (composited: `opacity`, `transform` — GPU composited; layout-triggering: `width`, `height`, `padding` — expensive; paint-triggering: `color`, `background` — medium), and Chrome DevTools Performance panel for diagnosing paint/composite times.""",

"""**Task (Code Generation):**
Implement a CSS `field-sizing: content` textarea that auto-grows to fit its content:

```css
/* Modern approach (Chrome 123+): */
textarea {
  field-sizing: content;      /* auto-grows with content */
  min-height: 3rem;
  max-height: 20rem;
  overflow-y: auto;           /* scroll when max-height reached */
  resize: none;               /* disable manual resize since it auto-sizes */
}

/* Fallback for browsers without field-sizing: */
@supports not (field-sizing: content) {
  textarea { height: auto; }
}
```

Show: the `field-sizing: content` specification, the JavaScript fallback that measures `scrollHeight` and sets `height` explicitly on `input` event (`textarea.style.height = auto; textarea.style.height = textarea.scrollHeight + 'px'`), why `height: auto` must be set before measuring `scrollHeight` (to collapse before measuring), and `@supports` for progressive enhancement.""",

"""**Debug Scenario:**
A CSS `container query` doesn't trigger when the container's size changes. The developer wrote:

```css
.sidebar { container-type: inline-size; }

@container (min-width: 300px) {
  .card { display: grid; } /* doesn't trigger */
}
```

The `.card` element is a direct child of `.sidebar`. Investigation shows `.sidebar` has `width: 100%` and its parent `<main>` has `display: flex`. The container query responds to the CONTAINER element's size — `.sidebar`'s computed width. The parent `<main>` has `overflow: hidden` which clips the sidebar to 0px in one layout variation.

Show: the debugging approach using browser DevTools' Container Query overlay, verifying the container's computed size with `getComputedStyle(sidebar).inlineSize`, fixing the parent overflow issue, and the difference between `container-type: inline-size` (only inline dimension) vs `container-type: size` (both dimensions).""",

]

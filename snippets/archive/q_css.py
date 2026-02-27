"""
snippets/q_css.py - 28 CSS/Styling questions
"""

Q_CSS = [

"""**Context:**
We're migrating from CSS Modules to CSS-in-JS (styled-components) in our dashboard. The migration is incremental -- some components use styled-components, others still use CSS Modules.

**Observed Issue:**
Components using styled-components generate runtime class names that occasionally conflict with static CSS Module class names when both systems are active simultaneously. The cascade order is unpredictable.

**Specific Ask:**
How do you safely run CSS-in-JS and CSS Modules simultaneously during an incremental migration? Is CSS @layer the mechanism that gives you deterministic cascade ordering between the two systems? What's the correct migration order to minimize conflicts -- migrate leaf components first or page-level components?""",

"""**Context:**
Our DataTable has sticky first column and sticky header row. The sticky column needs to show a subtle drop shadow when the table is scrolled horizontally.

**Observed Issue:**
We apply box-shadow to the sticky column. The shadow is clipped to the table cell's box -- it doesn't visually overlay the adjacent scrolling cell as expected. overflow: hidden on the parent clips the shadow.

**Specific Ask:**
How do you apply a custom scroll-position-dependent shadow to a sticky element without box-shadow being clipped? Is a ::after pseudo-element with opacity transition the right approach? Can CSS scroll-driven animations (@keyframes with animation-timeline: scroll()) eliminate the JavaScript scroll listener approach?""",

"""**Context:**
We need to detect when a card component exceeds its container width and apply an overflow layout. Currently this is done with a ResizeObserver in JavaScript that adds a data attribute.

**Observed Issue:**
The JS ResizeObserver approach adds a frame of layout shift before the compact layout applies, causing visual flicker.

**Specific Ask:**
Does CSS Container Queries (@container, inline-size) eliminate the need for ResizeObserver-based layout switching? At what browser support level is it safe to ship @container queries for a B2B SaaS without a polyfill? What's the fallback strategy for browsers that don't support @container?""",

"""**Context:**
Our design system uses CSS custom properties (variables) for design tokens. The theme (light/dark) is switched by swapping a data-theme attribute on the root element.

**Observed Issue:**
Our CSS variables are defined in separate light.css and dark.css files. When the data-theme switches, there's a 1-frame flash before the browser repaints with the new theme values.

**Specific Ask:**
Is the 1-frame theme flash inherent to class/attribute-based CSS custom property switching, or is there a mechanism to make theme changes synchronous with the attribute change? Does defining both themes in a single stylesheet with [data-theme='dark'] selectors eliminate the flash vs. loading separate CSS files?""",

"""**Context:**
We're building a complex dashboard grid layout: a fixed sidebar, a top navigation, and a scrollable content area. The content area has a sub-grid for responsive widget placement.

**Observed Issue:**
We started with CSS Grid for the outer layout and Flexbox for inner widgets. As requirements add nested responsive behaviors, we're mixing Grid, Flexbox, and absolute positioning in ways that are hard to reason about.

**Specific Ask:**
What's the modern CSS layout model for a dashboard with a fixed chrome (sidebar, nav) and a scrollable, responsive main area? Is CSS Subgrid (grid-template-columns: subgrid) necessary for aligning nested widget columns to the outer grid, or is Subgrid still too early for production? What's the equivalent Flexbox-only pattern?""",

"""**Context:**
We have a text truncation issue. Report titles in our table are truncated with text-overflow: ellipsis. Single-line truncation works fine, but we need to truncate at exactly 2 lines.

**Observed Issue:**
display: -webkit-box with -webkit-line-clamp: 2 works in modern browsers. But we're seeing layout shifts in Chromium when the container is inside a CSS Grid or Flexbox item -- the clamped element collapses to 0 height.

**Specific Ask:**
What are the known layout interactions between -webkit-line-clamp and CSS Grid/Flexbox that cause height collapse? Is the fix a min-height on the text container, or wrapping the clamped text in a block with overflow: hidden and a fixed height? And has the standardized line-clamp property been shipped in any browsers?""",

"""**Context:**
We need to implement a responsive sidebar that: (1) is fixed on desktop, (2) overlays as a drawer on mobile, and (3) can be toggled by the user on tablets. The sidebar contains long navigation lists and must be fully accessible.

**Observed Issue:**
Our current implementation uses different components for mobile (drawer) and desktop (fixed sidebar). Managing two separate component instances causes state duplication and a11y issues (two sets of nav links in the accessibility tree).

**Specific Ask:**
What's the correct CSS architecture for a single sidebar component that behaves as a fixed column on desktop and a drawer overlay on mobile? How do you use CSS Custom Properties + media queries to switch between the two modes without duplicating the DOM? And how do you handle focus trapping correctly for the drawer mode without affecting desktop mode?""",

"""**Context:**
We use CSS animations for loading skeletons across our whole dashboard. The skeleton shimmer is a gradient that slides across the element.

**Observed Issue:**
With 50+ skeleton elements visible simultaneously (a full dashboard load), each running its own CSS animation, the CPU usage in the Chrome Performance panel is high and we see frame drops on lower-end devices.

**Specific Ask:**
Why do 50 simultaneous CSS animations cause high CPU usage even though CSS animations are supposed to be GPU-composited? Is the issue that background-position animation isn't compositable (only transform and opacity are)? What's the correct performant shimmer approach -- only animating transform/opacity, or using a single shared animation via a pseudo-element?""",

"""**Context:**
Our design system buttons have a complex hover/focus/active state chain. We use :is() and :where() selectors in the design system's base CSS.

**Observed Issue:**
:is() carries the specificity of its most specific argument. Our use of :is(button, .btn, [role='button']) with a class selector makes the entire rule have specificity 0-1-0, overriding our more specific component styles.

**Specific Ask:**
Explain the specificity difference between :is(), :where(), and :not() selectors. When should :where() be preferred for design-system base styles to avoid specificity creep? And what's the impact of using :has() (which follows :is() specificity rules) for parent selection in a design system context?""",

"""**Context:**
We're implementing a print view for financial reports. The report is 3-5 pages when printed. Page breaks appear in the middle of financial tables, splitting rows across pages.

**Observed Issue:**
We have no @media print styles controlling page breaks. CSS properties page-break-inside: avoid and break-inside: avoid exist but aren't consistently applied.

**Specific Ask:**
What's the complete CSS approach for controlling page breaks in a printable financial table? Does break-inside: avoid on rows reliably prevent row splitting across pages in Chrome, Safari, and Firefox? And how do you add print-specific headers/footers (page numbers, report title) without JavaScript -- only using CSS @page rules?""",

"""**Context:**
We need to implement a masonry layout for a report card grid (variable height cards arranged in columns that fill space without gaps).

**Observed Issue:**
CSS Grid doesn't natively support masonry layout (all rows have equal height). We're using a JavaScript column-balancing approach that recalculates positions on every resize. But the JS approach causes layout shift on initial render.

**Specific Ask:**
Does CSS masonry layout (grid-template-rows: masonry) have browser support yet, or is it still experimental? What's the best CSS-only approximation for masonry that works today -- CSS columns property, or a Flexbox column-direction approach? What are the tab-order and accessibility implications of column-direction Flexbox masonry?""",

"""**Context:**
We have a form with labeled input fields. The label and input should align to a grid, and each label should be text-overflow: ellipsis width-responsive.

**Observed Issue:**
The label text wraps instead of truncating because text-overflow: ellipsis requires overflow: hidden and a fixed width or max-width, but inside a Grid cell the label wants to expand to its content.

**Specific Ask:**
How do you achieve text-overflow: ellipsis on a Grid child that should respect the grid's track sizes, without a fixed width? Is the fix min-width: 0 on the grid cell (overriding the default min-width: auto that allows expansion)? What's the interaction between min-width: 0 and grid-template-columns: auto 1fr for a form layout?""",

"""**Context:**
We have a card component with a fixed aspect ratio (16:9) that should maintain its ratio on all screen sizes. Inside the card is an absolutely positioned overlay.

**Observed Issue:**
We used padding-top: 56.25% (16:9 hack) with position: relative + absolute child. On some configurations the card height collapses because a parent has display: flex.

**Specific Ask:**
Does the aspect-ratio CSS property (aspect-ratio: 16/9) replace the padding-top hack reliably in 2024 browsers? What's the interaction between aspect-ratio and Flexbox/Grid parent sizing? And does aspect-ratio work correctly when combined with max-height constraints?""",

"""**Context:**
Our dashboard uses CSS Modules for component styles. We want to add global utility classes (.sr-only, .visually-hidden) that components can reference without importing a module.

**Observed Issue:**
Global styles added to global.css are available. But in CSS Modules files, composes: from global only works for classes defined in global CSS Modules files, not plain global.css. Components that use composes get scoped class names, which breaks the global utility purpose.

**Specific Ask:**
What's the correct way to use global utility classes (like Tailwind's sr-only pattern) alongside CSS Modules without losing scoping benefits elsewhere? Is :global(.sr-only) the mechanism for referencing global classes from a CSS Module? And how do you ensure global utility classes aren't accidentally scoped when the CSS Modules transform runs?""",

"""**Context:**
We need to implement a tooltip that positions itself to always stay within the viewport -- flipping from bottom to top if there's insufficient space below the trigger.

**Observed Issue:**
Our original approach used getBoundingClientRect() + scroll offsets in JavaScript. This requires a layout read on every scroll/resize. Our new attempt uses CSS only, but we can't find a CSS mechanism to conditionally flip placement.

**Specific Ask:**
Does the CSS Anchor Positioning API (position-anchor, @position-fallback) solve the viewport-aware tooltip placement problem natively? At what browser support level is it safe to use without a JavaScript polyfill? What's the Popper.js/Floating UI tradeoff vs. native CSS anchor positioning for a tooltip system?""",

"""**Context:**
Our design token CSS variables use hsl() values throughout. We're adding a color contrast accessibility feature that generates a high-contrast variant of each color token.

**Observed Issue:**
Generating a high-contrast variant requires knowing the relative luminance of each color. This is mathematically complex in CSS without CSS Color Level 5 functions. Currently we pre-compute all high-contrast variants at build time.

**Specific Ask:**
What CSS Color Level 5 features (color-contrast(), color-mix(), relative color syntax) are available in browsers today that could help with dynamic contrast generation? Can CSS color-mix(in oklch, ...) be used to lighten/darken tokens at runtime without pre-computing all variants? And how should we design our CSS custom property naming convention to support theming across normal, dark, and high-contrast?""",

"""**Context:**
We're adding a smooth page transition animation when navigating between routes in our Next.js 14 App Router. We want a slide/fade effect when navigating between dashboard sections.

**Observed Issue:**
Next.js App Router manages its own navigation lifecycle. Using CSS transitions on route changes is non-trivial because the new page renders immediately, replacing the old one.

**Specific Ask:**
How do you implement page transition animations in Next.js 14 App Router without Framer Motion? Does the View Transitions API (document.startViewTransition) work with Next.js App Router's client-side navigation? What are the browser support constraints, and what's the recommended pattern for graceful degradation when the View Transitions API isn't available?""",

"""**Context:**
Our dashboard table has 50 rows with alternating row colors (zebra striping). We implement this with nth-child(even).

**Observed Issue:**
When rows are dynamically reordered (sort), the nth-child positions don't change (they're DOM position-based), so stripes remain correct. But when a filter hides some rows (display: none), the nth-child numbering skips hidden rows incorrectly, producing uneven stripes.

**Specific Ask:**
How does nth-child count work with hidden (display: none) vs. invisible (visibility: hidden) elements -- does it count them? Is :nth-child(even of .visible-row) (the of selector syntax) the CSS-only fix for filtered zebra stripes? What's the browser support for the of selector syntax in nth-child?""",

"""**Context:**
We have a custom focus ring for our design system. The default browser ring is removed (outline: none) and replaced with a custom box-shadow focus ring.

**Observed Issue:**
Our custom focus ring doesn't appear when navigating with a keyboard in Safari. It works in Chrome and Firefox.

**Specific Ask:**
What are the cross-browser differences in :focus vs. :focus-visible behavior? Does Safari implement :focus-visible? How do you write a universal focus ring that appears for keyboard navigation (using :focus-visible) but not mouse click (using :not(:focus-visible)), consistently across Chrome, Firefox, and Safari?""",

"""**Context:**
We use CSS Grid's auto-fill and auto-fit for our responsive card grid. The cards should be minimum 280px wide and fill the available space.

**Code:**
```css
grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
```

**Observed Issue:**
When the container is exactly 560px wide, two columns appear. When it's 559px, one column appears. But at 840px, three cards appear -- the first two are wider than 1fr average because auto-fill creates an empty invisible track.

**Specific Ask:**
Explain the difference between auto-fill (creates empty tracks) and auto-fit (collapses empty tracks) in this context. At 840px with minmax(280px, 1fr), how many tracks does each create and how wide are they? Which is correct for a card grid that should always stretch to fill available width without empty ghost columns?""",

"""**Context:**
We've added CSS Layers (@layer) to our design system to control cascade order: @layer base, components, utilities. But component styles defined with @layer components are being overridden by old styles in a legacy stylesheet that doesn't use @layer.

**Observed Issue:**
Unlayered (non-@layer) styles always win over layered styles, regardless of layer order. The legacy stylesheet has no @layer declarations, so its styles defeat our new component layer.

**Specific Ask:**
Explain the cascade priority of layered vs. unlayered styles in CSS. Is the only fix to wrap the legacy stylesheet in a low-priority @layer (e.g., @layer legacy) to explicitly place it below component layer? What's the migration strategy for a codebase that has a mix of layered and unlayered CSS?""",

"""**Context:**
We're implementing a dark mode toggle for our dashboard. We detect system preference via prefers-color-scheme and allow user override stored in localStorage.

**Observed Issue:**
Using only CSS prefers-color-scheme (no user override) causes no JavaScript flash. Adding user override (read localStorage in JS, set data-theme attribute) causes a flash before JS hydrates.

**Specific Ask:**
What's the optimal dark mode implementation that supports both system preference detection and user override with zero flash? Does the "inline script before DOM renders" approach fully eliminate the flash, and is it compatible with Next.js 14 App Router's streaming HTML? How does next-themes solve this, and can you replicate its approach without the library?""",

"""**Context:**
We're implementing a CSS-only accordion (expand/collapse sections) without JavaScript, using the details/summary HTML elements.

**Observed Issue:**
The native details/summary accordion animation (height transition) doesn't work because height: auto can't be transitioned in CSS. The section snaps open/closed without animation.

**Specific Ask:**
What's the current CSS-only approach to animate height from 0 to auto (or auto to 0)? Does the new CSS @starting-style rule + transition: display combination solve this in 2024? What's the grid-rows: 0fr to 1fr animation trick, and does it work for arbitrary content heights inside details/summary?""",

"""**Context:**
Our chart tooltips use position: absolute inside a position: relative chart wrapper. Tooltips near the chart edges get clipped by the chart container's overflow: hidden.

**Observed Issue:**
The chart needs overflow: hidden to handle dynamic resizing. But this clips absolute-positioned tooltips.

**Specific Ask:**
What are the options for rendering absolutely-positioned tooltips that can overflow their parent without removing overflow: hidden from the parent? Does the CSS position: fixed tooltip approach work correctly inside a CSS transform parent, or does transform create a containing block that breaks fixed positioning? Is using a React Portal (render tooltip outside chart wrapper) the correct solution here?""",

"""**Context:**
We have a sticky header in our dashboard. The header uses position: sticky with top: 0. On iOS Safari it doesn't behave correctly -- it's not sticky at all on initial load, then sticks after the first scroll, and sometimes flickers.

**Observed Issue:**
iOS Safari has known issues with position: sticky on elements inside overflow: auto or overflow: scroll parents. The sticky element's ancestor chain must not have overflow (other than visible).

**Specific Ask:**
What are the exact rules for position: sticky to work correctly across browsers, specifically regarding overflow on ancestor elements? On iOS Safari, what's the minimal change required to make a sticky header work reliably? And what's the behavior difference between Safari's sticky and Chrome's when inside a CSS transformation context?""",

"""**Context:**
We're adding CSS scroll snapping to our dashboard's onboarding carousel. Items slide one at a time, snapping to each card.

**Code:**
```css
.carousel {
  overflow-x: scroll;
  scroll-snap-type: x mandatory;
}
.carousel-item {
  scroll-snap-align: start;
}
```

**Observed Issue:**
On iOS Chrome, scroll snap works correctly. On Android Chrome, snap points are inconsistent -- the carousel sometimes stops between items, especially when swiping quickly.

**Specific Ask:**
What's the difference between scroll-snap-type: x mandatory and scroll-snap-type: x proximity for mobile performance? Does scroll-snap-stop: always prevent fast-swipe skipping over snap points? And what touch event behaviors (overscroll-behavior, touch-action) interact with CSS scroll snapping in ways that cause inconsistent behavior on Android?""",

"""**Context:**
Our dashboard's responsive design breaks at one specific breakpoint: the sidebar and main content overlap when the viewport is exactly 1024px.

**Observed Issue:**
We have a media query for min-width: 1025px (desktop) and max-width: 1023px (tablet). At exactly 1024px no query applies and the layout reverts to its base styles, which causes an overlap.

**Specific Ask:**
Why is there a gap at exactly 1024px in this breakpoint setup? What's the correct exclusive breakpoint pattern to eliminate gaps (min-width: 1024px for desktop, max-width: 1023.98px for tablet)? And what's the CSS spec behavior for media queries at exactly the boundary value -- is it inclusive or exclusive?""",

"""**Context:**
Our design system uses a t-shirt sizing scale for spacing: xs (4px), sm (8px), md (16px), lg (24px), xl (32px). But we want the spacing to scale proportionally on larger displays.

**Observed Issue:**
Fixed px values mean xs is always 4px on a 4K display. The design should feel proportional at any viewport size without needing dozens of breakpoint overrides.

**Specific Ask:**
What's the approach for fluid spacing scales in CSS? Does clamp(min, preferred, max) with vw units work for spacing tokens, or is it better suited for typography? What's the mathematical relationship between fluid type (clamp with vw) and fluid spacing to maintain proportional visual rhythm across viewport sizes?""",

]

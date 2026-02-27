"""
snippets/q_performance.py — 28 FRESH Performance questions (mix of debugging + code generation)
Zero overlap with archived set.
"""

Q_PERFORMANCE = [

"""**Task (Code Generation):**
Implement an `ImageWithBlurHash` component for Next.js that:
- Shows a BlurHash-generated placeholder during image load
- Fades in the real image once loaded
- Works with `next/image` (wraps it)
- Accepts a `blurHash` prop (base83 encoded string) and decodes it client-side
- Does not block initial render — decodes BlurHash in a `useEffect`

Show the component and explain why BlurHash is preferable to base64 LQIP for large image grids.""",

"""**Debug Scenario:**
A dashboard's Lighthouse score dropped from 72 to 38 after adding a new analytics vendor script. The drop is entirely in TBT (Total Blocking Time) and INP, not LCP.

```html
<script src="https://analytics.vendor.com/sdk.js" />
```

The script is 180KB minified and synchronous. Diagnose the performance impact and rewrite the loading strategy using `async`, `defer`, and dynamic import — explain the behavioral difference of each approach for this use case.""",

"""**Task (Code Generation):**
Build a `useThrottle<T>(value: T, limit: number): T` hook and a `useDebounce<T>(value: T, delay: number): T` hook. Then:
- Explain the exact behavioral difference with a timing diagram
- Show which to use for: (a) window resize handler, (b) search-as-you-type, (c) scroll position tracking, (d) button spam prevention
- Implement a `useThrottledCallback` and `useDebounceCallback` variant that wraps functions rather than values""",

"""**Debug Scenario:**
A React table with 500 rows re-renders in 240ms when a single row is updated. All rows are wrapped in `React.memo`. The Profiler shows all 500 rows with "Rendered" status.

Investigation reveals the `rowClassName` prop is a function defined in the parent:
```tsx
<Table
  rows={rows}
  rowClassName={(row) => row.status === 'error' ? 'error-row' : ''}
/>
```

Why does `React.memo` fail to bail out here even if rows are stable? Implement a fix that allows `Table` to skip re-renders for unchanged rows while supporting dynamic `rowClassName` logic.""",

"""**Task (Code Generation):**
Implement a `useMeasure` hook that measures the dimensions of a DOM element and updates on resize:

```ts
const [ref, { width, height, top, left }] = useMeasure<HTMLDivElement>();
```

Requirements:
- Uses `ResizeObserver` (not `getBoundingClientRect` on scroll)
- Debounces resize callbacks to avoid thrashing (configurable delay)
- Handles element unmounting and remounting
- Returns initial dimensions synchronously if the element is already mounted (use `useLayoutEffect`)

Show usage in a responsive chart that re-renders based on container width.""",

"""**Debug Scenario:**
A Next.js app's `@next/bundle-analyzer` report shows `moment.js` is 230KB of the initial bundle despite the team only using `moment().format('YYYY-MM-DD')`.

```ts
import moment from 'moment';
```

The team claims they tried `import { format } from 'moment'` and it made no difference. Explain why and provide a complete migration plan to `date-fns` including code transforms — showing that `date-fns` tree-shakes where `moment` doesn't.""",

"""**Task (Code Generation):**
Build a `useRequestIdleCallback` hook that defers non-critical work until the browser is idle.

```ts
useRequestIdleCallback(() => {
  prefetchRoutes(); // run during idle time
}, { timeout: 2000 }); // force run after 2s if still not idle
```

Then implement a `usePrefetch(url: string)` hook that uses `useRequestIdleCallback` internally to prefetch the Next.js page data for a route when the user's link enters the viewport — before they click.""",

"""**Debug Scenario:**
A virtualized list using `react-window` shows a blank white area when the user scrolls rapidly on mobile. Increasing `overscanCount` from 2 to 15 reduces blanks but doubles the DOM node count.

The list items contain images loaded with `<img src>`. Diagnose why rapid scroll causes blanking even with overscan, and propose a solution that reduces blank time without increasing DOM size — consider image preloading, scroll velocity detection, or CSS `content-visibility`.""",

"""**Task (Code Generation):**
Implement a `CriticalCSS` extraction workflow for a Next.js app using `critters` or manual critical CSS approach:
- Show how to inline critical CSS for above-the-fold content into `<head>`
- Show how to load the full stylesheet asynchronously without FOUC
- Implement a `<NonCriticalCSS>` component that loads stylesheets after hydration via `useEffect`

Explain why inlining critical CSS improves LCP but can hurt caching, and how to balance the two.""",

"""**Debug Scenario:**
A dashboard's CLS (Cumulative Layout Shift) score is 0.27. The CLS debugger identifies two culprits:
1. An ad banner that loads after page paint and pushes content down by 90px
2. A skeleton loader for the user avatar that uses a different size than the loaded image

For each culprit, diagnose the exact mechanism causing the layout shift and provide the CSS-only fix. Explain how `aspect-ratio` and `min-height` reservation prevent CLS without JavaScript.""",

"""**Task (Code Generation):**
Write a `useLazyImage` hook that implements progressive image loading:
1. Shows a tiny blurred thumbnail (10px × 7px) immediately
2. Loads the full-size image in the background
3. Cross-fades from thumbnail to full image on load
4. Cancels the load if the component unmounts

```ts
const { src, isLoading } = useLazyImage({
  thumbnail: '/img/thumb.jpg',
  full: '/img/full.jpg',
});
```

Show the hook and a usage example with CSS animation for the crossfade.""",

"""**Debug Scenario:**
Analysis of Long Animation Frames (LoAF) in Chrome shows a 180ms frame during the initial dashboard mount. The main culprit is `JSON.parse(largeDataset)` — 2.1MB of JSON being parsed synchronously in a `useMemo` during render.

```ts
const data = useMemo(() => JSON.parse(rawJson), [rawJson]);
```

Propose a solution that keeps the UI responsive during parse. Consider: Web Workers, streaming JSON parse (`@discoveryjs/json-ext`), chunked parse with `scheduler.postTask`, and whether `useDeferredValue` helps here.""",

"""**Task (Code Generation):**
Implement a `useWebWorker<T, R>` hook that offloads computation to a Web Worker:

```ts
const { run, result, loading } = useWebWorker<number[], number>(
  (nums) => nums.reduce((a, b) => a + b, 0) // runs in worker
);
```

Requirements:
- Creates the worker from an inline function (no separate `.worker.js` file) using Blob URLs
- Terminates the worker on unmount
- Handles errors from the worker
- Works with TypeScript generics for input/output types

Explain the serialization limitations (no functions, DOM refs, etc. in messages).""",

"""**Debug Scenario:**
React DevTools Profiler shows a component called `PermissionMatrix` taking 85ms to render. It renders a 50×20 grid of checkboxes. The component is only mounted once and never re-renders — the 85ms is pure initial render time.

The checkboxes are rendered with `useMemo` inside a nested loop. Propose strategies to reduce initial render time to under 16ms — consider: chunked rendering with `scheduler.postTask`, server-side rendering the grid, `<canvas>` rendering, or CSS Grid without individual checkbox components.""",

"""**Task (Code Generation):**
Build a `useScrollRestoration` hook for a Next.js app that:
- Saves scroll position to `sessionStorage` before navigation
- Restores it after the new page loads and renders
- Works with dynamic content that loads after initial render (waits for data)
- Handles edge cases: back/forward navigation vs fresh navigation

Explain why Next.js's built-in `scrollRestoration: 'manual'` is necessary and show the full implementation.""",

"""**Debug Scenario:**
A `<DataGrid>` renders 1,000 rows with no virtualization. The initial render takes 420ms. A team member proposes adding `React.memo` to each row component. Another proposes server-side rendering the grid.

Profile each approach (React.memo, SSR) and explain: (a) what React.memo does to initial render time (spoiler: nothing), and (b) how SSR moves work from client to server. Then propose the correct solution: `content-visibility: auto` + `contain-intrinsic-size` for CSS-only virtualization.""",

"""**Task (Code Generation):**
Implement a Service Worker-based offline cache strategy for a Next.js dashboard:
- Cache API responses with a stale-while-revalidate strategy
- Cache static assets with cache-first
- Show a toast when the user goes offline and data is coming from cache
- Show a sync indicator when new data is available

Use Workbox (not raw Service Worker API). Show the `workbox-config.js`, the `next.config.js` integration, and the React hook that monitors cache status.""",

"""**Debug Scenario:**
An e-commerce product grid renders 48 product cards on the page. Each card has a `<img>` with no `loading` attribute. Lighthouse shows 16 off-screen images are blocking LCP.

```tsx
<ProductCard image={product.image} name={product.name} />
```

Fix the image loading strategy holistically:
1. `loading="lazy"` for off-screen images
2. `fetchpriority="high"` for the first 4 visible images
3. `<link rel="preload">` in the `<head>` for LCP image
4. `decoding="async"` for all images

Explain how each attribute affects browser resource prioritization.""",

"""**Task (Code Generation):**
Design and implement a `usePerformanceObserver` hook that monitors Core Web Vitals in real time and reports them to an analytics endpoint:

```ts
usePerformanceObserver({
  metrics: ['LCP', 'CLS', 'INP', 'FID', 'TTFB'],
  onReport: (metric) => analytics.track('web_vital', metric),
});
```

Show the PerformanceObserver setup for each metric, the correct attribution (what element caused LCP, which interaction caused INP), and how to send metrics on `visibilitychange` to avoid losing data when the user closes the tab.""",

"""**Debug Scenario:**
After deploying a new build, users report the updated JavaScript is not loading — they still see the old version of the app. Investigation shows the CDN is serving cached JS bundles even though Next.js uses content-hash filenames.

The CDN cache-control header is `max-age=86400` (set by the CDN config), and the `_next/static/` path is not excluded from CDN caching rules.

Design the complete CDN configuration: which paths need aggressive caching, which need `no-cache`, and how Next.js's content-hash filenames make immutable caching safe for JS/CSS but not for `/_next/data/` routes.""",

"""**Task (Code Generation):**
Build a `useAnimationFrame` hook for smooth 60fps animations:

```ts
const { start, stop, isRunning } = useAnimationFrame((elapsed) => {
  setPosition(prev => prev + elapsed * speed);
});
```

Requirements:
- `elapsed` is time since last frame in seconds (not milliseconds)
- Stops automatically on unmount
- Handles tab visibility changes (pauses when tab is hidden, resumes when visible)
- The callback always accesses the latest state via a ref (no stale closure)

Show usage animating a progress bar.""",

"""**Debug Scenario:**
A Next.js app's `_app.tsx` wraps every page with 3 Context providers and a global CSS import. After analyzing Webpack's module graph, every page chunk includes these providers even though they're only needed for authenticated routes.

```tsx
// _app.tsx
export default function App({ Component, pageProps }) {
  return (
    <AuthProvider>
      <ThemeProvider>
        <QueryClientProvider client={queryClient}>
          <Component {...pageProps} />
        </QueryClientProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}
```

Design a layout-based provider architecture (App Router) that only initializes heavy providers for routes that need them, reducing the initial JS payload for public/marketing pages.""",

"""**Task (Code Generation):**
Implement `optimizeImages` — a build-time script that:
- Scans all `public/` images
- Generates WebP and AVIF variants using `sharp`
- Creates a `imageManifest.json` mapping original paths → optimized paths + dimensions
- A React hook `useOptimizedImage(src)` that reads the manifest and picks the best supported format using `navigator.userAgent` or `<picture>` elements

Show the script and the hook.""",

"""**Debug Scenario:**
A team member added `will-change: transform` to every animated element on the page "for performance". Now the browser's memory usage has increased by 400MB and compositing layer count jumped from 8 to 127.

Explain exactly what `will-change: transform` does at the GPU compositing layer level, why applying it to too many elements is harmful, and give the correct heuristic for when `will-change` actually helps vs hurts. Show the DevTools workflow to audit layer count.""",

"""**Task (Code Generation):**
Build a `<SuspenseImage>` component that integrates with React Suspense for loading images:

```tsx
<Suspense fallback={<Skeleton />}>
  <SuspenseImage src="/hero.jpg" alt="Hero" />
</Suspense>
```

Requirements:
- Uses a cache to track image load status (loaded, loading, error)
- Throws a Promise while loading (Suspense protocol)
- Throws an Error on load failure (ErrorBoundary protocol)
- The cache persists across re-renders (singleton outside component)

Show the implementation and explain the `read()` function pattern.""",

"""**Debug Scenario:**
A React app using `styled-components` sees 12ms of scripting time on each re-render in the Performance tab, even for renders where no styled props change. The team is using `styled-components@6` with SSR.

Diagnose why styled-components has runtime overhead per-render even without prop changes, and compare to zero-runtime alternatives: `vanilla-extract`, `Linaria`, and `@emotion/css` with Babel plugin. Show a migration path for the most performance-critical components only.""",

"""**Task (Code Generation):**
Implement a `usePrefetchOnHover` hook that preloads route data when a user hovers over a link for more than 100ms:

```tsx
const prefetchProps = usePrefetchOnHover('/dashboard/reports');
return <Link href="/dashboard/reports" {...prefetchProps}>Reports</Link>;
```

- Uses a 100ms delay to avoid unnecessary prefetches on accidental hovers
- Uses Next.js `router.prefetch()` for the actual prefetch
- Cancels the prefetch timer if hover ends before 100ms
- Tracks already-prefetched routes to avoid re-fetching

Show the hook and explain how it improves perceived navigation performance.""",

"""**Debug Scenario:**
After switching from Create React App to Vite, the production bundle is 40% smaller but hot module replacement (HMR) during development is slower than CRA for large files.

Investigation shows that a `constants.ts` file with 3,000 lines of exported constants is being re-evaluated on every HMR update, even when only one constant changed — because every other module imports from the barrel file.

Diagnose the barrel file HMR problem, show how to split constants into smaller modules, and explain Vite's module graph invalidation strategy vs Webpack's.""",

]

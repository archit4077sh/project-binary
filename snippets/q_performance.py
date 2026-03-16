"""
snippets/q_performance.py — BATCH 3: 28 brand-new Performance questions
Zero overlap with batch1 or batch2 archives.
"""

Q_PERFORMANCE = [

"""**Task (Code Generation):**
Implement a `useIdleCallback` hook that schedules non-urgent work during browser idle time:

```ts
useIdleCallback(() => {
  prefetchNextPageData(); // run when browser is idle
}, { timeout: 3000 }); // force-run after 3s even if not idle
```

Show: the `requestIdleCallback` API with the `IdleDeadline` parameter, how to check `deadline.timeRemaining()` for chunking long tasks, the `cancelIdleCallback` cleanup, and a polyfill using `setTimeout(fn, 1)` for browsers that don't support it. Explain the difference between idle callbacks and microtasks.""",

"""**Debug Scenario:**
A Next.js app's Lighthouse score for Largest Contentful Paint (LCP) is 4.8 seconds. The LCP element is a hero image loaded with `<img>` (not `next/image`). 

The image is 2.4MB, served without a CDN, not preloaded, and not using modern formats. For each of the four issues, show the exact fix: `next/image` config for automatic WebP/AVIF conversion, `<link rel="preload">` in `<head>`, uploading to Vercel's image CDN, and `sizes` attribute for responsive loading. Predict the LCP improvement for each fix.""",

"""**Task (Code Generation):**
Build a `<LazyImage>` component that:
- Loads the image only when it's within 200px of the viewport (IntersectionObserver rootMargin)
- Shows a low-quality placeholder (LQIP) while loading (a 20px blurred version)
- Transitions from blurred placeholder to sharp image with a CSS cross-fade
- Handles `srcset` and `sizes` for responsive images
- Reports load time to an analytics service

Show the component, the IntersectionObserver setup, and the CSS transition.""",

"""**Debug Scenario:**
A React app's bundle contains three versions of `lodash` adding 450KB: `lodash` (v4.17, full), `lodash-es` (v4.17, ESM), and `@types/lodash` (dev only). Tree shaking doesn't reduce lodash because the app uses `import _ from 'lodash'` (default import).

Show Webpack bundle analysis commands to find the duplication, the exact import pattern change (`import debounce from 'lodash/debounce'`) that enables tree shaking, the Webpack `resolve.alias` to redirect all lodash imports to lodash-es, and which lodash methods to replace with native JavaScript in 2024.""",

"""**Task (Code Generation):**
Implement a Client-Side Performance Monitor component that tracks and reports Core Web Vitals in real time:

```tsx
<PerformanceMonitor
  onMetric={({ name, value, rating }) => analytics.track(name, { value, rating })}
  debug // shows floating overlay with live metrics
/>
```

Capture: LCP (PerformanceObserver `largest-contentful-paint`), FID/INP (`event` type observer), CLS (`layout-shift` accumulated score), TTFB (`navigation` entry), FCP. Show the observer setup, score rating thresholds (good/needs improvement/poor), and the overlay UI.""",

"""**Debug Scenario:**
A server-side rendered page's Time To First Byte (TTFB) averages 1.8 seconds. Profiling shows the bottleneck is a single database query fetching all products (2,000 rows) with no pagination, running synchronously before any HTML is sent.

Show the streaming solution using Next.js 14's `loading.tsx` (Suspense boundary), how React's streaming SSR sends HTML chunks incrementally, the database query optimization (cursor-based pagination + covering index), and how `generateMetadata` vs page data fetching affects TTFB.""",

"""**Task (Code Generation):**
Implement a `useRenderBudget` hook that warns when a component exceeds a render time budget:

```ts
useRenderBudget('UserTable', 16); // warn if render > 16ms (one frame)
```

Show: using `performance.mark()` and `performance.measure()` to time renders, wrapping with `useLayoutEffect` for post-render measurement, collecting statistics (mean, p95, p99 over last 100 renders), logging warnings in development only, and how to integrate with React DevTools profiler API (`Profiler` component).""",

"""**Debug Scenario:**
A Single Page Application has a JavaScript bundle of 1.8MB (uncompressed). After enabling Brotli compression on the server, the network transfer drops to 420KB — but mobile users on slow 3G connections still experience a 12-second Time to Interactive because the main thread is busy parsing and executing JavaScript.

Explain the Parse/Compile/Execute cost of JavaScript vs CSS, show how to measure parse time with Chrome DevTools' Coverage tab, and implement the fix: aggressive code splitting with `React.lazy` per route, moving non-critical scripts to Web Workers with Comlink, and deferring analytics initialization to after TTI.""",

"""**Task (Code Generation):**
Build a `<ProgressiveTable>` that renders large datasets progressively:
- Renders the first 50 rows immediately (above the fold)
- Schedules remaining rows in idle callbacks (50 rows per chunk)
- Shows a progress indicator while rows are being rendered
- Allows the user to cancel progressive loading and jump straight to full render if they scroll fast

Show the `requestIdleCallback` chunking logic, the React state management for progressive appending, and why this approach is better than pagination for search result tables.""",

"""**Debug Scenario:**
A developer runs `npm run build` and notices the production bundle is 200KB larger than expected. `source-map-explorer` shows `date-fns` contributing 180KB even though only `format` and `parseISO` are used.

Investigation shows the import is:
```ts
import { format, parseISO } from 'date-fns';
```

This should tree-shake correctly. But the `tsconfig.json` has `"moduleResolution": "node"` which resolves to the CJS build of `date-fns` (no tree shaking). Show the full fix: switching to `"moduleResolution": "bundler"` or `"node16"`, the `date-fns/esm` subpath, and verifying with `webpack-bundle-analyzer`.""",

"""**Task (Code Generation):**
Implement a `prefetchOnHover` utility that preloads page data when the user hovers a link (before clicking):

```ts
// Attach to all internal links automatically:
prefetchOnHover({
  selector: 'a[href^="/"]',
  loader: (href) => fetch(href, { priority: 'low' }),
  debounce: 100, // only prefetch after hovering 100ms
  maxConcurrent: 3,
});
```

Show: the event delegation setup, the `fetch` with low priority hint, deduplication (don't prefetch the same URL twice), abort on `mouseleave` if fetch hasn't started, and browser cache storage so navigating to prefetched pages is instant.""",

"""**Debug Scenario:**
A Next.js app using `next/font` shows a Font Flash (FOUT) on initial load despite `next/font` promising no layout shift. The flash affects the heading font.

Investigation shows `next/font/google` is configured correctly, but the font is applied to a `className` on a Client Component that only mounts after hydration — the server renders without the font class.

Explain why applying font classes to Client Components causes FOUT vs applying them to the `<html>` element in the root layout. Show the correct font integration pattern and the CSS `font-display: optional` tradeoff.""",

"""**Task (Code Generation):**
Build a `useBackgroundSync` hook that queues failed API requests and syncs them when the connection is restored:

```ts
const { queue, pendingCount, sync } = useBackgroundSync({
  onSync: async (request) => {
    await fetch(request.url, request.options);
  },
  storage: 'indexeddb', // survive page refresh
});
```

Integrate with the Service Worker Background Sync API for reliability when the page closes. Show the hook, the SW registration, and the `sync` event handler in the service worker. Handle the case where Background Sync isn't supported (polyfill with `online` event).""",

"""**Debug Scenario:**
A dashboard with 12 chart components renders slowly (800ms) when any filter is changed. Each chart uses `recharts` and receives a filtered dataset. React DevTools Profiler shows all 12 charts re-render even when only 2 are affected by the changed filter.

```ts
// Parent component:
const filteredData = useMemo(() => applyFilters(rawData, filters), [rawData, filters]);
// Passes ALL filtered data to each chart, each chart extracts its own slice
```

Show the optimization: separate the filtering per-chart (each chart gets its own memoized slice), then use `React.memo` comparison on the slice, reducing re-renders from 12 to 2 on average.""",

"""**Task (Code Generation):**
Implement a `useConnectionSpeed` hook that measures and tracks network quality:

```ts
const { downlink, rtt, type, isSlowNetwork } = useConnectionSpeed();
```

Combine two sources: (1) Network Information API (`navigator.connection`) for passive monitoring, (2) Active measurement by fetching a small known-size resource and measuring time. Show: the measurement fetch with a cache-busting URL, the bytes/milliseconds calculation, smoothing over multiple measurements with a rolling average, and using the result to adaptively load low-res or high-res images.""",

"""**Debug Scenario:**
A checkout page has a First Input Delay (FID) of 340ms on mobile. The user clicks "Place Order" and the button feels unresponsive for a third of a second. Chrome DevTools Long Tasks shows a 380ms task running when the button is clicked.

The task is a synchronous price recalculation (`recalculate()`) triggered by `onClick` before the API call. The recalculation iterates 5,000 cart promotions.

Show: breaking the work with `setTimeout(fn, 0)` slicing, moving it to a Web Worker with `comlink`, and using `startTransition` to mark the recalculation as non-urgent rendering. Explain which fix reduces FID vs which reduces TTI vs Interaction to Next Paint (INP).""",

"""**Task (Code Generation):**
Build a `<SmartImage>` component that selects the optimal image format based on browser support:

```tsx
<SmartImage
  src="/hero"
  alt="Hero image"
  formats={{ avif: '/hero.avif', webp: '/hero.webp', jpg: '/hero.jpg' }}
  width={1200} height={600}
/>
```

Show: `<picture>` element with `<source>` for format negotiation, `srcset` for resolution switching, `loading="lazy"` for below-fold images, `fetchpriority="high"` for LCP images, and a runtime format detection function that uses `createImageBitmap` to test browser support without a server round-trip.""",

"""**Debug Scenario:**
A React app deployed to Vercel has Cumulative Layout Shift (CLS) of 0.18 (poor, threshold is 0.1). The shift happens 2 seconds after page load when an ad banner loads and pushes content down 90px.

Show the three-part fix: (1) explicit `width` and `height` on the ad container to reserve space before the ad loads, (2) using CSS `aspect-ratio` as a modern alternative to the padding-top hack, (3) loading the ad using `IntersectionObserver` to defer it below the fold so it never causes layout shift for above-fold content. Measure CLS before and after.""",

"""**Task (Code Generation):**
Implement a compressed in-memory cache for computed values that evicts least-recently-used entries:

```ts
const cache = new LRUCache<ComputedReport>({ maxSize: 50, ttl: 5 * 60_000 });

const report = cache.getOrCompute('report-2024-q1', () => computeExpensiveReport(params));
```

Show: the doubly-linked list + hash map LRU implementation, TTL expiration (don't evict early but return stale on TTL miss), `getOrCompute` that prevents duplicate parallel computation for the same key (singleton promise), and React integration via `useRef` to ensure the cache persists across renders without being in state.""",

"""**Debug Scenario:**
A heavily animated landing page runs at 60fps on desktop but drops to 15fps on a mid-tier Android phone. Chrome DevTools remote debugging shows the main thread is blocked by a CSS animation that modifies `left` and `top` properties:

```css
@keyframes float {
  0%, 100% { top: 0px; }
  50% { top: -20px; }
}
```

Layout-triggering animations can't run on the compositor thread. Show: the exact refactor to use `transform: translateY()` instead, `will-change: transform` to promote the element to its own compositor layer, `contain: strict` to limit style recalculation scope, and the Chrome Layers panel to verify compositor promotion.""",

"""**Task (Code Generation):**
Build a `ServiceWorkerCache` class that implements cache-first with stale-while-revalidate for a PWA:

```ts
// In service-worker.ts:
const apiCache = new ServiceWorkerCache('api-v1', {
  strategy: 'stale-while-revalidate',
  maxAge: 60 * 60 * 1000, // 1 hour
  maxEntries: 100,
});

self.addEventListener('fetch', (e) => {
  e.respondWith(apiCache.handle(e.request));
});
```

Show the full implementation, cache versioning across SW updates, how to purge old caches on activation, and the `precacheAndRoute` pattern for static assets.""",

"""**Debug Scenario:**
A developer measures that their app's Time to Interactive (TTI) is 7 seconds on a slow 3G mobile connection. WebPageTest shows the waterfall: HTML (0-500ms), CSS (200-800ms), main JS bundle (500-4000ms), React init (4000-5000ms), data fetch (5000-6500ms), hydration (6500-7000ms).

Identify all optimization opportunities in the waterfall and show the implementations: `<link rel="preconnect">` for API origin, `<link rel="preload" as="script">` for critical chunks, `defer` vs `async` for third-party scripts, and splitting the data fetch to start server-side in parallel with JS loading.""",

"""**Task (Code Generation):**
Implement a `useScheduler` hook that manages a priority queue of tasks, running high-priority tasks first during idle time:

```ts
const { schedule, cancel } = useScheduler();

// High priority (runs immediately if browser is idle):
schedule(() => updateVisibleContent(), { priority: 'user-blocking' });
// Low priority (runs in background):
schedule(() => analyticsBatch.flush(), { priority: 'background' });
```

Show using `scheduler.postTask()` (Chrome 94+) with fallbacks to `requestIdleCallback` and `MessageChannel` for older browsers. Include a React hook that auto-cancels scheduled tasks on component unmount.""",

"""**Debug Scenario:**
A React app renders a user avatar from Gravatar with `<img src={gravatarUrl}>`. On slow connections, the image takes 2 seconds to load, causing layout shift and a poor user experience. There's no placeholder.

Show how to detect image load state using React, implement three progressive states: (1) colored initials placeholder matching the user's accent color while image loads, (2) low-quality LQIP from a 1px Gravatar variant while full image loads, (3) smooth CSS cross-fade transition to the loaded image. Also handle the case where Gravatar returns a 404 (default to initials permanently).""",

"""**Task (Code Generation):**
Build a `<Virtualized3DList>` that renders a windowed list with "3D" CSS perspective for a carousel-like effect:

```tsx
<Virtualized3DList
  items={1000_items}
  itemHeight={80}
  visibleCount={7}
  perspective={800}
  renderItem={(item, index, distanceFromCenter) => (
    <Card style={{ opacity: 1 - Math.abs(distanceFromCenter) * 0.15 }} item={item} />
  )}
/>
```

Show: the central item selection logic, CSS `transform: rotateX()` based on item distance from center, the virtual window (only render ±5 from center), smooth scrolling with `requestAnimationFrame`, and keyboard arrow-key navigation.""",

"""**Debug Scenario:**
An e-commerce category page fetches 200 product thumbnails. The page loads quickly (HTML delivered in 200ms) but Lighthouse marks First Contentful Paint at 3.2 seconds because the browser waits for 200 image requests.

Show: the HTTP/2 multiplexing limit (6 parallel requests per domain for HTTP/1.1, unlimited for HTTP/2 but browser still queues), `loading="lazy"` for below-fold images, `fetchpriority="high"` for the 3 hero images above the fold, image sprite sheets for small icons, and Content-Length headers to help the browser prioritize render-blocking resources.""",

"""**Task (Code Generation):**
Implement an adaptive polling hook that adjusts its polling interval based on whether the tab is visible and whether new data is being received:

```ts
const { data, pollInterval } = useAdaptivePolling('/api/notifications', {
  minInterval: 5_000,   // poll at most every 5s when active
  maxInterval: 120_000, // poll at most every 2min when idle
  backoffFactor: 2,     // double interval on each empty response
  resetOnData: true,    // reset to minInterval when new data arrives
});
```

Show: the interval state machine, Page Visibility API integration (pause when hidden), exponential backoff calculation, and React Query integration as an alternative approach.""",

"""**Debug Scenario:**
A design agency's marketing site has a JavaScript-heavy hero animation (Three.js scene). The animation runs fine on desktop but on iOS Safari it crashes the browser tab due to memory pressure.

DevTools memory snapshot shows the Three.js `WebGLRenderer` isn't being disposed when the hero section scrolls out of view, and a new renderer is created every time it re-enters. The component creates a renderer in `useEffect` but the cleanup function calls `renderer.dispose()` — yet the memory leak persists.

Diagnose why `renderer.dispose()` alone doesn't release GPU memory in Three.js (need `renderer.forceContextLoss()` + `renderer.domElement.remove()`), and show the complete Three.js cleanup sequence that prevents the iOS crash.""",

]

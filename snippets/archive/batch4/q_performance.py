"""
snippets/q_performance.py — BATCH 4: 28 brand-new Performance questions
Zero overlap with batch1, batch2, or batch3 archives.
"""

Q_PERFORMANCE = [

"""**Task (Code Generation):**
Implement a `usePaintTiming` hook that reports First Paint, First Contentful Paint, and Largest Contentful Paint metrics:

```ts
const { fp, fcp, lcp, ttfb } = usePaintTiming();
// fp: 120ms, fcp: 280ms, lcp: 1800ms, ttfb: 80ms
```

Show: `PerformanceObserver` for `paint` entries, `largest-contentful-paint` entries, `navigation` entries for TTFB, collecting all registered entries before the observer was created using `getEntriesByType`, and how to report these to an analytics endpoint with `navigator.sendBeacon` on `visibilitychange` to avoid blocking page unload.""",

"""**Debug Scenario:**
A Next.js app's page bundle includes `moment.js` (70KB gzipped) but the app only uses `moment().format('YYYY-MM-DD')`. The developer replaces it with a smaller alternative, but the bundle size doesn't decrease.

Investigation with `next build --debug` output shows `moment` is still included because a dependency (`react-datepicker`) imports `moment` as a peer. Show: using `resolve.alias` in `next.config.js` to redirect `moment` → `dayjs`, the `babel-plugin-import` for tree-shaking datepicker components, and measuring before/after with `@next/bundle-analyzer`.""",

"""**Task (Code Generation):**
Build a `ParallelDataLoader` that loads multiple resources in parallel with priority and circuit-breaking:

```ts
const loader = new ParallelDataLoader({
  maxConcurrent: 4,
  timeout: 5000,
  retries: 2,
});

const [user, orders, recommendations] = await loader.all([
  { key: 'user',            load: () => getUser(id),           priority: 'high' },
  { key: 'orders',          load: () => getOrders(id),         priority: 'medium' },
  { key: 'recommendations', load: () => getRecommendations(id),priority: 'low' },
]);
```

Show: priority queue ordering, concurrent slot management with a semaphore, timeout with `AbortController`, retry with exponential backoff, and partial results (return what succeeded even if low-priority fails).""",

"""**Debug Scenario:**
A React app's Interaction to Next Paint (INP) score is 620ms (very poor, threshold is 200ms). The worst interaction is clicking a "Add to cart" button. Profiler shows:

```
onClick → setState → re-render (420ms) → DOM update (50ms)
```

The 420ms re-render happens because clicking "Add to cart" triggers a global state update that causes the entire product catalog (800 items) to re-render.

Show: using `startTransition` to defer the non-urgent catalog re-render, `React.memo` + `useCallback` to prevent catalog items from re-rendering entirely (the item count doesn't change, only cart state changes), and measuring the improvement with `PerformanceObserver` for `event` entries.""",

"""**Task (Code Generation):**
Implement a `useImageOptimization` hook that automatically selects the best image variant:

```ts
const { src, loading } = useImageOptimization('/hero.jpg', {
  intrinsicWidth: 1200,
  displayWidth: containerWidth,
  devicePixelRatio: window.devicePixelRatio,
  formatPreference: ['avif', 'webp', 'jpg'],
  quality: 80,
});
```

Show: `<picture>` element generation from the hook's output, the CDN URL template for requesting specific dimensions and formats, client-side format support detection using `createImageBitmap`, and calculating the optimal `srcset` widths for a given display width (1x, 1.5x, 2x, 3x DPR variants).""",

"""**Debug Scenario:**
A developer measures their app's Time to Interactive (TTI) using Lighthouse and gets 8.2 seconds. The waterfall shows a 4-second "Long Task" immediately after JS parse. The Lighthouse treemap shows `analytics.js` (from a third-party analytics provider) as the culprit.

Show: loading third-party scripts with `<Script strategy="lazyOnload">` (Next.js), creating a Partytown setup that moves third-party scripts to a Web Worker thread (keeps main thread free), the Partytown configuration in `next.config.js`, and validating the fix with Chrome's Long Tasks API (`PerformanceObserver` for `longtask` type).""",

"""**Task (Code Generation):**
Build a `useComputeInWorker` hook that offloads expensive calculations to a Web Worker:

```ts
const { result, isComputing, cancel } = useComputeInWorker(
  workerFn,   // function to run in worker (serialized to blob URL)
  dependency, // deps — recomputes when this changes
);

// worker fn (runs in a separate thread):
function workerFn(data: number[]): number {
  return data.reduce((sum, n) => sum + Math.pow(n, 2), 0);
}
```

Show: creating a Worker from a function using `URL.createObjectURL(new Blob([...]))`, structured clone transferable types, cancellation via `worker.terminate()`, error handling from worker `onerror`, and why `useEffect` cleanup must terminate the worker.""",

"""**Debug Scenario:**
A CMS preview page renders 150 Rich Text blocks, each using a heavy markdown parser. The page takes 3 seconds to render on initial load. React DevTools Profiler shows each `<RichTextBlock>` taking 18ms to render.

The blocks are static — their content never changes during the session. `React.memo` is applied but doesn't help because the parent passes an inline `style` object that creates new references on every render:

```tsx
<RichTextBlock content={block.content} style={{ color: theme.text }} />
```

Show: extracting `style` into a memoized variable outside the rendered JSX, the `React.memo` comparator that deep-compares the `style` prop, and using CSS custom properties instead of inline styles for theme values to avoid the reference change entirely.""",

"""**Task (Code Generation):**
Implement a `ResourceHints` component that declaratively injects `<link>` preconnect/prefetch/preload hints:

```tsx
<ResourceHints
  preconnect={['https://fonts.googleapis.com', 'https://api.example.com']}
  prefetch={['/about', '/contact']}
  preload={[
    { href: '/fonts/Inter.woff2', as: 'font', crossOrigin: 'anonymous' },
    { href: '/hero.jpg', as: 'image', media: '(min-width: 1200px)' },
  ]}
/>
```

Show: `ReactDOM.createPortal` into `document.head`, deduplication (don't add the same hint twice), removing hints on unmount, and the performance impact of each hint type (preconnect saves DNS+TCP, prefetch queues documents, preload prioritizes current page resources).""",

"""**Debug Scenario:**
A React Native app shows jank (frame drops to 30fps) when scrolling a `<FlatList>` with 1000 items. Each item renders a product card with an image loaded from a URL. React DevTools shows excessive re-renders on the JS thread.

Show: `FlatList` optimization checklist — `keyExtractor`, `getItemLayout` for fixed height items (skips dynamic height estimation), `initialNumToRender: 10`, `maxToRenderPerBatch: 5`, `windowSize: 5`, `removeClippedSubviews: true` (Android), `React.memo` on the item renderer, `FastImage` library for image caching, and `InteractionManager.runAfterInteractions` for deferred data loading.""",

"""**Task (Code Generation):**
Build a `useSmartPolling` hook that switches between polling and WebSocket based on connection capability:

```ts
const { data, connectionType, pollInterval } = useSmartPolling('/api/price', {
  wsUrl: 'wss://prices.example.com',
  fallbackInterval: 5000,   // poll every 5s if WS not available
  onConnectionChange: (type) => analytics.track('connection_type', { type }),
});
```

Show: WebSocket connection attempt with a 3-second timeout, graceful downgrade to polling if WS fails or is blocked, the re-attempt logic (try WS every 60 seconds in case user's network changes), `navigator.connection.type` check to skip WS on `2g`/`slow-2g`, and TypeScript discriminated union for `connectionType`.""",

"""**Debug Scenario:**
A Next.js app reports high server CPU usage. Profiling shows the `getServerSideProps` function for the homepage runs for 800ms. The function fetches 5 independent API endpoints sequentially:

```ts
const user = await getUser(id);
const orders = await getOrders(id);
const notifications = await getNotifications(id);
const products = await getProducts();
const banners = await getBanners();
```

Show: refactoring to parallel `Promise.all`, identifying which calls have data dependencies (must be sequential) vs which are independent (can be parallel), estimated time reduction, and adding `Promise.allSettled` so a failed non-critical call (banners) doesn't break the entire page render.""",

"""**Task (Code Generation):**
Implement a `useBundlePreloader` hook that preloads lazy chunks based on user behavior:

```ts
useBundlePreloader({
  routes: {
    '/dashboard': () => import('./DashboardPage'),
    '/settings':  () => import('./SettingsPage'),
  },
  strategy: 'hover', // preload on link hover
  // OR:
  strategy: 'idle',  // preload on browser idle
  // OR:
  strategy: 'viewport', // preload when link is in viewport
});
```

Show: React Router `matchPath` for determining which routes to preload, attaching `mouseover` event listeners to `<a>` tags for hover strategy, `requestIdleCallback` for idle strategy, and `IntersectionObserver` for viewport strategy. The import is triggered but not awaited — just starting the chunk download.""",

"""**Debug Scenario:**
A dashboard app displays 12 `<Chart>` components, each using a `<canvas>` element. On a MacBook with a Retina display (2x DPR), all charts appear blurry.

The canvas is set to CSS dimensions but the drawing resolution isn't scaled:

```ts
canvas.width = 400;  // logical pixels, not physical
canvas.height = 300;
ctx.drawImage(...);
// On 2x DPR: canvas renders blurry because 400x300 canvas stretched to 800x600 CSS pixels
```

Show: the correct pattern — `canvas.width = 400 * devicePixelRatio`, `canvas.height = 300 * devicePixelRatio`, `ctx.scale(devicePixelRatio, devicePixelRatio)`, and then setting `canvas.style.width = '400px'`. Explain why this fixes the blur and how to detect DPR changes (external monitor plugged in/out) with `window.matchMedia('screen and (resolution: 2dppx)').addEventListener('change', ...)`.""",

"""**Task (Code Generation):**
Build a `<ProgressiveHydration>` wrapper that delays hydrating expensive components until they're needed:

```tsx
<ProgressiveHydration
  strategy="visible"     // hydrate when in viewport
  id="user-reviews"
  fallback={<ReviewsSkeleton />}
>
  <UserReviews productId={id} />
</ProgressiveHydration>
```

Show: the server rendering the full HTML (including `<UserReviews>`), the client-side wrapper that renders a skeleton and only hydrates (`ReactDOM.hydrateRoot`) when the `IntersectionObserver` fires, and why this reduces Time to Interactive for below-fold content even though the HTML is already present.""",

"""**Debug Scenario:**
A Next.js app caches API responses in a Redis instance. Cache hit rate is 45% and average response time for cache misses is 1.4s. The product team asks for sub-200ms responses for all users.

Problems identified: (1) Cache key is `userId + productId` — too specific, each user gets their own cache. (2) TTL is 30 seconds — heavy products expire constantly.

Show: redesigning cache keys to `productId` only (user-specific data fetched separately), edge caching popular products with TTL of 1 hour (instead of 30s), `stale-while-revalidate` strategy for near-miss scenarios, and `cache: 'force-cache'` + `next: { tags: ['product', id] }` for Next.js server-side caching.""",

"""**Task (Code Generation):**
Implement a `useMemoryPressure` hook that degrades gracefully when device memory is low:

```ts
const { memoryLevel, isLowMemory } = useMemoryPressure({
  thresholds: {
    critical: 512,  // MB — use minimal features
    low: 1024,      // MB — use reduced features
    normal: 2048,   // MB — full features
  },
});

// Usage:
const maxRenderItems = isLowMemory ? 50 : 500;
const showAnimations = memoryLevel === 'normal';
```

Show: `navigator.deviceMemory` for initial classification, `performance.memory` (Chrome-only) for runtime monitoring, a polling interval that adjusts quality settings, and graceful degradation strategies for `critical` memory (disable virtualization, render less, clear image caches).""",

"""**Debug Scenario:**
A developer sets `cache: 'no-store'` on a database-fetching Server Component to ensure fresh data. But this disables React's request-level deduplication, so the same query runs 8 times (one per component that calls it on the page).

```ts
// Called in 8 different Server Components on the same page:
const user = await fetch(`/api/user/${id}`, { cache: 'no-store' }); // 8 network requests
```

Show: `React.cache()` deduplicates per render tree — wrap the fetch function once, use it everywhere on the page, and get 1 request instead of 8. Explain: `React.cache()` is NOT persistent across requests (new cache per render), so `cache: 'no-store'` behavior is preserved while deduplicating within the same page render.""",

"""**Task (Code Generation):**
Build a `useNetworkIdle` hook that detects when all in-flight network requests complete:

```ts
const { isNetworkIdle, pendingRequests, waitForIdle } = useNetworkIdle({
  idleTimeout: 200, // consider idle after 200ms of no new requests
});

// Await until network is idle before taking a screenshot:
await waitForIdle();
```

Show: monkey-patching `XMLHttpRequest` and `fetch` to track in-flight requests, incrementing/decrementing a counter, the idle detection timer that resets on new requests, `waitForIdle()` returning a Promise that resolves when the counter hits 0 and stays at 0 for `idleTimeout`ms, and cleanup on unmount.""",

"""**Debug Scenario:**
A static Next.js site (exported with `next export`) has slow cold-start times on Cloudflare Pages Workers because the HTML files are large (each page is 280KB). The large size comes from inline base64-encoded LQIP (Low Quality Image Placeholders) for every image on the page.

Show: moving LQIP from base64 inline (adds bytes to HTML) to CSS `background-image` on a placeholder element (loads after HTML parse), using SVG-based LQIPs (15 bytes vs 2KB for base64), and the `blurhash` library as an alternative that encodes to a short string and decodes in JavaScript.""",

"""**Task (Code Generation):**
Implement a `measureRenderPhases` utility for fine-grained React performance measurement:

```ts
const { measure, report } = measureRenderPhases('UserList');

// In component:
measure('filter');                    // mark start
const filtered = items.filter(...);
measure('filter ends');               // mark end → records duration
measure('sort');
const sorted = filtered.sort(...);
measure('sort ends');

// In DevTools:
report(); // { filter: 2.3ms, sort: 8.1ms, total: 10.4ms }
```

Show: `performance.mark()` and `performance.measure()` implementation, a React `<Profiler>` wrapper that correlates custom marks with React's onRender callback, and how to expose all recorded measures in the React DevTools Profiler timeline using the User Timing API.""",

"""**Debug Scenario:**
A developer adds `export const revalidate = 0` to a Next.js page to opt out of caching, expecting the same behavior as `getServerSideProps`. But the page still serves cached responses from Vercel's edge cache.

Show: the three layers of caching in Next.js App Router (React Server Component payload cache, fetch() data cache, and full route cache), how `revalidate = 0` opts out of the full route cache but NOT the edge cache, using `Cache-Control: no-store` as a response header from a Route Handler to bypass Vercel's edge, and how `cookies()` / `headers()` in a Server Component automatically makes a route dynamic (effectively `revalidate = 0`).""",

"""**Task (Code Generation):**
Build a `<SelectiveHydration>` system that hydrates components in priority order on client load:

```tsx
// Critical: hydrate immediately
<Hydrate priority="critical"><Header /></Hydrate>

// High: hydrate in first idle callback
<Hydrate priority="high"><SearchBar /></Hydrate>

// Low: hydrate when in viewport
<Hydrate priority="low"><Footer /></Hydrate>
```

Show: the `<Hydrate>` wrapper that renders the server HTML statically but delays client-side React reconciliation based on priority, using `Suspense` for the hydration boundary, `startTransition` for non-critical hydration, and why this reduces TTI for complex pages.""",

"""**Debug Scenario:**
A GraphQL query fetches a user profile with fragments spread across 6 components. After a mutation updates the user's avatar, only 2 of the 6 Components re-render. The other 4 show the old avatar.

Apollo Client's normalized cache should update all instances. But 4 components use `useQuery` with a query that doesn't include the `__typename` and `id` fields in their fragments — Apollo can't normalize these objects, so they're stored as embedded (non-normalized) data.

Show: adding `__typename` and `id` to all fragments, Apollo's InMemoryCache normalization algorithm, and using `@client` fields with `readFragment` to manually trigger cache updates for embedded objects that can't be automatically normalized.""",

"""**Task (Code Generation):**
Implement a `useThrottledCallback` hook that throttles a callback to fire at most once per animation frame:

```ts
const throttledOnScroll = useThrottledCallback(
  (e: ScrollEvent) => updateScrollPosition(e.target.scrollTop),
  'rAF' // requestAnimationFrame throttle
);

// Also support time-based throttle:
const throttledSearch = useThrottledCallback(search, 300); // 300ms
```

Show: rAF-based throttle (cancel pending frame on new call, schedule new frame), time-based throttle (track `lastCalled`, skip if within interval), the `leading` and `trailing` options, how `useCallback` + `useRef` prevents stale closures, and cleanup via `cancelAnimationFrame` in the `useEffect` cleanup.""",

"""**Debug Scenario:**
A production Next.js deployment on Vercel shows significantly different performance between the first request to a region (cold) vs subsequent requests (warm). Cold requests take 4.2 seconds; warm requests take 180ms.

The performance gap is caused by a Next.js Server Component that runs a full database connection setup on every cold start:

```ts
const db = new PrismaClient(); // Creates new pool on cold start
```

Show: the module-level singleton pattern for Prisma in Next.js (with the `global.prisma` trick to prevent multiple instances in dev with HMR), Vercel's edge function warm-up ping, and `prisma.$connect()` called eagerly in a startup file to pre-warm the connection pool before the first real request.""",

"""**Task (Code Generation):**
Build a `useResizeVirtualizer` that virtualizes items in a container where items have variable heights that can change after render:

```ts
const { virtualItems, totalHeight, measureRef } = useResizeVirtualizer({
  count: items.length,
  estimatedItemHeight: 60,
  overscan: 3,
});

<div style={{ height: totalHeight }}>
  {virtualItems.map(({ index, start }) => (
    <div ref={measureRef(index)} style={{ position: 'absolute', top: start }}>
      <ItemComponent item={items[index]} />
    </div>
  ))}
</div>
```

Show: the measurement strategy using `ResizeObserver` per item, updating the offset map when an item's height changes, recalculating all offsets below the changed item, and batching `ResizeObserver` callbacks to avoid layout thrashing.""",

"""**Debug Scenario:**
A developer tries to improve a page's INP by wrapping an expensive `onClick` handler with `startTransition`. The INP score doesn't improve.

```ts
const handleClick = () => {
  startTransition(() => {
    setExpensiveState(computeValue()); // still blocks
  });
};
```

`computeValue()` is a synchronous 400ms calculation that runs BEFORE `startTransition`'s callback. `startTransition` only defers STATE UPDATES and their resulting renders — it doesn't defer synchronous JavaScript execution.

Show: moving `computeValue()` into a Web Worker (async), using `useDeferredValue` for the result display, and the correct mental model: `startTransition` lets React interrupt renders, but JavaScript on the main thread before `setState` always blocks the interaction.""",

]

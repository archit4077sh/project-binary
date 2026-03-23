"""
snippets/q_performance.py — BATCH 5: 28 brand-new Performance questions
Zero overlap with batch1, batch2, batch3, or batch4 archives.
"""

Q_PERFORMANCE = [

"""**Task (Code Generation):**
Implement a `useIdlePreloader` that downloads resources during browser idle time:

```ts
useIdlePreloader({
  resources: [
    { type: 'script',  url: '/js/heavy-feature.js',  priority: 'low' },
    { type: 'image',   url: '/hero-fallback.jpg',     priority: 'high' },
    { type: 'fetch',   url: '/api/prefetch/catalog',  priority: 'medium' },
    { type: 'module',  url: '/js/analytics.js',       priority: 'low' },
  ],
  maxIdleTime: 50,    // yield if idle callback runs > 50ms
  onComplete: () => analytics.track('preload_done'),
});
```

Show: `requestIdleCallback` with deadline checking (`deadline.timeRemaining() < 5`), priority sorting (high first), `<link rel="preload">` injection for images/scripts, dynamic `import()` for modules, `fetch` with `cache: 'force-cache'` for API resources, and `cancelIdleCallback` on unmount.""",

"""**Debug Scenario:**
A dashboard page's server response time jumps from 200ms to 4.5s after adding a new "Related Posts" section that fetches from an external content API. The main content renders immediately but waits for the related posts fetch to complete:

```ts
// app/dashboard/page.tsx:
const [mainData, relatedPosts] = await Promise.all([
  getMainData(),
  getRelatedPosts(), // external API, 4.3s
]);
```

The page blocks on `getRelatedPosts()` even though it's non-critical. Show: moving `getRelatedPosts()` into a child Server Component wrapped in `<Suspense>`, showing a skeleton for related posts while the main content streams immediately, and `unstable_noStore()` to prevent caching the slow external call from blocking ISR.""",

"""**Task (Code Generation):**
Build a `createMemoSelector` factory (like Reselect) with automatic invalidation:

```ts
const selectFilteredProducts = createMemoSelector(
  [(state) => state.products, (state) => state.filter],
  (products, filter) => {
    // expensive computation:
    return products.filter(p =>
      p.category === filter.category && p.price <= filter.maxPrice
    );
  }
);

// Called 1000 times with same state: runs computation only ONCE
const filtered = selectFilteredProducts(state);
```

Show: the memoization using a tuple of last inputs + last result, the equality check for each input selector, cache invalidation when any input changes, TypeScript inference of the result type from the result function, and a `createMemoSelectorFamily` for parameterized selectors.""",

"""**Debug Scenario:**
A TypeScript app imports a large JSON file from the public API definition:

```ts
import apiSchema from './openapi.json'; // 2.3MB JSON file
```

Webpack bundles the entire JSON into the main chunk. Show: using `import('./openapi.json')` (dynamic import) to split it into a separate chunk,`fetch('/openapi.json')` at runtime to load it on demand without bundling, configuring Webpack's `Rule.type: 'asset/resource'` to emit the JSON as a separate HTTP-fetched asset, and TypeScript's `resolveJsonModule: false` to prevent type-checking huge JSON files (define an interface manually instead).""",

"""**Task (Code Generation):**
Implement a `useOffscreenCanvas` hook for CPU-intensive canvas rendering off the main thread:

```ts
const { canvasRef, postMessage } = useOffscreenCanvas({
  worker: new URL('./canvas.worker.ts', import.meta.url),
  init: () => ({ width: 800, height: 600 }),
  onMessage: (msg) => {
    if (msg.type === 'frameReady') updateFPS(msg.fps);
  },
});

// Trigger re-render:
postMessage({ type: 'drawFrame', data: frameData });

<canvas ref={canvasRef} />
```

Show: `canvas.transferControlToOffscreen()` to transfer the canvas to a Worker, the Worker receiving a `OffscreenCanvas` via `postMessage` with `transferable: [offscreenCanvas]`, TypeScript types for `OffscreenCanvas` (add `lib: ['DOM.Iterable', 'WebWorker']` to tsconfig), and a `resize` handler that posts new dimensions to the worker.""",

"""**Debug Scenario:**
A React Native app has smooth 60fps rendering in development but drops to 20fps in the production release build. The main difference: development uses the Hermes JS engine in debug mode; production uses Hermes in release mode with stricter GC.

Profiling shows frequent minor GC pauses caused by thousands of short-lived objects created by `items.map(i => ({ ...i, computed: transform(i) }))` in the render function — creating 5,000 new objects on every render.

Show: memoizing the transformation outside render with `useMemo([items])`, using in-place mutation on a stable array ref (read-only views instead of new objects), React Native's Hermes-specific profiling (chrome://inspect DevTools), and the `PureComponent` vs `React.memo` choice for list items in React Native.""",

"""**Task (Code Generation):**
Build a `useLazyWithPreload` hook that extends React.lazy with manual preloading:

```ts
const LazyAdminPanel = useLazyWithPreload(() => import('./AdminPanel'));

// Preload on hover (before user clicks):
<button
  onClick={() => navigate('/admin')}
  onMouseEnter={() => LazyAdminPanel.preload()}
>
  Admin Panel
</button>

// Standard lazy rendering:
<Suspense fallback={<Loading />}>
  <LazyAdminPanel />
</Suspense>
```

Show: the hook wrapping `React.lazy` with a side-effectful import call that starts network download, `preload()` storing the Promise so `React.lazy`'s factory reuses the same Promise, TypeScript types for the preloadable component, and a `LazyRoute` wrapper that calls `preload()` automatically when the route link enters the viewport.""",

"""**Debug Scenario:**
A developer uses `console.time('render')` / `console.timeEnd('render')` to measure a component's render time and gets 0.02ms, but the browser's Performance tab shows ~60ms for the same component path.

`console.time` measures JavaScript execution time ONLY — it doesn't include the browser's layout, paint, and composite phases that happen AFTER the JS completes. Show: using PerformanceObserver for `long-animation-frame` entries (Chrome 123+) that includes JS + rendering phases, the `PerformancePaintTiming` for FCP/LCP, and Chrome DevTools' Performance panel's "Rendering" flamechart for separating JS execution from layout/paint time.""",

"""**Task (Code Generation):**
Implement a `useRenderBudget` hook that automatically degrades component quality when renders take too long:

```ts
const { quality, frameTime } = useRenderBudget({
  budgets: {
    high:   { maxFrameTime: 8 },   // < 8ms: full quality
    medium: { maxFrameTime: 16 },  // < 16ms: reduced quality
    low:    { maxFrameTime: 33 },  // < 33ms: minimal quality
  },
  window: 5, // average over last 5 frames
});

// Usage:
<Chart
  resolution={quality === 'high' ? 1000 : quality === 'medium' ? 500 : 100}
  animations={quality === 'high'}
/>
```

Show: measuring frame time with `performance.now()` between `requestAnimationFrame` calls, rolling average over the last N frames, gradual quality degradation (hysteresis: require 3 consecutive good frames before upgrading quality), and auto-reset on inactivity.""",

"""**Debug Scenario:**
A Next.js API route that processes image uploads starts throwing `out of memory` errors in production after 10 days of running. Memory steadily grows and never decreases.

Investigation reveals the route reads uploaded images with `fs.readFileSync` into a `Buffer` that's stored in a module-level `Map` as a "processing cache":

```ts
const processingCache = new Map<string, Buffer>(); // never cleared!
```

Show: implementing TTL-based cache eviction (delete entries after 5 minutes using `setTimeout`), using streams (`fs.createReadStream`) instead of reading entire files into memory, `sharp`'s streaming API for image processing, and monitoring memory with `process.memoryUsage()` in a health endpoint.""",

"""**Task (Code Generation):**
Build a `useConnectionAwareQuality` hook that adapts media quality to network conditions:

```ts
const { videoQuality, imageQuality, shouldDisableAnimations } =
  useConnectionAwareQuality({
    qualities: {
      '4g':   { video: '1080p', image: 'full',    animations: true },
      '3g':   { video: '480p',  image: 'medium',  animations: true },
      '2g':   { video: null,    image: 'low',     animations: false },
      offline:{ video: null,    image: 'cached',  animations: false },
    },
  });
```

Show: `navigator.connection.effectiveType` and `navigator.connection.downlink`, the `change` event on `navigator.connection` for real-time updates, `navigator.onLine` + `online`/`offline` events for connectivity state, the `saves-data` check (`navigator.connection.saveData`), and `@media (prefers-reduced-data)` CSS alternative.""",

"""**Debug Scenario:**
A Node.js server handling server-side rendering creates a new `Intl.DateTimeFormat` object for every request to format dates, contributing to high CPU usage under load:

```ts
export function formatDate(date: Date, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric', month: 'long', day: 'numeric'
  }).format(date); // new object per call
}
```

`Intl.DateTimeFormat` construction is expensive. Show: caching `Intl.DateTimeFormat` instances by locale + options key using a `Map` (module-level, survives across requests), the LRU eviction for the cache (bounded at 100 entries), and benchmarking before/after with `node:perf_hooks`' `PerformanceObserver`.""",

"""**Task (Code Generation):**
Implement a `<ProgressiveImage>` component that shows a blurred placeholder while the full image loads:

```tsx
<ProgressiveImage
  src="/photos/mountain.jpg"
  lqip="/photos/mountain-lqip.jpg" // or base64 data URL
  alt="Mountain landscape"
  aspectRatio="16/9"
  onLoad={() => analytics.track('hero_image_loaded')}
/>
```

Show: loading the full image in a hidden `new Image()` JavaScript object, swapping `src` only after JS-native load completes (smooth transition), CSS `filter: blur(20px)` on the LQIP with `transform: scale(1.05)` to hide blur edges, `aspect-ratio` CSS to prevent layout shift before image loads, and the `loading="lazy"` + IntersectionObserver fallback for native lazy loading.""",

"""**Debug Scenario:**
A developer uses `React.lazy` + Webpack to split code by route, but `vite build --analyze` shows the `vendor` chunk is 1.8MB because React, lodash-es, and framer-motion are all in one chunk:

```ts
// vite.config.ts
build: {
  rollupOptions: {
    output: {
      manualChunks: undefined // default: vendor chunk strategy
    }
  }
}
```

Show: custom `manualChunks` that splits React into its own chunk (cached long-term), framer-motion into a separate animation chunk (only loaded on pages that animate), and the `splitVendorChunkPlugin` approach versus manual configuration, with before/after bundle size comparison.""",

"""**Task (Code Generation):**
Build a `useRAFState<T>` hook that batches state updates to animation frames (prevents over-rendering from rapid events):

```ts
const [scrollPos, setScrollPos] = useRAFState({ x: 0, y: 0 });

useEffect(() => {
  const handler = () => setScrollPos({ x: window.scrollX, y: window.scrollY });
  window.addEventListener('scroll', handler, { passive: true });
  return () => window.removeEventListener('scroll', handler);
}, []);
// Even though scroll fires 60+ times/sec, state updates are batched to one per frame
```

Show: the rAF-batched state update (cancel pending frame, request new frame that calls the real `setState`), the `useCallback` wrapper so `setScrollPos` is stable, and the cleanup with `cancelAnimationFrame` in the hook's `useEffect` return.""",

"""**Debug Scenario:**
A production server renders 50 requests per second. After adding `getServerSideProps` that loads translations from a YAML file using `js-yaml`, CPU spikes to 95%. Each request reads and parses a 200KB YAML file from disk:

```ts
export async function getServerSideProps(ctx) {
  const translations = yaml.load(fs.readFileSync('./i18n/en.yaml', 'utf8'));
  return { props: { translations } };
}
```

Show: parsing YAML once at server startup (module-level `const`), caching the parsed result in memory, serving it reference-only per request, handling hot-reload in development (watch the file with `fs.watch`), and converting YAML to JSON at build time for instant `require('./i18n/en.json')` (JSON.parse is 10x faster than YAML parse).""",

"""**Task (Code Generation):**
Implement a `useDebouncedQuery` hook that prevents redundant API calls while typing:

```ts
const { data, isLoading, debouncedQuery, cancelPending } = useDebouncedQuery({
  query,
  fetcher: (q) => api.search(q),
  debounce: 350,
  minLength: 2,       // don't fetch for very short queries
  deduplicate: true,  // skip fetch if query equals last successfully fetched query
  onError: (err) => toast.error('Search failed'),
});
```

Show: the debounce with `useRef`-held timer ID, the deduplication check (store last fetched query), cancellation of in-flight requests using `AbortController`, the `cancelPending()` function exposed to allow imperative cancellation, and TypeScript generic for the return data type.""",

"""**Debug Scenario:**
A web app built with Vite has a 3.2MB JavaScript bundle after `vite build`. Analysis shows `@sentry/browser` (500KB), `@aws-sdk/client-s3` (800KB), and `pdf-lib` (600KB) are all imported in the main entry file even though they're only used in specific features.

Show: moving Sentry initialization to a separate entry point loaded only in production (`import('./sentry-init').then(m => m.initSentry())`), lazy-loading the S3 client (`const { S3Client } = await import('@aws-sdk/client-s3')`) only when the upload feature is used, and making `pdf-lib` a separate chunk that's only downloaded when the user clicks "Export PDF", with bundle size validation in CI using `vite-bundle-visualizer`.""",

"""**Task (Code Generation):**
Build a `usePollingWithBackoff` hook that polls an API and slows down when errors occur:

```ts
const { data, status, resetBackoff } = usePollingWithBackoff({
  fetcher: () => api.getJobStatus(jobId),
  interval: 2000,
  backoff: {
    strategy: 'exponential',
    maxInterval: 30_000, // max 30s between polls after errors
    jitter: true,        // ± 20% jitter to spread load
  },
  stopWhen: (data) => data.status === 'complete' || data.status === 'failed',
  onComplete: (data) => handleJobComplete(data),
});
```

Show: `setInterval`-based polling, the exponential backoff multiplier on error, jitter calculation (`interval * (0.8 + Math.random() * 0.4)`), `stopWhen` predicate, cleanup on unmount, and `resetBackoff()` that clears error count and resets to initial interval.""",

"""**Debug Scenario:**
A Next.js 14 app using the App Router has every page as a Client Component (`'use client'`) because the team was unsure about Server vs Client Component boundaries. Lighthouse scores show 4.2MB of JavaScript on the network.

The team wants to migrate to Server Components. Show: identifying components that use `useState`, `useEffect`, `onClick` (must remain Client Components), components that only fetch data and render (can be Server Components), the "leaves of the tree" pattern (push `'use client'` as close to the browser-interactive parts as possible), using `<Suspense>` to stream server-rendered data, and expected JS bundle reduction after migration.""",

"""**Task (Code Generation):**
Implement a `WeakCache<K extends object, V>` that doesn't prevent garbage collection of its keys:

```ts
const cache = new WeakCache<Request, Response>({
  compute: async (req) => {
    return new Response(await generateContent(req));
  },
});

const res1 = await cache.get(requestObject);
const res2 = await cache.get(requestObject); // cached
// When requestObject is GC'd, the cached Response is also GC'd automatically
```

Show: `WeakMap`-based storage (keys are objects, GC'd when no other references exist), the `compute` factory for cache misses, handling concurrent requests for the same key (deduplicate with a `Map<K, Promise<V>>` of in-flight Promises), and `FinalizationRegistry` to track when keys are collected (for cache hit-rate logging).""",

"""**Debug Scenario:**
An e-commerce site's product listing page has a 95th-percentile server response time of 8 seconds. The median is 180ms. Investigation shows the slow responses correlate exactly with database cold connections — the connection pool is exhausted during traffic spikes.

```ts
const pool = new Pool({ max: 10 }); // only 10 concurrent connections
```

Show: increasing pool max with a guard (`max: Math.min(50, os.cpus().length * 5)`), implementing a queue for requests waiting for a connection (with timeout), adding `pool.on('connect')` and `pool.on('remove')` logging to measure pool pressure, using PgBouncer for transaction-mode pooling (allows thousands of Node connections to share 10 actual DB connections), and monitoring with `pool.totalCount`, `pool.idleCount`, `pool.waitingCount`.""",

"""**Task (Code Generation):**
Build a `useHydrationMismatch` debug hook that detects and logs server/client render differences in development:

```ts
// Development only:
useHydrationMismatch(componentName, {
  serverValue: serverRenderedContent,
  tolerance: 'whitespace', // ignore whitespace-only differences
  onMismatch: (diff) => {
    console.error(`[Hydration] ${componentName} mismatch:`, diff);
    reportToErrorTracking(diff);
  },
});
```

Show: comparing server-rendered HTML (`innerHTML` of a ref) with client-rendered output after hydration, the `useEffect` (client-only) that checks for differences, the tolerance modes (`exact`, `whitespace`, `attributes-only`), disabling in production (`process.env.NODE_ENV !== 'development'`), and using `MutationObserver` to detect DOM changes during hydration.""",

"""**Debug Scenario:**
A React app's bundle includes multiple copies of the same package. Running `npm ls react` shows:

```
my-app@1.0.0
├── react@18.2.0
└── my-component-lib@2.1.0
    └── react@17.0.2 ← second copy!
```

Two versions of React are bundled, causing "Invalid hook call" errors. Show: using Webpack's `resolve.alias` to force a single React version (`{ 'react': path.resolve('./node_modules/react') }`), fixing the root cause by adding React as a peer dependency in `my-component-lib` (not a direct dependency), running `npm dedupe` to flatten the dependency tree, and detecting the issue earlier with `npm-why react` and `duplicate-package-checker-webpack-plugin`.""",

"""**Task (Code Generation):**
Implement a `useFPS` hook that measures real-time frame rate and triggers callbacks on drops:

```ts
const { fps, avgFps, isDropping } = useFPS({
  sampleWindow: 60,           // average over last 60 frames
  dropThreshold: 45,          // fps below 45 = dropping
  onDrop: (fps) => {
    analytics.track('fps_drop', { fps });
    reduceQuality();
  },
  onRecover: () => restoreQuality(),
});
```

Show: the `requestAnimationFrame` loop that measures `1000 / (thisTimestamp - lastTimestamp)`, a circular buffer of the last N frame times for rolling average, the drop detection with hysteresis (require 3 consecutive drops before triggering), cleanup with `cancelAnimationFrame` on unmount, and displaying the FPS counter only in dev mode.""",

"""**Debug Scenario:**
A developer profiles a React app and finds that `useMemo` calls in their component are actually SLOWER than not memoizing. A component memoizes a simple string concatenation:

```ts
const displayName = useMemo(
  () => `${user.firstName} ${user.lastName}`,
  [user.firstName, user.lastName]
);
```

`useMemo` has overhead: dependency comparison + potential cache hit check on every render. For trivial computations (< 0.1ms), `useMemo` overhead (dependency array allocation, equality checks) exceeds the computation cost.

Show: the guidelines for when `useMemo` is worth it (computation > 1ms, or a stable reference needed by a downstream `React.memo`/`useMemo`/`useEffect`), removing `useMemo` for simple derived values, and using `React.memo` on the consumer instead if the real goal is preventing re-renders.""",

"""**Task (Code Generation):**
Build a `createSharedWorkerState<T>` for sharing state between multiple browser tabs without a server:

```ts
const [state, setState] = createSharedWorkerState('app-state', {
  initialState: { theme: 'light', notifications: [] },
  reducer: (state, action) => {
    switch (action.type) {
      case 'SET_THEME': return { ...state, theme: action.theme };
      case 'ADD_NOTIFICATION': return { ...state, notifications: [...state.notifications, action.notification] };
    }
  },
});

// In any tab:
setState({ type: 'SET_THEME', theme: 'dark' }); // updates ALL tabs instantly
```

Show: `SharedWorker` setup (one worker shared across all tabs), the worker receiving actions and broadcasting updated state to all connected ports, `localStorage` as a fallback when `SharedWorker` isn't supported, and React hook integration with `useSyncExternalStore`.""",

"""**Debug Scenario:**
A Node.js HTTP server has a consistent 50ms tail-latency spike every 30 seconds. Application metrics show no database queries or external API calls during those spikes — the event loop is simply blocked.

Investigation with `--prof` V8 profiler and `node --perf-basic-prof` reveals a `setInterval(() => compactLocalCache(), 30_000)` call that synchronously iterates 50,000 Map entries to evict stale entries — blocking the event loop for 48ms.

Show: moving the eviction to a background process using `worker_threads`, chunking the eviction into micro-tasks (`setImmediate` to yield between chunks), using a more efficient data structure (`DoublyLinkedList` + `Map` for O(1) LRU eviction instead of O(n) iteration), and `perf_hooks.monitorEventLoopDelay()` to measure event loop lag in production.""",

]

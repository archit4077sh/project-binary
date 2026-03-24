"""
snippets/q_performance.py — BATCH 6: 56 brand-new Performance questions
Zero overlap with batches 1-5 archives.
"""

Q_PERFORMANCE = [

"""**Task (Code Generation):**
Build a `useResourceHints` hook that injects preconnect/prefetch/preload link hints:

```ts
useResourceHints({
  preconnect: ['https://fonts.googleapis.com', 'https://cdn.example.com'],
  preload: [
    { href: '/fonts/inter.woff2', as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' },
    { href: '/hero.jpg', as: 'image' },
  ],
  prefetch: ['/api/dashboard', '/js/heavy-feature.js'],
});
```

Show: injecting `<link>` elements into `document.head`, deduplication (skip if already injected), cleanup on unmount, and the performance impact comparison (preconnect saves DNS+TCP+TLS, preload forces early fetch, prefetch is low-priority background fetch).""",

"""**Task (Code Generation):**
Implement a `createImageOptimizer` service for WebP/AVIF conversion and responsive `srcSet` generation:

```ts
const optimizer = createImageOptimizer({
  formats: ['avif', 'webp', 'jpeg'],
  sizes: [320, 640, 1024, 1920],
  quality: { avif: 60, webp: 75, jpeg: 85 },
  placeholderStrategy: 'blurhash',
});

const { src, srcSet, placeholder, sizes } = optimizer.optimize('/photos/hero.jpg');
```

Show: generating `srcSet` with `w` descriptors, `<picture>` with `<source type="image/avif">` and `<source type="image/webp">`, blurhash decoding to a CSS `background-image` for the LQIP placeholder, and `decoding="async"` attribute.""",

"""**Task (Code Generation):**
Build a `useParallelWorkers<In, Out>` hook for CPU-intensive work across multiple workers:

```ts
const { process, isProcessing, progress } = useParallelWorkers<ImageData, ProcessedImage>({
  workerUrl: '/workers/image-processor.js',
  poolSize: navigator.hardwareConcurrency ?? 4,
  taskQueue: images,
  onResult: (result, index) => setProcessed(prev => { prev[index] = result; }),
});

await process(imageDataArray);
```

Show: creating a pool of `Worker` instances, distributing tasks via a FIFO work queue (idle workers pick up tasks), `Transferable` objects for zero-copy image data transfer, progress tracking, and cleanup terminating all workers on unmount.""",

"""**Task (Code Generation):**
Implement a `createStreamingJSONParser` for processing large API responses without blocking the main thread:

```ts
const parser = createStreamingJSONParser<Product>({
  arrayPath: 'data.products',
  onItem: (product) => addToUI(product),
  onComplete: (total) => setLoading(false),
  chunkSize: 16_384,
});

const response = await fetch('/api/products/export');
await parser.parse(response.body!);
```

Show: reading the `ReadableStream` via `getReader()`, accumulating bytes and splitting on object delimiters, parsing each completed JSON object, yielding between chunks using `queueMicrotask`, and a `TransformStream`-based implementation as an alternative.""",

"""**Task (Code Generation):**
Build a `useAdaptiveLoading` hook that adjusts content quality based on device capability:

```ts
const { tier, shouldLoadVideos, imageQuality, animationEnabled } =
  useAdaptiveLoading({
    tiers: {
      high:   { minRam: 4, minCores: 4, connection: '4g' },
      medium: { minRam: 2, minCores: 2, connection: '3g' },
      low:    {},
    },
  });
```

Show: reading `navigator.deviceMemory`, `navigator.hardwareConcurrency`, `navigator.connection.effectiveType`, `window.matchMedia('(prefers-reduced-motion: reduce)').matches`, the tier scoring algorithm, and `SessionStorage` persistence.""",

"""**Task (Code Generation):**
Implement a `useProfiledRender` hook that measures component render performance in production:

```ts
function HeavyComponent() {
  const { startMark, endMark } = useProfiledRender('HeavyComponent', {
    sampleRate: 0.1,
    slowThreshold: 16,
    onSlowRender: (duration) => metrics.record('slow_render', { duration }),
  });
  startMark();
  const result = expensiveComputation();
  endMark();
  return <div>{result}</div>;
}
```

Show: `performance.mark()` and `performance.measure()` APIs, sampling via `Math.random() < sampleRate`, reading the measure duration from `PerformanceObserver`, and a production-safe approach that skips measurement when `sampleRate` doesn't pass.""",

"""**Task (Code Generation):**
Build a `createBundleAnalyzer` Vite plugin that enforces bundle size budgets in CI:

```ts
createBundleAnalyzer({
  budgets: {
    'main':         { maxKB: 150 },
    'vendor-react': { maxKB: 50 },
    'features/*':   { maxKB: 30 },
  },
  reporter: 'html',
  failOnExceed: true,
  compareWithBaseline: './bundle-baseline.json',
})
```

Show: the Vite plugin's `generateBundle` hook reading chunk sizes, comparing with budgets, glob pattern matching for chunk names, generating a baseline JSON on first run, and the delta comparison reporting size change vs last baseline.""",

"""**Task (Code Generation):**
Implement a `usePageTransitionProgress` hook that tracks Core Web Vitals for analytics:

```ts
const { ttfb, fcp, lcp, cls, fid } = usePageTransitionProgress({
  onMetric: (metric) => analytics.track('web_vital', {
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
  }),
});
```

Show: using the `web-vitals` library, `PerformanceObserver` for LCP and CLS, `PerformanceNavigationTiming` for TTFB, the `rating` thresholds (LCP good ≤2.5s, needs-improvement ≤4s, poor >4s), and attributing CLS to specific layout-shifting elements via `sources`.""",

"""**Task (Code Generation):**
Build a `useRequestDeduplicator<T>` that prevents concurrent duplicate HTTP requests:

```ts
const { get, invalidate } = useRequestDeduplicator({ cache: new Map(), maxAge: 5_000 });

// 50 simultaneous calls with the same key → 1 actual HTTP request:
const [u1, u2, u3] = await Promise.all([
  get('/api/user/1', fetchUser),
  get('/api/user/1', fetchUser),
  get('/api/user/1', fetchUser),
]);
```

Show: storing in-flight Promises by URL key (concurrent requests share one Promise), storing the resolved result for the `maxAge` period, `invalidate(url)` for cache busting, and TypeScript generics inferring return type from the fetcher function.""",

"""**Task (Code Generation):**
Build a `useIncrementalSearch<T>` hook that searches a large offline dataset without blocking the UI:

```ts
const { results, isSearching, cancel } = useIncrementalSearch({
  dataset: allProducts,     // 50,000 items
  searchFn: (q, item) => item.name.toLowerCase().includes(q),
  chunkSize: 500,
  maxResults: 50,
  debounce: 200,
});
```

Show: chunked processing using `requestIdleCallback`, early termination when `maxResults` is reached, cancelling the current search when the query changes (via a generation counter), updating `results` incrementally as each chunk completes, and Web Worker alternative for true parallelism.""",

"""**Task (Code Generation):**
Implement a `usePersistentSWR<T>` hook combining SWR with IndexedDB persistence:

```ts
const { data, error, isLoading } = usePersistentSWR<DashboardData>(
  '/api/dashboard',
  fetcher,
  {
    persistKey: 'dashboard-v2',
    maxAge: 24 * 60 * 60 * 1000,
    serialize: JSON.stringify,
    deserialize: JSON.parse,
  }
);
// Shows persisted data immediately, fetches fresh data in background
```

Show: reading from IndexedDB as initial data, writing to IndexedDB on successful fetch in `onSuccess`, a `maxAge` check on cached data, and the `idb` library for IndexedDB interaction.""",

"""**Task (Code Generation):**
Implement a `useMemoryPressureMonitor` hook that reacts to device memory pressure:

```ts
const { tier, pressure } = useMemoryPressureMonitor({
  onHighPressure: () => {
    clearImageCache();
    disableAnimations();
  },
  onLowPressure: () => restoreFeatures(),
  pollInterval: 10_000,
});
```

Show: the `performance.memory` API (Chrome-only: `usedJSHeapSize` / `jsHeapSizeLimit`), percentage thresholds (>80% = high pressure), `navigator.deviceMemory` for device RAM tier, and `FinalizationRegistry` for tracking when large objects are GC'd.""",

"""**Task (Code Generation):**
Build a `useNetworkQueueManager` that batches and prioritizes API requests:

```ts
const { enqueue, flush, queueLength } = useNetworkQueueManager({
  maxConcurrent: 4,
  priorityLevels: ['critical', 'high', 'normal', 'low'],
  deduplicateKey: (req) => `${req.method}:${req.url}`,
  retryOnFailure: 2,
});

enqueue({ url: '/api/save', method: 'POST', body: draft, priority: 'high' });
enqueue({ url: '/api/analytics', method: 'POST', body: event, priority: 'low' });
```

Show: the priority queue using multiple `Array<Request>` queues, a concurrency limiter (at most N in-flight requests), deduplication by key, retry scheduling, and pausing/flushing the queue based on `navigator.onLine`.""",

"""**Task (Code Generation):**
Build a `createVirtualScroller` for efficiently rendering millions of items as a flat list:

```ts
const scroller = createVirtualScroller({
  containerHeight: 600,
  itemHeight: (index) => index % 5 === 0 ? 80 : 48,  // variable heights
  totalItems: 2_000_000,
  renderItem: (index, style) => <Row key={index} style={style} data={data[index]} />,
  overscan: 5,
  onVisibleRangeChange: (start, end) => prefetchRange(start, end),
});
```

Show: computing cumulative height offsets for variable heights (binary search for visible range), the `onScroll` handler that updates `startIndex` and `endIndex`, absolute positioning of items, a `useVirtualScroller` React hook wrapping the imperative class, and dynamic item height measurement via `ResizeObserver`.""",

"""**Debug Scenario:**
A React app's Time to Interactive (TTI) is 8.8 seconds on 4G mobile. Lighthouse shows a 2.2MB JavaScript payload. A charting library (800KB) and 3D library (600KB) are in the main bundle but are only used on the Analytics page.

Show: dynamic import of both libraries inside the Analytics page component, code splitting via Webpack magic comments, `React.lazy` + `Suspense` wrapping of `<AnalyticsPage>`, and Vite's `rollupOptions.output.manualChunks` to separate these into named chunks.""",

"""**Debug Scenario:**
A Next.js app using `next/image` shows LCP of 4.2s. The hero image has default `loading="lazy"` which defers image discovery.

`loading="lazy"` defers the image fetch until near viewport, but the hero IS visible at initial load. Show: adding `priority` prop to the hero `next/image` which adds `rel="preload"`, `loading="eager"`, and `fetchpriority="high"` on the underlying `<img>`, and why only ONE image per page should receive `priority`.""",

"""**Debug Scenario:**
A Node.js Express API serving SSR pages has memory growing to 4GB after 2 hours:

```ts
const requestLog = new Map(); // module-level, never cleared

app.use((req, res, next) => {
  requestLog.set(req.id, { body: req.body, timestamp: Date.now() });
  next();
});
```

Show: removing the module-level accumulator, using a TTL-based cache that expires entries, `WeakMap` for request-keyed data that GC's automatically, and `node --inspect` + Chrome DevTools memory profiling to find heap retainers.""",

"""**Debug Scenario:**
A React component's `useEffect` makes 15 sequential API calls, causing a 12-second load on 3G:

```ts
useEffect(async () => {
  const user = await fetchUser();
  const orders = await fetchOrders(user.id);
  const products = await fetchProducts(); // waits for orders!
  const categories = await fetchCategories(); // waits for products!
}, []);
```

Show: grouping independent parallel calls with `Promise.all`, then fan-out for user-dependent data, and measuring the time savings (serial: sum of all calls; parallel: max of independent group + dependent calls).""",

"""**Debug Scenario:**
A Vite app's HMR takes 8 seconds per save because a custom plugin runs `eslint` synchronously in `transform`:

```ts
plugins: [{
  name: 'eslint-on-save',
  transform(code, id) {
    runEslintSync(id); // blocks HMR!
    return null;
  },
}]
```

Show: removing the blocking `transform` hook, moving ESLint to `vite-plugin-eslint` running asynchronously, using `eslint --cache` to only lint changed files, and `vite-plugin-checker` running type-checking and linting in a separate thread.""",

"""**Debug Scenario:**
A product page has CLS of 0.35 (poor). A banner ad loads after 1.5s and pushes content down 90px.

Show: pre-reserving space for the ad with `min-height: 90px` on the ad container, `content-visibility: auto` for off-screen sections, lazy-loading images with explicit `width` and `height` attributes, and the CLS contribution formula (`impact_fraction × distance_fraction`).""",

"""**Debug Scenario:**
A table with 5,000 rows renders in 800ms. `React.memo` doesn't help because the `columns` prop is defined inline:

```tsx
const columns = [{ key: 'name', label: 'Name' }, ...]; // new array each render
const MemoizedTable = React.memo(DataTable);
// Still 800ms because columns is a new reference every render
```

Show: moving `columns` outside the component or wrapping with `useMemo`, virtualizing rows using `react-window` or `@tanstack/virtual`, and `React.memo` on row components.""",

"""**Debug Scenario:**
A rich-text editor calls `localStorage.setItem()` on every keystroke, causing UI lag after 500 keystrokes:

```ts
editor.on('change', (content) => {
  localStorage.setItem('draft', JSON.stringify(content)); // blocks every keystroke
});
```

`localStorage.setItem` is synchronous and blocks the main thread. Show: debouncing saves to 1s after last keystroke, switching to `IndexedDB` (async, non-blocking), and `scheduler.postTask()` with `background` priority.""",

"""**Debug Scenario:**
Google Fonts are blocking render — showing in Lighthouse's render-blocking resources:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet">
```

Show: using `rel="preconnect"` for the font domain, loading the stylesheet as `rel="preload"` then switching to `stylesheet` (`onload="this.rel='stylesheet'"`), `font-display: swap` to show a fallback font immediately, and self-hosting fonts to avoid the third-party round-trip.""",

"""**Debug Scenario:**
Webpack build takes 3 minutes. `speed-measure-webpack-plugin` shows `babel-loader` takes 95s and `ts-loader` 45s.

Show: replacing `babel-loader` + `ts-loader` with `swc-loader` (Rust-based, 10-20x faster), enabling persistent caching (`cache: { type: 'filesystem' }`), splitting TypeScript type checking to `fork-ts-checker-webpack-plugin`, and upgrading to Next.js 13+ which uses Turbopack.""",

"""**Debug Scenario:**
500 components re-render when `notificationCount` updates because it's read from top-level state:

```tsx
function App() {
  const { notificationCount } = useAppStore(); // triggers root re-render → all 500 children
  return <Router>...</Router>;
}
```

Show: moving `notificationCount` to a localized `NotificationContext` consumed only by `<NotificationBell>`, `React.memo` on subtree roots, and Zustand's per-selector subscription (components only re-render when their specific slice changes).""",

"""**Debug Scenario:**
Production logs show "Script error." without stack traces for errors in CDN-hosted chunks:

```
Uncaught Error: Script error. (at https://cdn.example.com/chunk-abc.js:1)
```

Browser security blocks cross-origin error details without CORS. Show: adding `crossorigin="anonymous"` to `<script>` tags, configuring the CDN to send `Access-Control-Allow-Origin: *` on JS files, setting up Sentry with source maps, and `errorBoundary.getDerivedStateFromError` for React rendering errors.""",

"""**Debug Scenario:**
Every `MouseMove` triggers a full React re-render of 500 child components:

```tsx
function DraggablePanel() {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  return (
    <div onMouseMove={(e) => setPos({ x: e.clientX, y: e.clientY })}>
      {/* 500 children re-render on every mouse move */}
    </div>
  );
}
```

Show: moving `pos` to a `useRef` and applying transform directly to the DOM element (no re-render), using `requestAnimationFrame` to throttle DOM updates, and `React.memo` on children.""",

"""**Debug Scenario:**
A Next.js Pages Router page using `getServerSideProps` has P99 latency of 12 seconds — the DB query runs a table scan on a 1M-row table:

```ts
await db.query('SELECT * FROM products WHERE slug = $1', [params.slug]);
// No index on slug — O(n) scan!
```

Show: adding a B-tree index on `slug` (`CREATE INDEX CONCURRENTLY`), using `EXPLAIN ANALYZE` to verify the query plan, Prisma's `@@index([slug])` equivalent, query timeout middleware (fail fast after 2s), and serving a cached version while the query times out.""",

"""**Debug Scenario:**
React Query refetches data every mount because `staleTime` is not configured:

```ts
const { data } = useQuery({
  queryKey: ['user', id],
  queryFn: () => fetchUser(id),
  // staleTime defaults to 0 — data stale immediately
});
```

Show: setting `staleTime: 5 * 60 * 1000` (5 minutes), the global default override in `QueryClient`, the difference between `staleTime` (when to background-refetch) and `gcTime` (when to remove from cache), and `refetchOnMount: false` for static data.""",

"""**Debug Scenario:**
A CSS `transform`-only animation causes `Paint` events on every frame in Chrome DevTools:

```css
.moving-element { animation: slide 2s ease infinite; }
@keyframes slide { from { transform: translateX(0); } to { transform: translateX(100vw); } }
```

A sibling with high `z-index` forces the browser to repaint the whole stacking context. Show: promoting the animated element to its own layer with `will-change: transform`, isolating it with `isolation: isolate`, checking the DevTools Layers panel to confirm compositing, and measuring FPS before/after.""",

"""**Debug Scenario:**
An API endpoint serializing a 50MB response takes 2.3 seconds in `JSON.stringify`:

```ts
app.get('/api/catalog/all', async (req, res) => {
  const catalog = await db.products.findMany(); // 200,000 rows
  res.json(catalog); // JSON.stringify of 200K objects — 2.3s!
});
```

Show: streaming the response using `res.write('[')` + iterating rows while writing JSON chunks + `res.end(']')`, using a JSON streaming library, enabling gzip compression, and paginating the endpoint instead of fetching all rows at once.""",

"""**Debug Scenario:**
A Vite dev server takes 45 seconds to start because it's pre-bundling 3,000 node_modules:

Show: Vite's pre-bundling cache location (`.vite/deps/`), adding large infrequently-changed packages to `optimizeDeps.include`, excluding rarely-used packages with `optimizeDeps.exclude`, configuring `server.warmup.clientFiles` to pre-transform entry files, and the hardware impact of NVMe SSD vs HDD for file I/O.""",

"""**Debug Scenario:**
A `<textarea>` becomes janky because `useEffect` runs a 50ms text analysis on every keystroke:

```tsx
useEffect(() => {
  const result = analyzeText(text); // 50ms computation
  setAnalysis(result);
}, [text]); // every keystroke blocks main thread
```

Show: debouncing the analysis with `useDebounce(text, 300)`, moving `analyzeText` to a Web Worker, and `useDeferredValue(text)` which defers the analysis update (keeping text input responsive).""",

"""**Debug Scenario:**
Mobile FCP is 5.2 seconds because the CSS file is 800KB (uncompressed):

```html
<link rel="stylesheet" href="/styles/main.css" />
<!-- 800KB — all styles for all pages loaded upfront -->
```

Show: analyzing unused CSS with PurgeCSS or DevTools Coverage panel, critical CSS inlining (first-paint styles in `<style>` tag, rest deferred), enabling Brotli compression (compresses CSS ~80%), and checking that the server sends `Content-Encoding: br` header.""",

"""**Debug Scenario:**
A Next.js page with `revalidate = 60` does not revalidate after deployment — old content serves for hours:

```ts
export const revalidate = 60;
export default async function Page() { ... }
```

The CDN caches the static HTML indefinitely with `Cache-Control: immutable`. Show: configuring the CDN to respect `Cache-Control: s-maxage=60, stale-while-revalidate`, disabling CDN/edge caching for ISR routes, and using `unstable_cache` with `revalidate` for fetch-level caching.""",

"""**Debug Scenario:**
A GraphQL resolver has an N+1 problem — each blog post fetches its author in a separate DB query:

```ts
Post: {
  author: (post) => db.users.findUnique({ where: { id: post.authorId } })
  // For 50 posts: 50 separate DB queries!
}
```

Show: implementing DataLoader with a `batchLoadFn` (all user IDs fetched in one `WHERE id IN (...)`) query, DataLoader's automatic batching per tick, per-request DataLoader instantiation, and the `@dataloader` schema directive for automatic generation.""",

"""**Debug Scenario:**
React 18 concurrent mode shows "tearing" — components display inconsistent values from the same external store during a transition.

React 18 can pause and resume rendering, reading external stores at different points in time. Show: migrating from `useState` to `useSyncExternalStore`, the `getSnapshot` function (must return the same reference if data hasn't changed), and why built-in React state doesn't tear but external mutable stores do.""",

"""**Debug Scenario:**
An IntersectionObserver for lazy-loading images loads all images immediately on page load:

```ts
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) loadImage(entry.target);
  });
});
// All 100 images observed — all trigger isIntersecting: true on first callback!
```

All images are marked as intersecting on first observe if the page is short. Show: checking the initial `isIntersecting` on first observe, using `threshold: 0.01`, setting `rootMargin: '200px'` to pre-load within 200px, and `disconnect()` or `unobserve()` after loading each image.""",

"""**Debug Scenario:**
`useMemo` always recomputes because `activeFilters` (array from props) is a new reference every render:

```ts
const filteredItems = useMemo(
  () => items.filter(item => activeFilters.includes(item.category)),
  [items, activeFilters] // activeFilters: new array every parent render
);
```

Parent does: `<ProductList activeFilters={selectedCategories.filter(Boolean)} />` — `filter` creates a new array every render. Show: stabilizing in parent with `useMemo`, using a stringified comparison key as the dep, and `shallowEqual` as a custom dep comparison.""",

"""**Debug Scenario:**
A Next.js API route for PDF generation times out because `puppeteer` launches a new browser per request:

```ts
export async function POST(req: Request) {
  const browser = await puppeteer.launch(); // ~5s cold start each time
  const page = await browser.newPage();
  const pdf = await page.pdf({ format: 'A4' });
  await browser.close();
  return new Response(pdf);
}
```

Show: creating a shared browser instance at module level that persists across requests, using `browser.newPage()` per request, graceful reconnection if the browser crashes, and `puppeteer-cluster` for automatic page pool management with concurrency limits.""",

"""**Debug Scenario:**
A React component has `useCallback` with empty deps but the function still reads stale state:

```ts
const handleSave = useCallback(async () => {
  await api.save(formData); // formData is always the initial value!
}, []); // empty deps — stale closure
```

`formData` is captured at the time `useCallback` was first called and never updated. Show: adding `formData` to the deps array, using a `useRef` to hold the latest `formData` (`formDataRef.current = formData`) and reading `formDataRef.current` inside the callback, and the `useEventCallback` pattern from stable-refs.""",

"""**Debug Scenario:**
A production Next.js app suddenly shows much slower TTFB (1.2s instead of 80ms) after a dependency update. The hot path is hitting `bcrypt.hash()` on every request:

```ts
export async function middleware(req: NextRequest) {
  const token = req.headers.get('authorization');
  const isValid = await verifyToken(token); // calls bcrypt.compare internally!
}
```

Middleware runs on EVERY request. `bcrypt.compare` is intentionally slow (10+ rounds). Show: switching to a fast HMAC signature verification (`crypto.timingSafeEqual` with SHA-256) for token validation in middleware, keeping bcrypt only for password hashing at login-time, and the security trade-off (bcrypt for passwords, HMAC for session tokens).""",

"""**Debug Scenario:**
A developer finds that `React.Suspense` causes their app to flash a loading spinner briefly when switching between pre-loaded routes:

```tsx
<Suspense fallback={<PageSpinner />}>
  <Routes>
    <Route path="/home" element={<HomePage />} />
    <Route path="/about" element={<AboutPage />} />
  </Routes>
</Suspense>
```

Even though data is cached, React temporarily shows the `fallback` during the transition render. Show: wrapping route navigation in `startTransition` (React defers showing the fallback if the transition resolves quickly), the `useDeferredValue` alternative, and the difference between concurrent transitions (may show stale content briefly) vs non-concurrent (always shows fallback).""",

"""**Debug Scenario:**
A `WeakRef`-based cache is not behaving as expected — cached values are immediately garbage collected even though they are still referenced:

```ts
const cache = new Map<string, WeakRef<ComputedResult>>();
cache.set(key, new WeakRef(result));
// later:
cache.get(key)?.deref() // returns undefined immediately!
```

The `result` object has no other strong references — it was passed to `new WeakRef` and immediately became GC-eligible. Show: ensuring the original `result` variable is still reachable in the calling scope when the `deref()` is called, understanding that GC can run between the `new WeakRef()` call and `deref()` in production V8, and using `FinalizationRegistry` to remove dead WeakRef entries from the Map.""",

"""**Debug Scenario:**
A developer notices that server-side rendered HTML is significantly larger than necessary — each page includes a 200KB `window.__NEXT_DATA__` JSON blob even for simple static pages:

```html
<script id="__NEXT_DATA__" type="application/json">
{"props":{"pageProps":{"allProducts": [/* 500 products × 400 bytes each = 200KB */]}}}
</script>
```

The entire product catalog is serialized into `pageProps` even though only 10 products display above the fold. Show: filtering props server-side to include only immediately-needed data, using `generateStaticParams` with selective data, fetching additional data client-side with React Query, and the `unstable_serialize` trick to avoid double-fetching.""",

]

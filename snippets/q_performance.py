"""
snippets/q_performance.py — BATCH 7: 56 brand-new Performance questions
Zero overlap with batches 1-6 archives.
"""

Q_PERFORMANCE = [

'''**Task (Code Generation):**
Implement a `createLazyImage` component with LQIP (Low Quality Image Placeholder) and progressive reveal:

```tsx
<LazyImage
  src="/photos/hero.jpg"
  lqip="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."  // 20-byte blurry thumbnail
  width={1200}
  height={630}
  alt="Mountain landscape"
  blurAmount={20}
  transitionDuration={400}
  onLoad={() => trackImageLoad('hero')}
/>
```

Show: the placeholder `<img>` with the base64 LQIP shown immediately, loading the full image via `new Image()` then swapping on `load`, CSS `filter: blur()` transition from blurry to sharp, and generating the LQIP using `sharp` on the Node.js build side (resize to 20px → toBuffer → base64 encode).''',

'''**Task (Code Generation):**
Build a `createPrefetchStrategy` for predictive resource loading based on hover intent:

```ts
const prefetcher = createPrefetchStrategy({
  hoverDelay: 100,      // ms hover before prefetching
  prefetchLinks: true,   // For anchor hrefs
  prefetchData: true,    // For API data
  concurrency: 3,        // Max 3 simultaneous prefetch requests
  cooldown: 5_000,       // Don't re-prefetch same URL within 5s
  cacheStrategy: 'memory-first',
});

// Auto-instruments all <a> elements:
prefetcher.observe(document.body);

// Manual trigger:
prefetcher.on('#product-card', {
  link: '/products/abc',
  data: () => fetch('/api/products/abc').then(r => r.json()),
});
```

Show: `pointerenter` + `setTimeout` to detect intent (cancel on `pointerleave`), `<link rel="prefetch">` for navigation, `fetch` with low-priority header (`fetchpriority: 'low'`) for data, the in-memory dedup set, and cleanup with `IntersectionObserver` to stop observing off-screen elements.''',

'''**Task (Code Generation):**
Implement a `createWorkerPool` for CPU-intensive tasks using Web Workers:

```ts
const workerPool = createWorkerPool('/workers/image-processor.worker.js', {
  size: navigator.hardwareConcurrency ?? 4,
  maxQueueSize: 50,
  taskTimeout: 30_000,
});

// Process images using idle workers:
const processed = await workerPool.run({
  command: 'resize',
  imageBuffer: file.arrayBuffer(),
  targetWidth: 800,
}, { transferable: [imageBuffer] });

await workerPool.terminate(); // Graceful shutdown
```

Show: the `Worker` instances array, a task queue drained to available workers, `Transferable` objects (`ArrayBuffer`, `ImageBitmap`) for zero-copy transfers, worker `terminate()` on timeout, and error propagation back to the main thread via `postMessage({ error: ... })`.''',

'''**Task (Code Generation):**
Build a `createResponseCache` for edge function caching with stale-while-revalidate:

```ts
export default async function handler(req: Request) {
  return withCache(req, {
    cacheControl: 'public, max-age=60, stale-while-revalidate=600',
    vary: ['Accept-Language', 'Accept-Encoding'],
    cacheKey: (req) => `${req.url}::${req.headers.get('Accept-Language')}`,
    compute: async () => {
      const data = await fetchDataFromDB();
      return Response.json(data);
    },
    store: cloudflareKV,  // Edge KV store
  });
}
```

Show: the `Cache-Control: stale-while-revalidate` header semantics (serve stale immediately, update cache in background), Cloudflare KV `get`/`put` with TTL, the `Vary` header for content negotiation, and background revalidation using `ctx.waitUntil(revalidate())` in Cloudflare Workers.''',

'''**Task (Code Generation):**
Implement a `createStreamingSSR` setup for React 18 streaming with selective hydration:

```tsx
// server.tsx:
app.get('*', async (req, res) => {
  res.setHeader('Content-Type', 'text/html');
  res.setHeader('Transfer-Encoding', 'chunked');

  const { pipe, abort } = renderToPipeableStream(
    <App url={req.url} />,
    {
      bootstrapScripts: ['/static/main.js'],
      onShellReady() { pipe(res); },
      onShellError(err) { res.status(500); res.send('<!DOCTYPE html><h1>Error</h1>'); },
      onAllReady() { /* unused — we use streaming, not buffered */ },
      onError(err) { console.error(err); },
    }
  );

  req.on('close', abort);
  setTimeout(abort, 10_000); // Abort after 10s
});
```

Show: React 18's `renderToPipeableStream`, the shell (nav, layout) streamed first, `<Suspense>` boundary streaming (placeholders replaced with content as data resolves), selective hydration (`<Suspense>` with `fetchpriority`), and why streaming improves TTFB without hurting TBT.''',

'''**Task (Code Generation):**
Build a `createCriticalCSS` extractor that inlines above-the-fold styles:

```ts
const criticalCSS = await extractCriticalCSS({
  html: renderToString(<App url='/' />),
  css: readFileSync('./dist/styles.css', 'utf-8'),
  viewport: { width: 1440, height: 900 },
  inlineThreshold: 10_000,  // Inline if <10KB, else preload
});

// Result:
// criticalCSS.inline: styles for above-the-fold elements
// criticalCSS.preload: remaining styles as <link rel="preload">
// criticalCSS.html: modified HTML with inline <style> and preload link
```

Show: the `critical` npm package approach, the pure-JS fallback using `JSDOM` + `css-select` to find rendered elements and match CSS selectors, inlining via a `<style>` tag in `<head>`, and `<link rel="preload" as="style" onload="this.rel='stylesheet'">` for the non-critical CSS.''',

'''**Task (Code Generation):**
Implement a `createCompressedFetch` utility that automatically compresses request bodies:

```ts
const response = await compressedFetch('/api/large-payload', {
  method: 'POST',
  body: JSON.stringify(largePayload),    // 500KB JSON
  compress: 'gzip',                      // Compress to ~50KB
  decompress: 'auto',                    // Auto-detect response compression
});

// Also wraps the Response to auto-decompress:
const data = await response.json(); // Works transparently
```

Show: `CompressionStream` for gzip/deflate in the browser (`new CompressionStream('gzip')`), `ReadableStream` piping to the compression stream, setting `Content-Encoding: gzip` header, server-side decompression middleware (Express `compression()` package), and the `Accept-Encoding: gzip, deflate, br` request header convention.''',

'''**Task (Code Generation):**
Build a `createFontSubsetter` for optimizing web font loading to only the characters actually used:

```ts
const subsets = await createFontSubsetter({
  fonts: [
    { family: 'Inter', src: './public/fonts/Inter.woff2', weight: '400 700' },
  ],
  html: await getAllPageHTML(),  // Scan all pages for characters used
  characters: {
    include: 'auto',    // Auto-detect from HTML
    extra: '→←•…"" ''', // Always include these
  },
  output: './public/fonts/subsets/',
  format: ['woff2'],
});

// Creates: Inter-subset-U+0020-007F.woff2 (Basic Latin)
//          Inter-subset-U+2010-2027.woff2 (Punctuation)
```

Show: the `fonttools` / `glyphhanger` / `pyftsubset` approach, `unicode-range` CSS descriptor for automatic subset selection, and measuring the size reduction (Inter Regular: 380KB → 45KB for English-only subset).''',

'''**Task (Code Generation):**
Implement a `createJavascriptProfiler` for production performance monitoring using the User Timing API:

```ts
const profiler = createJavascriptProfiler({
  enabled: process.env.NODE_ENV === 'production',
  sampleRate: 0.05,  // Profile 5% of users
  reportTo: 'https://analytics.example.com/perf',
  measures: [
    'checkout-flow',
    'search-results',
    'initial-render',
  ],
});

profiler.mark('checkout-start');
await processCheckout();
profiler.measure('checkout-flow', 'checkout-start');
// Sends: { name: 'checkout-flow', duration: 234, p50, p95, userAgent }
```

Show: `performance.mark()` and `performance.measure()`, reading `PerformanceObserver` for measures, the `PerformanceLongTaskTiming` API for detecting tasks >50ms, batching reports with `navigator.sendBeacon`, and sampling with `Math.random() < sampleRate`.''',

'''**Task (Code Generation):**
Build a `createAsyncBatcher<T, R>` for coalescing multiple async calls into a single batched request:

```ts
const getUserById = createAsyncBatcher<string, User>({
  batchFn: async (ids) => {
    const users = await fetch('/api/users/batch', {
      method: 'POST',
      body: JSON.stringify({ ids }),
    }).then(r => r.json());
    return ids.map(id => users.find(u => u.id === id) ?? null);
  },
  maxBatchSize: 100,
  maxWait: 16,  // Batch requests within the same frame
  cacheResults: true,
});

// Called from 50 components simultaneously:
const user = await getUserById('u1'); // Batched into one request with all other IDs
```

Show: the `DataLoader` pattern, collecting calls within the `maxWait` window using `setTimeout`, `Map<key, { resolve, reject }>` for per-key deferred promises, the return order guarantee (return values must align with input order), and the in-memory cache layer.''',

'''**Task (Code Generation):**
Implement a `createPerformanceBudget` checker for CI/CD pipeline:

```ts
const budgetResult = await checkPerformanceBudget({
  url: 'https://staging.example.com',
  budgets: [
    { metric: 'first-contentful-paint',  max: 1500 },
    { metric: 'largest-contentful-paint', max: 2500 },
    { metric: 'total-blocking-time',      max: 200 },
    { metric: 'cumulative-layout-shift',  max: 0.1 },
    { metric: 'bundle-size',              max: 200_000 },
    { metric: 'image-size',              max: 100_000 },
  ],
  runs: 3,
  device: 'mobile',
  throttling: { cpu: 4, network: '3G' },
});

if (!budgetResult.passed) process.exit(1);
```

Show: running Lighthouse programmatically (`lighthouse(url, options, config)`), averaging metrics over multiple runs, the Lighthouse CI config format, GitHub Actions integration for PR comments with budget failures, and `bundlemon` for bundle size budgets.''',

'''**Task (Code Generation):**
Build a `createImageSprite` generator for combining icons into a single image sprite:

```ts
const sprite = await createImageSprite({
  inputDir: './src/icons/*.svg',
  output: './public/sprites/',
  formats: ['svg-sprite', 'css-sprite'],
  prefix: 'icon-',
  optimize: true,
});

// Output CSS:
// .icon-arrow { background-position: -40px 0; width: 24px; height: 24px; }
// .icon-user  { background-position: -64px 0; width: 24px; height: 24px; }

// SVG Sprite usage:
<svg><use href="/sprites/icons.svg#icon-arrow"></svg>
```

Show: reading SVG files with `glob`, combining into an SVG `<defs>` sprite with `<symbol>` elements, calculating sprite sheet positions for PNG sprites, generating corresponding CSS classes, and the trade-off between SVG sprites (scalable, CSS-styleable) vs PNG sprites (wider compat).''',

'''**Task (Code Generation):**
Implement a `createNetworkAdaptiveLoading` strategy for serving different content based on connection quality:

```ts
const loadingStrategy = createNetworkAdaptiveLoading({
  dataSaver: {
    images: 'low',      // Serve lower resolution
    video: 'disabled',  // No autoplay video
    prefetch: false,    // No prefetching
    animations: false,  // No decorative animations
  },
  '2g': { ... similar ... },
  '3g': { images: 'medium', video: 'enabled', prefetch: true, animations: false },
  '4g': { images: 'high',   video: 'enabled', prefetch: true, animations: true },
});

// Usage in React:
const { strategy } = useNetworkAdaptiveLoading(loadingStrategy);
<img srcSet={strategy.images === 'high' ? highDPI : standardDPI} />
```

Show: `navigator.connection.effectiveType` and `navigator.connection.saveData`, the `Network Information API` with `change` event for dynamic updates, CSS `@media (prefers-reduced-data)`, and SSR-safe defaults (assume high quality, degrade client-side).''',

'''**Task (Code Generation):**
Build a `createMemoryOptimizedList` for rendering large datasets without virtualization using pagination chunking:

```tsx
const { visibleItems, loadMore, isComplete, totalLoaded } =
  useMemoryOptimizedList({
    items: allItems,           // 100,000 items
    initialChunkSize: 50,
    chunkSize: 25,
    renderOnIdle: true,        // Use requestIdleCallback to expand chunks
    onChunkRender: (chunk) => analytics.track('chunk-rendered', { size: chunk.length }),
  });

return (
  <>
    {visibleItems.map(item => <Item key={item.id} item={item} />)}
    {!isComplete && <button onClick={loadMore}>Load more ({totalLoaded}/{allItems.length})</button>}
  </>
);
```

Show: `requestIdleCallback` for incremental rendering (render chunk during idle frames, `{ timeout: 300 }` for max latency), `window.requestAnimationFrame` fallback for browsers without `requestIdleCallback`, `useTransition` for React 18's non-blocking chunk expansion, and cleanup of pending idle callbacks on unmount.''',

'''**Task (Code Generation):**
Implement a `createRenderProfiler` HOC and hook for measuring component render performance in production:

```tsx
// HOC usage:
const ProfiledProductList = withRenderProfiler(ProductList, {
  name: 'ProductList',
  threshold: 16,    // Log renders taking >16ms (over one frame budget)
  sampleRate: 0.1,
  reportTo: sendToAnalytics,
});

// Hook usage:
function HeavyComponent() {
  const renderTime = useRenderProfiler('HeavyComponent', { threshold: 16 });
  // ...
}
```

Show: measuring render time with `performance.now()` in `useRef` (before render) vs `useEffect` (after commit), `React.Profiler` component as the official API, the `onRender` callback receiving `actualDuration` and `baseDuration`, and why measuring in production requires opt-in (React Profiler has overhead in production unless explicitly enabled).''',

'''**Debug Scenario:**
A website's Lighthouse score drops from 95 to 45 after adding a cookie consent banner that blocks the main thread for 800ms:

```js
// cookie-banner.js (vendor, loaded synchronously):
<script src="https://cdn.example.com/cookie-consent.js"></script>
// Blocks HTML parsing + main thread for 800ms!
```

Show: adding `defer` or `async` attribute to move the script off the critical path, checking if the vendor supports loading as an ES module (`<script type="module">`), delaying initialization until after `DOMContentLoaded`, wrapping in a `setTimeout(init, 0)` to yield the main thread, and using `scheduler.yield()` (Chrome 115+) for cooperative scheduling within long tasks.''',

'''**Debug Scenario:**
A Next.js app's bundle size grew from 120KB to 890KB after one PR. The change added a date picker component:

```tsx
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css'; // 50KB CSS!

// react-datepicker ships with all date-fns locales bundled:
// ~700KB of locale data for 40+ languages, but app only uses en-US
```

Show: importing only the needed locale (`import { registerLocale } from 'react-datepicker'; import enUS from 'date-fns/locale/en-US'`), using a lighter alternative (`react-day-picker` at 18KB), dynamic import with `React.lazy` so the picker only loads when opened, and `webpack-bundle-analyzer` to find the bloat.''',

'''**Debug Scenario:**
A PWA's service worker caches are storing 400MB on users' devices because all API responses are cached without size limits:

```js
// sw.js:
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.open('api-cache').then(cache =>
      cache.match(event.request) || fetch(event.request).then(response => {
        cache.put(event.request, response.clone()); // No size limit, no TTL!
        return response;
      })
    )
  );
});
```

Show: checking `Response.headers.get('Content-Length')` before caching (skip if > 100KB), the `StorageManager.estimate()` API for monitoring quota usage, evicting old entries (implement LRU using `caches.open` + `cache.keys()` + `cache.delete()`), Workbox's built-in `CacheFirst` strategy with `maxEntries` and `maxAgeSeconds` plugins, and `navigator.storage.persist()` for durable cache that resists eviction.''',

'''**Debug Scenario:**
A React app's FID (First Input Delay) is 800ms — users notice the page is unresponsive right after load:

```js
// main.js (first script to execute):
const data = processAllProducts(rawProducts); // 600ms synchronous processing!
const store = createStore(data);
ReactDOM.createRoot(root).render(<App store={store} />);
```

A 600ms synchronous computation blocks the main thread immediately, making the page unresponsive to user input right after the JS loads. Show: moving heavy processing to a Web Worker (`worker.postMessage(rawProducts); worker.onmessage = e => createStore(e.data)`), using React's `startTransition` to defer store initialization, streaming the data from the server in smaller chunks instead of one large payload, and using FID's successor — INP (Interaction to Next Paint).''',

'''**Debug Scenario:**
A developer's `React.memo` comparison causes layout thrashing because it reads from `getBoundingClientRect` in the comparison function:

```tsx
const MemoizedList = React.memo(ListComponent, (prev, next) => {
  const el = document.querySelector('.list-container');
  const { height } = el.getBoundingClientRect(); // Forces layout!
  return height === prev.containerHeight; // Reads DOM during render
});
```

`getBoundingClientRect()` forces layout (reflow) — called from a comparison function that runs during React's render phase, this causes layout thrashing on every render cycle. Show: removing DOM reads from the comparison function, using a `ResizeObserver` in a `useEffect` to track container height (stored in state/ref), and keeping comparison functions pure and fast.''',

'''**Debug Scenario:**
A Vercel deployment's Edge middleware runs on every request, including static assets, adding 30ms latency:

```ts
// middleware.ts:
export function middleware(request: NextRequest) {
  const token = request.cookies.get('session');
  if (!token) return NextResponse.redirect('/login');
  return NextResponse.next();
}

// No matcher — runs on /favicon.ico, /_next/static/*, /images/* too!
export const config = {}; // Missing matcher!
```

Show: adding a `matcher` to exclude static files:

```ts
export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|images/).*)'],
};
```

And the performance impact: Edge middleware adds ~20-40ms even for simple checks — static assets should bypass it entirely.''',

'''**Debug Scenario:**
A website's CLS (Cumulative Layout Shift) score is 0.35 — the buy button jumps after the font loads:

```css
body { font-family: 'CustomFont', Arial, sans-serif; }
/* CustomFont has different metrics than Arial — text reflows on load */
```

Font swap causes layout shifts because the fallback font has different metrics (ascender, descender, cap height). Show: using `font-display: optional` (no flash, no shift — use fallback if font not in cache), `size-adjust`, `ascent-override`, `descent-override` CSS descriptor to match fallback font metrics to custom font, `<link rel="preload" as="font">` for critical fonts, and the `Font Loading API` to control when fonts are applied.''',

'''**Debug Scenario:**
A WebGL canvas animation drops to 15fps on mobile because it redraws even when the scene hasn't changed:

```js
function renderLoop() {
  drawScene(gl, scene); // Redraws every frame — 60fps even when static!
  requestAnimationFrame(renderLoop);
}
```

Show: adding a `dirty` flag (`let dirty = false`) set when scene data changes, skipping the draw call in `renderLoop` if `!dirty` (idle frames: just `requestAnimationFrame` without drawing), using `scene.addEventListener('change', () => dirty = true)`, `cancelAnimationFrame` when the tab is hidden (`document.addEventListener('visibilitychange', ...)`), and `performance.now()` throttling to cap at 60fps on high-refresh-rate screens.''',

'''**Debug Scenario:**
A developer's Express server handling file uploads blocks all other requests because `multer` stores files in memory:

```ts
const upload = multer({ storage: multer.memoryStorage() });

// Uploading a 500MB file blocks the entire process:
// Other requests queue up waiting for the upload to finish
```

Node.js is single-threaded — a 500MB file in memory doesn't block the event loop (I/O is async), but it causes memory pressure that triggers GC pauses. Show: using `multer.diskStorage()` to stream to disk instead of memory, setting `limits: { fileSize: 50 * 1024 * 1024 }` (50MB max), streaming directly to S3 with `multer-s3-transform`, and `busboy` for streaming multipart processing without staging the whole file in memory.''',

'''**Debug Scenario:**
A Prisma ORM query fetches 10,000 rows even though only 10 are needed, because `findMany` is called without limits:

```ts
const products = await prisma.product.findMany({
  where: { category: 'electronics' },
  // Missing: take, skip, cursor
});
// Returns ALL 10,000 electronics products into memory!
```

Show: always using `take` (page size) and `skip` or `cursor` for pagination, Prisma's cursor-based pagination for stable paging on frequently-updated data, the `count` query to get total before fetching pages, and `prisma.$queryRaw` with `LIMIT` when the ORM abstraction isn't expressive enough.''',

'''**Debug Scenario:**
A developer's React component re-renders 400 times per second because a `Date.now()` call is in the render path:

```tsx
function LiveClock() {
  const [_, forceUpdate] = useReducer(x => x + 1, 0);

  useEffect(() => {
    const id = setInterval(forceUpdate, 1000);
    return () => clearInterval(id);
  }, []);

  return <time>{new Date().toLocaleTimeString()}</time>;
}
// This is correct (1 render/second). But...

function ParentWithBug() {
  const now = Date.now(); // Evaluated every render!
  if (now - lastAction > 5000) showIdleBanner();
  // Every child state change triggers a Parent render → Date.now() → logic runs
}
```

Show: moving side effects and time checks to `useEffect` or event handlers (not render body), the pattern of keeping renders pure (no side effects, no non-deterministic calls), and `performance.now()` vs `Date.now()` for measuring elapsed time.''',

'''**Debug Scenario:**
A developer's Next.js page is not getting ISR (Incremental Static Regeneration) updates in production — the page never refreshes:

```ts
export async function getStaticProps() {
  const data = await getData();
  return {
    props: { data },
    revalidate: 60, // Should update every 60 seconds
  };
}
```

ISR updates happen on the NEXT request after the `revalidate` window — not on a timer. If no users visit the page, it never revalidates. Show: understanding the on-demand revalidation trigger model, using `res.revalidate('/some-page')` in an API route for immediate invalidation (Next.js On-Demand ISR), and `revalidatePath`/`revalidateTag` in the App Router.''',

'''**Debug Scenario:**
A developer's Tailwind CSS build takes 45 seconds in development because JIT scan is checking all files in `node_modules`:

```js
// tailwind.config.js:
module.exports = {
  content: ['**/*.{js,jsx,ts,tsx}'],  // Matches node_modules/**!
};
```

The glob `**/*.tsx` without excluding `node_modules` makes Tailwind scan hundreds of thousands of files. Show: the correct content config:

```js
content: ['./src/**/*.{js,jsx,ts,tsx}', './app/**/*.{js,jsx,ts,tsx}'],
```

And adding `'!**/node_modules/**'` exclusion, using the `raw` content option for dynamically constructed class names, and enabling Tailwind CSS `watch` mode's incremental scanning.''',

'''**Task (Code Generation):**
Build a `createAdaptiveLoadingHook` that detects device capabilities and adjusts quality settings:

```tsx
const {
  tier,           // 'low' | 'mid' | 'high'
  usesDataSaver,
  isSlowCPU,
  deviceMemory,
  effectiveType,
  preferReducedMotion,
} = useDeviceCapabilities();

// In a 3D scene component:
const quality = {
  low:  { shadows: false, antialias: false, maxParticles: 100 },
  mid:  { shadows: false, antialias: true,  maxParticles: 500 },
  high: { shadows: true,  antialias: true,  maxParticles: 2000 },
}[tier];
```

Show: `navigator.deviceMemory` API (GB RAM), `navigator.hardwareConcurrency` (CPU cores), `navigator.connection.effectiveType`, `window.matchMedia('(prefers-reduced-motion: reduce)')`, combining signals into a tier classification, and SSR-safe defaults.''',

'''**Task (Code Generation):**
Implement a `createAtomicWrite` pattern for safe concurrent file writes in Node.js:

```ts
const safeWriter = createAtomicWrite({
  tmpDir: '/tmp/atomic-writes',
  fsync: true,          // Flush to disk before moving (data integrity)
  maxRetries: 3,
  retryDelay: 100,
});

// Write safely — uses temp file + atomic rename:
await safeWriter.write('/data/config.json', JSON.stringify(config));
// Process: write to /tmp/atomic-writes/config-tmp → fsync → rename to /data/config.json

// Read safely — handles concurrent reads during write:
const config = await safeWriter.read('/data/config.json');
```

Show: `fs.writeFile` to a temp file, `fs.fsync` for durability, `fs.rename` (atomic on POSIX systems), handling the EXDEV error (cross-device rename: copy+delete fallback), and a `reader-writer lock` for high-concurrency scenarios.''',

'''**Task (Code Generation):**
Build a `createPaintWorklet` for GPU-accelerated custom CSS paint using the Houdini Paint API:

```js
// paint-worklet.js (runs in separate worklet thread):
class DiagonalLinesWorklet {
  static get inputProperties() { return ['--line-color', '--line-spacing', '--line-width']; }

  paint(ctx, size, properties) {
    const color   = properties.get('--line-color').toString();
    const spacing = parseInt(properties.get('--line-spacing'));
    const width   = parseInt(properties.get('--line-width'));

    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    for (let i = -size.height; i < size.width + size.height; i += spacing) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i + size.height, size.height);
      ctx.stroke();
    }
  }
}
registerPaint('diagonal-lines', DiagonalLinesWorklet);
```

Show: `CSS.paintWorklet.addModule('./paint-worklet.js')` registration, CSS usage (`background: paint(diagonal-lines)`), custom properties for parameterization, `@supports (background: paint(id))` detection, and the perf benefit (runs off main thread, GPU composited).''',

'''**Task (Code Generation):**
Implement a `createThrottledEventStream` for efficiently processing rapid DOM events:

```ts
const stream = createThrottledEventStream(window, {
  events: ['pointermove', 'scroll', 'resize'],
  throttle: 'animation-frame',    // Batch to one call per RAF
  // OR: throttle: 100,            // Max 10 calls/second
  coalesce: true,                  // When batching, only use the LAST event of each type
  wakeOnFrame: true,               // Resume processing if tab becomes visible
});

stream.on('pointermove', (latestEvent) => updateCursor(latestEvent.clientX, latestEvent.clientY));
stream.on('scroll',      (latestEvent) => updateScrollIndicator());
stream.on('resize',      (latestEvent) => recalculateLayout());

return () => stream.destroy();
```

Show: `requestAnimationFrame` batching (store the latest event per type, drain in RAF), the RAF ID stored in `ref` for cancellation on unmount, `addEventListener` passive mode for touch/wheel events (`{ passive: true }`), and comparing event delegation vs per-element listeners for large element counts.''',

'''**Debug Scenario:**
A Node.js HTTP server has a gradual memory leak — memory grows 10MB per hour under constant traffic:

```ts
const cache = new Map<string, Buffer>();

app.get('/thumbnail/:id', async (req, res) => {
  const { id } = req.params;
  if (!cache.has(id)) {
    const img = await generateThumbnail(id);
    cache.set(id, img); // Never evicted!
  }
  res.type('image/jpeg').send(cache.get(id));
});
```

Every unique `id` request adds to the Map indefinitely. Show: implementing LRU eviction with a max size (`lru-cache` library: `new LRUCache({ max: 500, maxSize: 50 * 1024 * 1024 })`), using `stale-while-revalidate` instead of indefinite caching, and monitoring with `process.memoryUsage().heapUsed` reported to metrics.''',

'''**Debug Scenario:**
A Next.js API route is returning stale data because the response has `Cache-Control: max-age=3600` but the data changes every 5 minutes:

```ts
export default async function handler(req, res) {
  const data = await db.getLatestData();
  res.setHeader('Cache-Control', 'max-age=3600'); // 1 hour!
  res.json(data);
}
```

Setting `max-age=3600` on an API route that changes data every 5 minutes means CDN/browsers cache a stale version for up to 1 hour. Show: `Cache-Control: max-age=0, s-maxage=60, stale-while-revalidate=300` (instant browser, 1min CDN, 5min swr), `no-store` for truly real-time data, and Next.js App Router's `next: { revalidate: 60 }` fetch option.''',

'''**Debug Scenario:**
A developer's web app uses `window.innerWidth` in render to pick a layout, causing hydration mismatches in SSR:

```tsx
function Layout() {
  const isMobile = window.innerWidth < 768; // ReferenceError in SSR!
  return isMobile ? <MobileLayout /> : <DesktopLayout />;
}
```

`window` doesn't exist in Node.js SSR. Even if guarded, the server and client may disagree on the viewport. Show: using a CSS media query approach (no JS needed for layout switching), `useEffect` + `useState(false)` to detect client-side only, `useMediaQuery` hook with SSR-safe defaults, and Next.js `<ClientOnly>` wrapper for truly client-only components.''',

'''**Debug Scenario:**
An Express server's event loop is blocked by a synchronous crypto operation, causing 5-second response delays:

```ts
app.post('/hash-password', (req, res) => {
  const hash = crypto.pbkdf2Sync(
    req.body.password,
    saltBytes,
    100_000,               // 100,000 iterations
    64,
    'sha512'
  );
  // pbkdf2Sync blocks the event loop for ~500ms!
  res.json({ hash: hash.toString('hex') });
});
```

`pbkdf2Sync` is synchronous — blocks Node.js's event loop for ~500ms per request. Under load, requests queue up. Show: using `pbkdf2` (async, runs in `libuv` thread pool): `crypto.pbkdf2(pass, salt, iters, len, alg, callback)` or `util.promisify(crypto.pbkdf2)`, and `bcrypt`/`argon2` libraries that use worker threads for hashing.''',

'''**Debug Scenario:**
A developer's React `useTransition` is not providing a smooth experience because the transition contains synchronous DOM reads:

```tsx
const [isPending, startTransition] = useTransition();

function handleSearch(value: string) {
  startTransition(() => {
    setQuery(value);
    const containerHeight = containerRef.current!.getBoundingClientRect().height;
    // getBoundingClientRect forces a synchronous layout during the transition!
    setContainerHeight(containerHeight);
  });
}
```

`getBoundingClientRect()` inside `startTransition` forces a synchronous reflow, defeating the purpose of the transition (React can't time-slice a synchronous DOM read). Show: moving DOM reads outside `startTransition`, reading the container height via `ResizeObserver` (stored in ref), and only passing pure state setters inside `startTransition`.''',

'''**Task (Code Generation):**
Build a `usePageVisibility` hook that pauses expensive operations when the tab is hidden:

```tsx
const { isVisible, wasHidden, hiddenAt } = usePageVisibility({
  onHide:  () => pauseVideoPlayback(),
  onShow:  () => resumeVideoPlayback(),
  debounce: 300,  // Debounce rapid visibility changes (alt-tab flicker)
});

// Conditional rendering based on visibility:
return isVisible ? <LiveDataChart /> : <PausedPlaceholder hiddenSince={hiddenAt} />;
```

Show: `document.addEventListener('visibilitychange', ...)`, reading `document.visibilityState === 'visible'`, the `Page Visibility API` (also fires on mobile when user switches apps), debouncing rapid changes, and tracking `hiddenAt` timestamp with `Date.now()`.''',

]

"""
snippets/q_performance.py - 28 Performance Optimization questions
"""

Q_PERFORMANCE = [

"""**Context:**
Running @next/bundle-analyzer on our Next.js 14 SaaS dashboard. The /dashboard route chunk is 920KB unminified. The analyzer shows a massive node_modules/recharts block taking up ~35% of the chunk even though only 2 out of 12 dashboard panels use it.

**Observed Issue:**
We use next/dynamic for AnalyticsPanel (which imports Recharts), but it still ends up in the main chunk. The dynamic() call is definitely there -- we see the separate chunk in the build output -- but the main bundle still contains Recharts.

**Specific Ask:**
What causes a dynamically imported module to still appear in the parent chunk? Is it a barrel file re-export (index.ts) hoisting the import? How do you systematically trace which import path is pulling Recharts into the main chunk using Webpack's module graph?""",

"""**Context:**
Our dashboard imports specific functions from lodash using named imports, which should tree-shake correctly on Webpack 5.

**Code:**
```ts
import { debounce, groupBy, sortBy } from 'lodash';
```

**Observed Issue:**
Bundle analyzer shows the entire lodash library (530KB) in the output despite named imports and sideEffects: false in package.json. Switching to lodash-es fixes it but breaks two other packages that peer-depend on lodash (CJS).

**Specific Ask:**
Why does Webpack 5 fail to tree-shake CJS lodash even with named imports and sideEffects: false? How do you audit which packages in a dependency graph are CJS vs ESM? And when you can't upgrade a peer dependency, what's the alternative to getting lodash tree-shaken?""",

"""**Context:**
Our dashboard has 14 route segments. Currently we bundle-split at the page level, but the /dashboard/reports route still loads 1.1MB because it imports the entire reporting engine even for users who only view summaries.

**Observed Issue:**
We want finer-grained splits -- lazy load the PDF export module, the chart customizer, and the advanced filter panel independently. But adding more dynamic imports creates a waterfall of 4-5 sequential network requests on first load.

**Specific Ask:**
How do you balance granular code-splitting (smaller chunks = faster parse) vs. request waterfall (more chunks = more round trips)? Is link preloading the build-time chunks the answer? What's the right heuristic for where to draw split boundaries in a heavily nested component tree?""",

"""**Context:**
Our DataTable uses react-window FixedSizeList to virtualize 50,000 rows. Scrolling fast causes a white flash -- rows haven't rendered yet when they enter the viewport.

**Observed Issue:**
Increasing overscanCount from 3 to 25 reduces flashing but the commit takes 180ms (too heavy). We need more pre-rendered rows without paying the full render cost.

**Specific Ask:**
Is there a way to increase visible row buffer without increasing synchronous render work? Can we pre-render offscreen rows in a lower-priority concurrent render using startTransition? Or is the correct fix to optimize individual row render time so a larger overscan is cheap?""",

"""**Context:**
Our dashboard has a useRealtimeMetrics hook used in 40+ components. Each call attaches a message listener to a shared EventTarget. After 2 hours of use, Chrome's Memory tab shows heap growing from 90MB to 380MB.

**Code:**
```ts
useEffect(() => {
  const handler = (e) => updateMetric(metricId, e.data);
  metricsEmitter.addEventListener('update', handler);
  // cleanup omitted by mistake
}, [metricId]);
```

**Observed Issue:**
The missing cleanup means every re-render with a new metricId adds another listener without removing the old one. After heavy navigation, thousands of listeners accumulate.

**Specific Ask:**
Beyond fixing the obvious cleanup bug -- how do you set up a systematic memory regression test that would catch this class of leak in CI before it reaches production? What tooling (Puppeteer heap snapshots, Playwright memory assertions) can give a reliable signal?""",

"""**Context:**
We have a custom sticky column implementation in our DataTable. On horizontal scroll we programmatically update left offsets for sticky cells by reading then writing their widths in a loop.

**Code:**
```ts
cells.forEach(cell => {
  const w = cell.getBoundingClientRect().width; // READ
  cell.style.left = `${offset}px`;             // WRITE
  offset += w;
});
```

**Observed Issue:**
Chrome DevTools Performance panel shows forced reflow on every scroll event. The interleaved reads and writes force layout recalculation on each iteration.

**Specific Ask:**
What's the canonical pattern to batch DOM reads and writes here? Should I read all widths first, then write all offsets? Or cache widths with ResizeObserver and skip DOM reads entirely during scroll? Would CSS scroll-driven animations eliminate this JS loop altogether?""",

"""**Context:**
Our animated sidebar uses CSS transform for open/close. The Performance panel shows expensive paint operations on the sidebar's 200+ descendant elements during the animation, even though transform should be compositor-only.

**Observed Issue:**
Descendants that use box-shadow and border-radius aren't being promoted to their own layers -- they're being repainted as part of the sidebar every frame.

**Specific Ask:**
How do you isolate compositor-thread animations from triggering descendant repaints? Does adding contain: layout paint to the sidebar prevent descendant paint invalidation? When does will-change: transform on descendants help vs. hurt performance due to layer memory cost?""",

"""**Context:**
React DevTools Profiler shows a 220ms commit after each WebSocket message that updates our 200-row DataTable. The flame chart shows Row being the hottest component, but every row re-renders, including unchanged ones.

**Observed Issue:**
Rows are wrapped in React.memo and their data comes from a normalized Zustand store. But the selector for each row returns a new object reference: `(state) => state.rows[id]` -- because rows[id] is spread on every store update.

**Specific Ask:**
How do you structure Zustand selectors so individual row components only re-render when their specific row's data changes? Should each Row use a granular selector like `state => state.rows[id].status` per field, or is there a shallow-equality selector pattern that avoids spreading?""",

"""**Context:**
Our dashboard runs a large JSON transformation (flattening 10MB of nested API response into a normalized table format) on the main thread on every data refresh, blocking the UI for ~300ms.

**Observed Issue:**
During the 300ms block, all user interactions (hover, typing in filter) are unresponsive. We want to move this work off the main thread.

**Specific Ask:**
What's the correct pattern for offloading heavy synchronous computation to a Web Worker in a React + TypeScript + Next.js app? How do you handle the async message-passing without making the component feel sluggish? Is Comlink a good abstraction, or does it introduce overhead that matters at 10MB data sizes?""",

"""**Context:**
We have a scroll handler that updates a sticky header's shadow and a progress bar position. It's called on every scroll event -- potentially 60+ times per second.

**Code:**
```ts
window.addEventListener('scroll', () => {
  header.style.boxShadow = window.scrollY > 0 ? '...' : 'none';
  progressBar.style.width = `${getProgress()}%`;
});
```

**Observed Issue:**
The Progress panel shows long scripting tasks during scroll. The handler runs synchronously on every scroll event, blocking the main thread.

**Specific Ask:**
Should this be wrapped in requestAnimationFrame to batch scroll updates to once per frame? Or is a passive event listener + throttle enough? What's the difference between throttle(16ms) and rAF for scroll handlers in terms of scheduling guarantees?""",

"""**Context:**
Our dashboard search box filters a large client-side dataset. We debounce the API call but the local filter (for immediate UI feedback) runs on every keystroke.

**Observed Issue:**
On a mid-tier device, filtering 5,000 items on each keystroke takes ~80ms. With a 30ms event loop, the lag is noticeable. Debouncing the local filter would make the UI feel unresponsive.

**Specific Ask:**
Is useDeferredValue the right tool for the local filter -- show a stale list immediately and update it non-urgently? Or should we move the filter computation to a Web Worker? What's the practical threshold where moving computation off-thread is worth the complexity of message-passing?""",

"""**Context:**
Our dashboard homepage has a hero image as the LCP element. Lighthouse reports LCP at 4.8s on a 4G connection. The image is served from a CDN, is correctly sized, and uses next/image.

**Observed Issue:**
Waterfall analysis shows the image starts loading at 2.1s (after JS parses and React renders). It's not being preloaded, so the browser doesn't know about it until the React render completes.

**Specific Ask:**
How does next/image handle preloading for above-the-fold images? Is the priority prop enough to add a <link rel="preload">? What HTTP headers or HTML hints ensure the CDN serves the image early, before React has hydrated?""",

"""**Context:**
Our dashboard uses a custom sans-serif font (Inter, self-hosted). On initial load, users see a flash of unstyled text (FOUT) for ~600ms while the font loads, causing a layout shift.

**Observed Issue:**
We use font-display: swap. The fallback font (Arial) has different metrics than Inter, causing text to reflow when Inter loads. This scores 0.14 CLS on Lighthouse.

**Specific Ask:**
Is font-display: optional better than swap for CLS, at the cost of potentially not showing the custom font on slow connections? What's the size-adjust / ascent-override / descent-override CSS descriptor approach for matching fallback font metrics to Inter, and does next/font handle this automatically?""",

"""**Context:**
Our static assets are served from S3 + CloudFront. JS bundle sizes are: main chunk 340KB gzipped. Build output shows Brotli-compressed versions exist but the CDN is serving gzip.

**Observed Issue:**
Brotli compresses our main chunk to 290KB vs gzip's 340KB -- a 15% saving. The S3 objects have .br equivalents but CloudFront isn't serving them.

**Specific Ask:**
What's the CloudFront configuration needed to serve Brotli when the browser sends Accept-Encoding: br? Is this a cache behavior policy, an origin response header issue, or a compression setting? And for a Next.js app, should compression happen at the CDN layer, the server layer, or both?""",

"""**Context:**
Our design system uses styled-components v6. The React DevTools Profiler shows 12ms spent in styled-components' style injection on every DataTable render (200 rows with styled Row and Cell).

**Observed Issue:**
Styled-components injects a new <style> tag or updates the CSSStyleSheet on every render, even when props haven't changed. On a 200-row table, this 12ms adds up to 2.4 seconds of cumulative style injection during a 2-minute usage session.

**Specific Ask:**
Is runtime CSS injection from styled-components fundamentally incompatible with high-density, high-frequency-render components? What's the migration path: CSS Modules, vanilla-extract, or Linaria (compile-time)? Can we do a targeted migration (only the table) while keeping styled-components elsewhere?""",

"""**Context:**
Our dashboard includes Google Tag Manager, Intercom, and a third-party analytics script. Lighthouse TTI is 7.2s and Long Tasks analysis shows these scripts are the primary culprits.

**Observed Issue:**
All three scripts load synchronously in <head>. GTM alone runs 1.1s of JavaScript on the main thread during page load. Users can't interact with the dashboard until these scripts finish.

**Specific Ask:**
What's the correct loading strategy for third-party scripts that shouldn't block TTI? next/script with strategy="lazyOnload" vs "afterInteractive" -- what's the actual difference in execution timing relative to hydration? And for GTM specifically, are there any gotchas with loading it async vs sync related to dataLayer initialization?""",

"""**Context:**
Our dashboard uses a Service Worker for offline caching of static assets. After deploying a new version, some users continue to get stale JS bundles cached by the old SW even after refreshing.

**Observed Issue:**
The old Service Worker intercepts the network requests and serves cached files. The new SW (with updated cache names) isn't activating because the old SW is controlling the page.

**Specific Ask:**
What's the correct cache-busting strategy for Service Workers? Is skipWaiting() + clients.claim() the right approach to force activation on deploy? What are the risks -- could this cause a half-old/half-new bundle state where old and new chunks are mixed during a session?""",

"""**Context:**
We use <link rel="prefetch"> for likely-next-page routes in our dashboard SPA. But Lighthouse flags that prefetched resources are being fetched but not used within 3 seconds, reducing their effective priority.

**Observed Issue:**
We prefetch /dashboard/reports on the home page. But users take 5-10 minutes to navigate there. By then, the prefetched resource may have been evicted from cache.

**Specific Ask:**
What's the actual browser cache behavior for prefetched resources -- how long do they stay in the prefetch cache before eviction? Is prefetch the right hint for resources used 5+ minutes later, or should modulepreload or preconnect be used instead? How does Next.js's built-in route prefetching strategy differ?""",

"""**Context:**
We're using Module Federation to split our dashboard into a host and two remotes (AnalyticsMFE, ReportsMFE). On initial load, the host app renders, then sequentially fetches the remote manifests, then fetches the remote chunks.

**Observed Issue:**
The sequential waterfall (host JS → remote manifest → remote chunk) adds 1.4s to TTI on a 4G connection. Users see a spinner for both MFE panels until all three requests complete.

**Specific Ask:**
How do you parallelize Module Federation remote loading to eliminate the waterfall? Should remote manifests be inlined into the host's HTML at build time? Is there a pattern for loading remote chunks speculatively (before the host JS has executed) using <link rel="preload">?""",

"""**Context:**
During code review, a teammate added a dynamic import inside a frequently-called utility function. Now our dashboard shows a waterfall of 6 sequential chunk loads on startup.

**Code:**
```ts
async function formatCurrency(amount, locale) {
  const { format } = await import('./formatters/currency'); // loaded on every call
  return format(amount, locale);
}
```

**Observed Issue:**
The await import() is inside a loop called 200 times on mount. Webpack emits a single chunk but the dynamic import creates a promise chain that serializes with other dynamic imports in the startup sequence.

**Specific Ask:**
What's the correct pattern for a utility that should be code-split but called frequently? Should the dynamic import be hoisted to module level (defeating the split)? Or should we use a module-level import() promise that's awaited once and then cached?""",

"""**Context:**
Lighthouse reports our dashboard has an INP (Interaction to Next Paint) of 680ms -- well above the 200ms "good" threshold. The LoAF (Long Animation Frames) breakdown shows the click handler on our primary CTA runs a 600ms synchronous task.

**Observed Issue:**
The click handler validates a form, runs client-side permission checks, and triggers a Zustand state update -- all synchronously. The 600ms block prevents the browser from painting the loading state.

**Specific Ask:**
How do you decompose a long synchronous click handler to improve INP? Is the fix to yield to the main thread (scheduler.postTask, setTimeout(0)) between each phase? Or should the expensive work (permission checks) be precomputed and cached so the click handler is instant?""",

"""**Context:**
Our dashboard's main filter bar interaction has INP of 400ms. Chrome DevTools traces show the interaction triggers a React state update that synchronously re-renders 80 components.

**Observed Issue:**
The filter state lives high in the component tree (at Dashboard level). Every filter change re-renders the entire subtree, including components that don't use the filter state.

**Specific Ask:**
Is the root fix state colocation (move filter state lower) or memoization (prevent non-filter components from re-rendering)? What's the React 18 concurrent mode approach -- does wrapping the state update in startTransition reduce the INP score even if the total work is the same?""",

"""**Context:**
Our dashboard has a CLS score of 0.21 (threshold: 0.1). The CLS debugger shows two main culprits: (1) the user avatar image in the header loads late and shifts the nav, and (2) a promotion banner renders after hydration and pushes content down.

**Observed Issue:**
The avatar has no explicit width/height attributes. The banner is only shown to certain user segments (fetched client-side after hydration).

**Specific Ask:**
For the avatar: is width/height on the img tag or aspect-ratio in CSS sufficient to reserve space before the image loads? For the banner: since it's segment-specific and can't be server-rendered, what's the pattern to reserve its space without knowing if it will show? A skeleton with fixed height?""",

"""**Context:**
Our LCP element is a hero chart (SVG) that renders after a client-side data fetch. Lighthouse consistently reports LCP at 5.2s. The chart cannot be statically generated because data is user-specific.

**Observed Issue:**
The LCP is blocked by: (1) JS download, (2) React hydration, (3) fetch, (4) chart render. Each step is sequential. We can't preload the SVG because it doesn't exist at build time.

**Specific Ask:**
For user-specific dynamic content that can't be prerendered, what's the LCP optimization strategy? Should we stream a server-rendered skeleton with exact final dimensions so the browser reserves LCP space early? Does Next.js 14 streaming RSC affect LCP measurement differently than client-side rendering?""",

"""**Context:**
Our Next.js dashboard TTFB is 820ms at P75. The server is on Vercel Edge. Database queries are the bottleneck -- each RSC page makes 3-4 sequential Postgres queries via Prisma.

**Observed Issue:**
The queries run sequentially because each awaits the previous result. Total DB time is 600ms of the 820ms TTFB.

**Specific Ask:**
How do you parallelize independent database queries in a Next.js RSC route without causing waterfalls? Should we use Promise.all for independent queries and only sequence truly dependent ones? Are there Prisma batching patterns that reduce round trips? Does using a connection pooler (PgBouncer, Supabase pooling) meaningfully reduce per-query overhead?""",

"""**Context:**
Lighthouse flags two render-blocking resources on our dashboard: a third-party font CSS file loaded in <head> and our own global.css. Both block First Contentful Paint.

**Observed Issue:**
global.css contains critical above-the-fold styles AND non-critical below-the-fold animation styles. The font CSS loads Inter from Google Fonts synchronously.

**Specific Ask:**
What's the right strategy to make global.css non-blocking? Is the critical CSS inlining approach (extract above-fold styles, inline them, load the rest async) still worth the complexity with HTTP/2 push available? For the Google Fonts CSS, is <link rel="preconnect"> + media="print" onload trick still the best async load pattern?""",

"""**Context:**
On a Moto G4 (simulated in Lighthouse), our dashboard JavaScript parse + execution time is 8.2 seconds. The main thread is blocked for nearly the entire load. On a MacBook it's 800ms.

**Observed Issue:**
The 10x difference is almost entirely parse/eval time, not network time. We have 2.1MB of unminified JS being evaluated on a single-core mobile CPU.

**Specific Ask:**
Beyond reducing bundle size (which we're doing), are there techniques to reduce JS parse time on low-end devices? Does code-splitting help parse time linearly (each chunk parsed lazily) or does the total parse cost remain the same? Is there a practical way to defer non-interactive module evaluation using module script type="module" semantics?""",

"""**Context:**
Our dashboard receives WebSocket updates at 20 messages/second during market hours. Each message triggers a Zustand store update which React picks up via useSyncExternalStore and re-renders affected components.

**Observed Issue:**
At 20 updates/second, React can't batch renders fast enough. We get 20 separate render commits per second (each ~15ms), consuming 300ms/second of main thread -- visible as input lag.

**Specific Ask:**
How do you throttle or batch high-frequency external store updates before they reach React? Should we accumulate WebSocket messages in a buffer and flush to Zustand at 60fps using requestAnimationFrame? What's the interaction between batched Zustand updates and React 18's automatic batching?""",

]

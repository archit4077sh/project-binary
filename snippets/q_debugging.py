"""
snippets/q_debugging.py — BATCH 6: 56 brand-new Debugging questions
Zero overlap with batches 1-5 archives.
"""

Q_DEBUGGING = [

"""**Debug Scenario:**
A developer opens Chrome DevTools Network panel and sees a critical API request is taking 2.3 seconds, but the server logs show processing time of only 80ms. The 2.3 seconds include: DNS lookup (450ms), Connection (120ms), TLS (180ms), Waiting (TTFB) (80ms), Download (5ms).

Show: using `dns-prefetch` and `preconnect` to eliminate DNS/TCP/TLS overhead for critical API domains, `keep-alive` connections (HTTP/1.1: `Connection: keep-alive`), HTTP/2 multiplexing that reuses one TCP connection for all API calls, and identifying that the 750ms of DNS+Connection+TLS is the bottleneck — not the server.""",

"""**Debug Scenario:**
A React app has a "Warning: Each child in a list should have a unique 'key' prop" even though keys ARE provided:

```tsx
function UserList({ users }: { users: User[] }) {
  return users.map((user, index) => (
    <div>                                     {/* Missing key here! */}
      <UserCard key={user.id} user={user} />  {/* Key on the wrong element */}
    </div>
  ));
}
```

The `key` is on `<UserCard>` but not on the wrapping `<div>`. The outermost element returned from `map` must have the `key`. Show: moving `key` to the outer `<div key={user.id}>`, removing the redundant `key` from `<UserCard>`, and using `<Fragment key={user.id}>` when the wrapper is only for grouping.""",

"""**Debug Scenario:**
A CSS grid layout breaks on Safari 15 but works on Chrome. The grid uses `gap` shorthand:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem; /* Not supported in Safari < 12 as 'gap', must use 'grid-gap' */
}
```

Safari 15 supports `gap` in grid, but some users are on Safari 14. Show: adding `grid-gap` alongside `gap` for older Safari (`grid-gap: 1rem; gap: 1rem;`), using `@supports (gap: 1rem)` as a feature query, and the BrowserStack/Sauce Labs workflow for cross-browser testing.""",

"""**Debug Scenario:**
A developer's `async/await` error handler silently swallows errors in a `forEach`:

```ts
async function processAll(items: Item[]) {
  items.forEach(async (item) => {
    try {
      await processItem(item); // Errors here are caught by inner try/catch
    } catch (e) {
      console.error('Item failed', e);
    }
  });
  // processAll returns void BEFORE any items finish!
}
```

`forEach` doesn't await async callbacks. The outer function resolves before processing begins. Show: replacing with `for...of` + `await` for sequential processing, or `Promise.all(items.map(async (item) => ...))` for parallel processing, and the `p-limit` library for controlled concurrency with error handling.""",

"""**Debug Scenario:**
A Next.js page passes large objects through `getServerSideProps` and the response is 1.2MB, causing slow page loads:

```ts
export async function getServerSideProps() {
  const allProducts = await db.products.findMany(); // 50,000 rows = 1.2MB JSON!
  return { props: { allProducts } };
}
```

`getServerSideProps` serializes props to JSON and embeds it in the initial HTML as `__NEXT_DATA__`. Show: filtering to only the fields needed (`select: { id, name, price, image }`), paginating (return only the first page), fetching the full dataset client-side with React Query (load page fast, data loads incrementally), and the 128KB recommended limit for `__NEXT_DATA__`.""",

"""**Debug Scenario:**
Chrome DevTools shows a long "Evaluate Script" task (180ms) blocking the main thread during page load:

```html
<script src="/vendor/lodash.js"></script>        <!-- 73KB gzipped = 350ms parse on mobile -->
<script src="/vendor/moment.js"></script>         <!-- 22KB gzipped = 100ms parse on mobile -->
<script src="/bundle.js"></script>                <!-- 200KB gzipped = 600ms parse on mobile -->
```

JavaScript parse+evaluation is CPU-bound and blocks the main thread. Show: switching to `date-fns` (tree-shakeable) from `moment.js`, removing Lodash (most utils native in modern JS), using `<script defer>` to parse after HTML, code splitting to defer non-critical JS, and the "Cost of JavaScript" metric (parsing + compilation time).""",

"""**Debug Scenario:**
A React form's `onChange` handler reconstructs a new object from the entire form state on every keystroke, causing unnecessary re-renders of unrelated fields:

```tsx
const [form, setForm] = useState({ name: '', email: '', bio: '' });

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setForm({ ...form, [e.target.name]: e.target.value });
  // Every field re-renders on every change to any field
};
```

All fields share one `useState` — any update rerenders all. Show: using `React.memo` on individual field components (only re-render if their specific value changes), separating fields into independent `useState` calls, using `useReducer` for form state (more efficient for complex forms), and `react-hook-form` (uses uncontrolled inputs — zero re-renders per keystroke).""",

"""**Debug Scenario:**
A developer finds that `console.log` statements in production are crashing the app when objects contain circular references:

```ts
const user = { id: 'u1', manager: null as any };
user.manager = user; // Circular reference!
console.log(JSON.stringify(user)); // TypeError: Converting circular structure to JSON
```

`JSON.stringify` throws for circular references. Show: implementing a `safeStringify` using a `WeakSet` replacer to detect and skip circular refs, using `util.inspect` in Node.js (handles circles), `JSON.stringify(obj, null, 2)` with a custom replacer, and the `flatted` library for serializing/deserializing circular JSON.""",

"""**Debug Scenario:**
A custom `useFetch` hook causes "Warning: Can't perform a React state update on an unmounted component" every time a page is navigated away during a pending request:

```ts
function useFetch(url: string) {
  const [data, setData] = useState<Data | null>(null);

  useEffect(() => {
    fetch(url).then(r => r.json()).then(setData); // setData after unmount!
  }, [url]);

  return data;
}
```

The `fetch` completes after the component unmounts and tries to call `setData` on an unmounted component. Show: using `AbortController` to cancel the fetch on cleanup (`signal: controller.signal; return () => controller.abort()`), checking a `mounted` flag before `setData`, and React 18's `startTransition` which handles this automatically.""",

"""**Debug Scenario:**
A developer uses `Object.assign` to merge config objects but deeply nested defaults are not preserved:

```ts
const defaults = {
  server: { port: 3000, host: 'localhost', ssl: { enabled: false, cert: '' } },
  logging: { level: 'info', format: 'json' },
};

const userConfig = { server: { port: 8080 } };

const merged = Object.assign({}, defaults, userConfig);
// merged.server: { port: 8080 } — ssl and host are GONE!
// Object.assign does shallow merge only
```

Show: deep merge using `structuredClone` + recursive merge, `lodash.merge` for deep merging, `{ ...defaults, server: { ...defaults.server, ...userConfig.server } }` for manual deep spread, and TypeScript's `DeepPartial<T>` type for the user config parameter.""",

"""**Debug Scenario:**
A React component that renders a `<canvas>` for data visualization crashes in SSR (Next.js) because `canvas` APIs aren't available in Node.js:

```ts
function Chart({ data }: { data: ChartData }) {
  useEffect(() => {
    const canvas = canvasRef.current!;
    const ctx = canvas.getContext('2d')!; // ReferenceError: document is not defined in SSR
    drawChart(ctx, data);
  }, [data]);
}
```

`canvas.getContext` errors during SSR because there's no DOM in Node.js. Show: wrapping in `useEffect` (already client-only), using dynamic import with `ssr: false` (`const Chart = dynamic(() => import('./Chart'), { ssr: false })`), and `typeof window !== 'undefined'` guard for canvas operations.""",

"""**Debug Scenario:**
A developer writes an optimization using `shouldComponentUpdate` but it creates subtle bugs when nested objects change:

```tsx
shouldComponentUpdate(nextProps) {
  return this.props.data !== nextProps.data; // Shallow reference check
}

// Parent updates a nested property:
this.setState(prev => {
  prev.data.items.push(newItem); // MUTATION — same reference!
  return { data: prev.data };   // shouldComponentUpdate: false → no re-render!
});
```

Mutating state and comparing references is always incorrect. Show: using immutable updates (`{ ...prev.data, items: [...prev.data.items, newItem] }`), switching to `React.PureComponent` (shallow comparison of all props/state), and using `immer`'s `produce` for immutable state updates.""",

"""**Debug Scenario:**
An API returns a `Set-Cookie` header but the cookie doesn't appear in the browser due to `SameSite` restrictions:

```
Set-Cookie: session=abc123; Secure; HttpOnly; SameSite=Strict
```

The frontend is at `app.example.com` and the API is at `api.example.com` — cross-origin. With `SameSite=Strict`, the cookie is not sent on cross-origin requests. Show: changing to `SameSite=None; Secure` for cross-origin cookies, or switching to `SameSite=Lax` (cookies sent on top-level navigation but not AJAX), moving the API to the same origin via a reverse proxy (best solution), and the browser's "third-party cookie" blockage in Chrome 2024.""",

"""**Debug Scenario:**
A developer's TypeScript union type narrows correctly in `if/else` but not in a `switch-case`:

```ts
type Shape = { kind: 'circle'; radius: number } | { kind: 'rect'; width: number; height: number };

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case 'circle': return Math.PI * shape.radius ** 2; // shape.radius: number ✓
    case 'rect':   return shape.width * shape.height;  // shape.width: number ✓
    // TypeScript marks the 'default' case as unreachable (exhaustive ✓)
  }
  // ERROR: Function lacks ending return statement — TypeScript doesn't see the switch as exhaustive
}
```

TypeScript doesn't always consider a `switch` exhaustive without explicit `default`. Show: adding `default: return assertNever(shape)`, or adding `return 0` after the switch, or using a `switch (true)` with explicit `return` in each case so TypeScript sees all code paths return.""",

"""**Debug Scenario:**
A developer's custom `useDebounce` hook fires immediately even when the component re-renders within the debounce window:

```ts
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer); // This cancels and restarts on every render!
  }); // BUG: No dependency array — runs on every render

  return debounced;
}
```

Without a dependency array, the effect runs on EVERY render. If the component re-renders (e.g., parent re-renders), the timer resets even if `value` didn't change. Show: adding `[value, delay]` as the dependency array so the timer only resets when `value` or `delay` changes.""",

"""**Debug Scenario:**
A developer's React `useRef` for tracking previous value doesn't work on the first render:

```ts
function usePrevious<T>(value: T): T | undefined {
  const prevRef = useRef<T>();
  useEffect(() => {
    prevRef.current = value;
  });
  return prevRef.current; // Returns undefined on first render!
}
```

On the first render, `prevRef.current` is `undefined` because the effect hasn't run yet. Show: this is the correct/expected behavior for a `usePrevious` hook — on the first render there IS no previous value, so `undefined` is appropriate. Also show an alternative that initializes with the first value (`useRef<T>(value)`) — this returns the initial value on first render (current = previous = initial).""",

"""**Debug Scenario:**
A production React app is throwing "Too many re-renders" in a component that uses `useState` inside a render:

```tsx
function Counter() {
  const [count, setCount] = useState(0);
  setCount(count + 1); // Called during render — infinite loop!
  return <div>{count}</div>;
}
```

`setCount` called during render triggers another render, which calls `setCount` again — infinite loop. Show: moving `setCount` into a `useEffect` (for side effects), an event handler (for user interactions), or an initial `useState(() => computeInitialValue())` lazy initializer (for one-time setup).""",

"""**Debug Scenario:**
A developer creates a memoized selector but performance is worse than without memoization:

```ts
// Without reselect — recomputes each render but fast:
const total = cart.reduce((sum, item) => sum + item.price, 0);

// With reselect — but called with a new args object every render:
const selectTotal = createSelector(
  [(state) => state.cart],
  (cart) => cart.reduce((sum, item) => sum + item.price, 0)
);

const total = useSelector(selectTotal); // Memoization works properly ✓
```

Actually the memoization here IS working correctly. Show a pattern that BREAKS memoization:

```ts
const selectProductsByCategory = createSelector(
  [(state) => state.products, (_, category) => category],
  (products, category) => products.filter(p => p.category === category)
);

// In component — broken: createSelector only has cache size of 1:
const electronics = useSelector(state => selectProductsByCategory(state, 'electronics'));
const books = useSelector(state => selectProductsByCategory(state, 'books')); // invalidates electronics cache!
```

Show: using `createSelectorCreator` with a custom cache (memoize-one with cache size 2+) or creating a selector factory (`makeSelectByCategory = () => createSelector(...)`).""",

"""**Debug Scenario:**
A developer's Node.js script for bulk database inserts is extremely slow — inserting 100,000 rows takes 45 minutes:

```ts
for (const record of records) {
  await db.query('INSERT INTO events VALUES ($1, $2, $3)', [record.id, record.data, record.ts]);
}
// 100,000 ROUNDTRIPS to the database!
```

One `await` per row means 100,000 sequential network round-trips. Show: batching inserts (`INSERT INTO events VALUES ($1,$2,$3),($4,$5,$6)...` with chunks of 1000 rows), using PostgreSQL `COPY FROM` for maximum throughput (100K rows in ~5 seconds), `Promise.all` with controlled concurrency for parallel inserts, and Prisma's `createMany`.""",

"""**Debug Scenario:**
A developer's regex produces catastrophic backtracking and hangs the server when processing user input:

```ts
// Vulnerable regex — nested quantifiers:
const emailRegex = /^([a-zA-Z0-9._%+-]+)+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$/;

// With malicious input: 'aaaaaaaaaaaaaaaaaaaaaa@b'
// Regex engine tries exponential combinations — hangs for minutes!
server.post('/validate', (req, res) => {
  const isValid = emailRegex.test(req.body.email); // HANGS
});
```

Nested quantifiers like `([a-zA-Z0-9.]+)+` cause catastrophic backtracking. Show: simplifying to `^[^\s@]+@[^\s@]+\.[^\s@]+$` for basic email validation, using the `validator.js` library (battle-tested, safe regex), setting a regex timeout with a worker thread, and using `re2` (Google's linear-time regex engine) for user-supplied patterns.""",

"""**Debug Scenario:**
A developer's `Promise.race` doesn't cancel the slower promise when the faster one resolves:

```ts
const result = await Promise.race([
  fetch('/api/fast-endpoint'),   // resolves in 100ms
  fetch('/api/slow-endpoint'),   // still in flight!
]);
// slow-endpoint fetch continues running in background (resource leak)
```

`Promise.race` returns the first resolved value but doesn't cancel other promises — they continue in the background. Show: using `AbortController` with all promises in the race (`const controller = new AbortController(); Promise.race([..., timeout]).finally(() => controller.abort())`), and a `raceWithAbort` utility that cancels all others when one wins.""",

"""**Debug Scenario:**
A developer's `EventEmitter` memory leak warning fires after adding listeners dynamically:

```ts
const emitter = new EventEmitter();

function subscribeComponent(name: string) {
  emitter.on('data', (payload) => processPayload(name, payload));
  // No cleanup! Called 15 times → 15 listeners on 'data' → warning
}
```

`EventEmitter` warns at >10 listeners (default). Each call adds a new listener that's never removed. Show: calling `emitter.off('data', handler)` when the consumer is done (requires storing the handler reference: `const handler = (p) => ...; emitter.on('data', handler)`), `emitter.once` for one-time listeners, and React's cleanup pattern in `useEffect` for EventEmitter subscriptions.""",

"""**Debug Scenario:**
A Node.js Express app has very slow cold starts (8 seconds) on Lambda because it imports the entire app at the top of the handler:

```ts
// handler.ts (Lambda entry):
import express from 'express';
import helmet from 'helmet';
import { router } from './routes/all-routes'; // imports everything!

const app = express();
app.use(helmet());
app.use(router);

export const handler = serverlessExpress({ app });
// 8 second cold start → all routes & dependencies loaded upfront
```

Show: lazy-loading routes that aren't needed for this specific Lambda invocation, using `--bundle` with `esbuild` to reduce deployment package size (fewer `require()` calls), keeping the Lambda runtime warm with scheduled pings, and the `middy` middleware framework which lazy-loads plugins.""",

"""**Debug Scenario:**
A developer's `for await...of` loop over an async generator processes items slower than expected — each item waits for the previous to finish:

```ts
async function* generateItems() {
  for (const url of urls) {
    const data = await fetch(url).then(r => r.json());
    yield data; // Each item waits for its fetch to complete
  }
}

for await (const item of generateItems()) {
  await processItem(item); // Sequential: fetch then process, one at a time
}
```

Items are fetched and processed sequentially. Show: prefetching the next item while processing the current one (producer-consumer pattern), using `Promise.all` to fetch all items upfront if they fit in memory, and a sliding window approach (fetch N items ahead, process 1 at a time).""",

"""**Debug Scenario:**
A developer's TypeScript `interface` extends two interfaces with conflicting method signatures, but TypeScript doesn't raise an error — it silently uses one:

```ts
interface A { getValue(): number }
interface B { getValue(): string }

interface C extends A, B {} // TypeScript Error: Named property 'getValue' of types 'A' and 'B' are not identical.

// But if using intersection instead:
type C = A & B;
const obj: C = { getValue: () => ... }; // What type should getValue return?
// Answer: getValue(): number & string = never!
```

Show: the correct error TypeScript raises for `interface extends` with conflicts, the silent `never` produced by intersection, and resolving conflicts by overriding in `C`: `interface C extends A, B { getValue(): never }` to explicitly acknowledge the conflict, or redesigning to avoid the conflict.""",

"""**Debug Scenario:**
A React app's `useEffect` dependency on a function causes an infinite loop:

```tsx
function Parent() {
  const fetchData = async () => {
    const data = await api.getData();
    setItems(data);
  };

  return <Child fetchData={fetchData} />;
}

function Child({ fetchData }: { fetchData: () => Promise<void> }) {
  useEffect(() => {
    fetchData(); // Called on every render!
  }, [fetchData]); // fetchData changes every render (new function reference)
}
```

`fetchData` is redefined every `Parent` render. Show: wrapping `fetchData` in `useCallback` in the Parent, moving `fetchData` outside the component if it doesn't use component state, and the ESLint `react-hooks/exhaustive-deps` rule detecting this pattern.""",

"""**Debug Scenario:**
A developer discovers that `Date.now()` returns different values between server and client, causing hydration mismatches in Next.js:

```tsx
function TimeDisplay() {
  return <span>Generated at: {new Date(Date.now()).toLocaleTimeString()}</span>;
  // SSR: 10:00:00 AM | Client hydration: 10:00:01 AM → mismatch!
}
```

The server renders at one time, the client hydrates a second or more later — clocks diverge. Show: using `suppressHydrationWarning` on the element (for truly dynamic values where mismatches are expected), computing the time in a `useEffect` (renders on client only), passing the server time as a prop from `getServerSideProps`, and `useId` for stable identifiers across SSR/CSR.""",

"""**Debug Scenario:**
A developer's Webpack bundle includes multiple copies of the same library because different packages require different versions:

```
Bundle analysis shows:
  - lodash@4.17.21 (348KB) — used by app
  - lodash@3.10.1  (310KB) — required by old-library
  Total: 658KB of lodash!
```

Two versions of lodash are bundled when they could share one. Show: Webpack's `resolve.alias` to deduplicate (`'lodash': path.resolve(__dirname, 'node_modules/lodash')`), `npm dedupe` / `yarn dedupe` to hoist compatible versions, the `webpack-bundle-analyzer` plugin for identifying duplicates, and upgrading `old-library` to support the newer lodash version.""",

"""**Debug Scenario:**
A developer's React Native / web app has flickering images because `uri` prop changes on every render:

```tsx
function Avatar({ userId }: { userId: string }) {
  const uri = `https://cdn.example.com/avatars/${userId}.jpg?t=${Date.now()}`; // Changes every render!
  return <img src={uri} />;
}
```

`Date.now()` in the `uri` means every render generates a new URL — browser's image cache misses, causing flicker. Show: removing the cache-busting query param (CDN handles invalidation via path: `/avatars/${userId}/v2.jpg`), using `useMemo` to stabilize the URL, and proper cache busting strategy (change URL only when the image changes, not on every render).""",

"""**Debug Scenario:**
A developer's `window.addEventListener` keeps adding duplicate listeners because it's called inside a function that runs on every state change:

```tsx
function App() {
  const [count, setCount] = useState(0);

  const onResize = () => setCount(window.innerWidth);
  window.addEventListener('resize', onResize); // Added every render!

  return <Button onClick={() => setCount(c => c + 1)} />;
}
```

`addEventListener` outside `useEffect` runs on every render — adding unlimited listeners. Show: wrapping in `useEffect` with proper cleanup (`return () => window.removeEventListener('resize', onResize)`), stabilizing `onResize` with `useCallback` (or using `useCallback` with no deps: `useCallback((e) => setCount(window.innerWidth), [])`).""",

"""**Debug Scenario:**
A developer's Node.js `https.request` doesn't validate SSL certificates and passes security review quietly:

```ts
const req = https.request({
  hostname: 'api.example.com',
  path: '/data',
  rejectUnauthorized: false,  // Disables SSL verification!
}, (res) => { ... });
```

`rejectUnauthorized: false` disables certificate validation, making the connection vulnerable to man-in-the-middle attacks. Show: removing `rejectUnauthorized: false`, using `ca` option to provide a custom CA bundle for self-signed certificates in internal networks, the `NODE_EXTRA_CA_CERTS` environment variable for system-level custom CAs, and `NODE_TLS_REJECT_UNAUTHORIZED=0` as an env var (also insecure, also wrong).""",

"""**Debug Scenario:**
A developer's React component using `useImperativeHandle` doesn't expose the method to the parent — the ref is always `null`:

```tsx
const Input = forwardRef((props, ref) => {
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
    clear: () => { /* ... */ },
  }));
  return <input ref={inputRef} />;
});

// Parent:
const inputRef = useRef<HTMLInputElement>(); // Wrong type!
inputRef.current?.focus(); // focus() from useImperativeHandle, not DOM
```

The parent typed the ref as `HTMLInputElement` but `useImperativeHandle` returns a custom object, not the DOM element. Show: typing the ref as `useRef<{ focus: () => void; clear: () => void }>(null)`, defining an `InputHandle` interface for the exposed methods, and `forwardRef<InputHandle, InputProps>`.""",

"""**Debug Scenario:**
A developer's CSS `position: sticky` isn't working despite correct styling:

```css
.sticky-header {
  position: sticky;
  top: 0;      /* correct */
  z-index: 10; /* correct */
}
```

The sticky element isn't sticking. Investigation reveals the parent container has `overflow: hidden`:

```css
.parent {
  overflow: hidden; /* Breaks sticky positioning! */
}
```

`overflow: hidden/auto/scroll` on an ancestor breaks `sticky` positioning — the sticky element scrolls with the overflow container, not the viewport. Show: removing `overflow: hidden` from the ancestor (or changing to `overflow: clip`), finding the problematic ancestor with `getComputedStyle`, and `overflow: clip` as a safe alternative that doesn't create a scroll container.""",

"""**Debug Scenario:**
A developer's `Map` is growing unboundedly in a server that handles millions of requests:

```ts
const requestMetrics = new Map<string, RequestData>();

app.use((req, res, next) => {
  requestMetrics.set(req.id, { start: Date.now(), url: req.url });
  res.on('finish', () => {
    const data = requestMetrics.get(req.id);
    logMetrics(data!);
    // BUG: requestMetrics.delete(req.id) is missing!
  });
});
```

Every request adds to the Map but nothing removes it. After millions of requests, memory is exhausted. Show: adding `requestMetrics.delete(req.id)` in the `res.on('finish')` callback, using `WeakMap` (automatically GC'd when the key object is collected, though `req` objects may not be GC'd if other refs exist), and APM tools (Datadog, New Relic) for detecting memory leaks in production.""",

"""**Debug Scenario:**
A developer's service worker caches API responses and users see stale data after deployments:

```ts
// service-worker.js:
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request); // Return cached forever!
    })
  );
});
```

API responses are cached indefinitely — no expiry, no network update. Show: stale-while-revalidate strategy (return cache immediately, fetch update in background), cache-first with max-age check (check cache timestamp, refresh if older than 5 minutes), adding a version header check (if server version != cached version, bust cache), and the Workbox library for service worker caching strategies.""",

"""**Debug Scenario:**
A React application shows `NaN` in the UI because a numeric operation got a string somewhere in the chain:

```tsx
function TotalPrice({ items }: { items: Item[] }) {
  const total = items.reduce((sum, item) => sum + item.price, 0);
  return <div>Total: ${total.toFixed(2)}</div>;
}
// Shows: "Total: $NaN"
```

`item.price` is `"15.99"` (a string from the API), so `0 + "15.99"` = `"015.99"` then `"015.99" + "12.00"` = `"015.9912.00"` — actually `NaN` only shows if the first string addition produces something unparseable. Show: converting `item.price` with `Number(item.price)` or `parseFloat(item.price)`, Zod schema validation at the API boundary to ensure `price` is always a number, and TypeScript types that properly reflect the actual runtime data.""",

"""**Debug Scenario:**
A developer's `try/catch` around a promise chain doesn't catch rejections from `.then` callbacks:

```ts
try {
  const data = await fetch('/api/data')
    .then(r => r.json())
    .then(data => processData(data)); // If processData throws, is it caught?
} catch (e) {
  console.error('Caught:', e); // Yes, it IS caught when using await
}

// But without await:
fetch('/api/data')
  .then(r => r.json())
  .then(data => processData(data)); // Unhandled promise rejection!
// The try/catch block above is gone by the time this rejects
```

Show: always `await`ing promise chains, using `.catch()` on unwaited promises, `process.on('unhandledRejection')` in Node.js as a last resort, and the ESLint rule `@typescript-eslint/no-floating-promises`.""",

"""**Debug Scenario:**
A developer's OAuth redirect flow is breaking because `window.location.href` assignment gets blocked by the browser's popup blocker:

```tsx
function LoginButton() {
  const handleLogin = async () => {
    const { redirectUrl } = await getOAuthUrl(); // Async call!
    window.location.href = redirectUrl;          // Sometimes blocked!
  };
  return <button onClick={handleLogin}>Login</button>;
}
```

Popup blockers block `window.location.href` or `window.open` called from async code — the browser no longer considers it a direct user gesture. Show: pre-fetching the OAuth URL on button hover (or even on mount), storing it in state, then setting `window.location.href` directly in the synchronous `onClick` handler (before any `await`).""",

"""**Debug Scenario:**
A developer's custom event emitter leaks memory because arrow function event listeners can't be removed with `off`:

```ts
class Component {
  constructor(emitter: EventEmitter) {
    emitter.on('update', (data) => this.handleUpdate(data)); // arrow function — new ref each call
  }

  cleanup(emitter: EventEmitter) {
    emitter.off('update', (data) => this.handleUpdate(data)); // Different reference! Not removed!
  }
}
```

Show: storing the listener reference (`this.boundHandle = (data) => this.handleUpdate(data); emitter.on('update', this.boundHandle)`), then removing it (`emitter.off('update', this.boundHandle)`), or using a class-bound method (`handleUpdate = (data) => { ... }` as a class property).""",

"""**Debug Scenario:**
An Axios interceptor that refreshes JWT tokens creates infinite loops when the refresh endpoint itself returns 401:

```ts
axios.interceptors.response.use(null, async (error) => {
  if (error.response?.status === 401) {
    await refreshToken(); // If refresh ALSO returns 401 → infinite loop!
    return axios.request(error.config);
  }
  throw error;
});
```

If `refreshToken()` fails with 401, the interceptor catches it and tries to refresh again — endlessly. Show: checking a flag to prevent re-interception (`error.config._retry`), skipping the interceptor for the refresh endpoint URL itself, and clearing auth state + redirecting to login on refresh failure.""",

"""**Debug Scenario:**
A developer notices their React app's bundle size grew by 800KB after adding a charting library, even though only a simple line chart is used:

```ts
import { Chart } from 'chart.js'; // Imports ALL chart types — 800KB!

// But only LineChart is needed
```

Many libraries with a default namespace export bundle everything together. Show: using tree-shaking-compatible ES module imports (`import { Chart } from 'chart.js/auto'` vs selective imports), registering only needed chart components (`Chart.register(LineController, LinearScale, PointElement, LineElement)`), switching to a lighter alternative (`lightweight-charts` is 40KB), and checking the `webpack-bundle-analyzer` to confirm tree-shaking is working.""",

"""**Debug Scenario:**
A developer's Node.js app has a race condition where multiple concurrent requests create duplicate database records:

```ts
async function getOrCreateUser(email: string) {
  let user = await db.users.findUnique({ where: { email } });
  if (!user) {
    user = await db.users.create({ data: { email } }); // Race! Two requests can both findUnique null
  }
  return user;
}
```

Two concurrent requests both find no user, then both try to create — the second `create` fails with unique constraint violation. Show: handling the unique constraint violation (`catch (e) { if (e.code === 'P2002') return db.users.findUnique({ where: { email } }); throw e; }`), PostgreSQL `INSERT ... ON CONFLICT DO NOTHING RETURNING *`, and Prisma's `upsert`.""",

"""**Debug Scenario:**
A developer's `JSON.parse` silently truncates large integers from API responses:

```ts
const response = '{"orderId": 9007199254740993}'; // Larger than Number.MAX_SAFE_INTEGER
const parsed = JSON.parse(response);
console.log(parsed.orderId); // 9007199254740992 — truncated! Loss of precision
```

JavaScript `Number` can't safely represent integers above 2^53 - 1. Show: using `BigInt` with a custom JSON reviver (`JSON.parse(str, (key, val) => key === 'orderId' ? BigInt(val) : val)`), but the reviver receives the already-truncated number — need to process the raw JSON string, using `json-bigint` library for BigInt-safe parsing, or receiving the ID as a string in the API contract.""",

"""**Debug Scenario:**
A developer's service has `SIGTERM` handling but doesn't wait for in-flight database queries to complete before shutdown:

```ts
process.on('SIGTERM', () => {
  server.close(); // Stops accepting new connections
  process.exit(0); // Exits immediately! In-flight queries are killed
});
```

Kubernetes sends SIGTERM before killing the pod. Exiting immediately kills any pending database transactions. Show: waiting for the server to drain (`server.close(async () => { await db.$disconnect(); process.exit(0); })`), setting a maximum drain timeout (`setTimeout(() => process.exit(1), 30_000)`), draining the job queue, and signaling readiness probe to fail (remove from load balancer rotation) before closing.""",

"""**Debug Scenario:**
A developer's `useSyncExternalStore` implementation causes the component to re-render on every tick even when the store data hasn't changed:

```ts
const data = useSyncExternalStore(
  store.subscribe,
  () => ({ ...store.getState() }), // New object every call!
  () => ({ ...initialState }),
);
```

`getSnapshot` creates a new object every call — React sees it as a different value even when store data is unchanged, causing infinite re-renders. Show: memoizing the snapshot object (use `useRef` to cache the last snapshot, only return a new object if the data actually changed), or returning a stable primitive/same reference when data is unchanged (`return store.getState()` without spreading).""",

"""**Debug Scenario:**
A developer's `requestAnimationFrame` animation causes a stuttering effect on high refresh rate monitors (120Hz/165Hz):

```ts
function animate(timestamp: number) {
  // Target: 60fps animation — moves 1px per expected 16ms frame:
  element.style.left = `${position++}px`; // Moves 1px per frame
  requestAnimationFrame(animate);
}
```

At 120Hz, `requestAnimationFrame` fires every ~8ms instead of 16ms — the animation runs at double speed. Show: using `timestamp` delta time to calculate movement based on elapsed time (not frame count): `const delta = timestamp - lastTime; position += speed * delta / 1000; lastTime = timestamp`, making the animation frame-rate independent.""",

"""**Debug Scenario:**
A developer's React app breaks with "Hydration mismatch" errors when using `Math.random()` to generate IDs for SSR:

```tsx
function Tag({ label }: { label: string }) {
  const id = `tag-${Math.random()}`; // Server: 0.123, Client: 0.456!
  return <span id={id}>{label}</span>;
}
```

`Math.random()` is non-deterministic — server and client generate different values, causing hydration mismatch. Show: using React 18's `useId` hook (generates stable, SSR-consistent IDs), a sequential counter with `useRef`, or a content-based hash (`slugify(label)`) which is deterministic.""",

"""**Debug Scenario:**
A developer's TypeScript `as` assertion causes a silent runtime crash that TypeScript didn't prevent:

```ts
const value: unknown = { name: 'Alice' };
const user = value as User; // TypeScript allows this
console.log(user.email.toLowerCase()); // Runtime: Cannot read properties of undefined!
```

`as User` tells TypeScript "trust me" — but `value` doesn't actually have `email`. TypeScript's type assertions don't perform runtime checks. Show: using a type guard or Zod schema to validate before asserting (`const result = UserSchema.safeParse(value); if (result.success) use(result.data)`), `instanceof` for class types, and when `as` is safe (e.g., narrowing within a function that's already type-guarded).""",

"""**Debug Scenario:**
A developer's CSS animation doesn't work on a transformed parent because of an unexpected stacking context:

```css
.parent {
  transform: translateZ(0); /* Creates a containing block! */
}
.child {
  position: fixed; /* Is supposed to position relative to viewport... */
  top: 0; left: 0; /* But actually positions relative to .parent! */
}
```

`position: fixed` is positioned relative to the viewport UNLESS an ancestor has `transform`, `will-change`, `filter`, or `backdropFilter` — those create a new containing block. Show: checking all ancestors for the containing block triggers, moving the fixed element outside the transformed parent in the DOM, and using `position: sticky` (which uses the scroll container, not containing block) as an alternative.""",

"""**Debug Scenario:**
A developer's Cloud Run container fails to start with "container failed to start and listen on the port defined by the PORT environment variable":

```ts
const PORT = 3000; // Hardcoded!
app.listen(PORT, () => console.log(`Listening on ${PORT}`));
```

Cloud Run (and other container platforms) dynamically assign a port via the `PORT` environment variable. Hardcoding 3000 means the container listens on 3000 but the platform sends traffic to the dynamic port. Show: `const PORT = process.env.PORT ?? 3000`, the `0.0.0.0` vs `localhost` binding (`app.listen(PORT, '0.0.0.0')` to accept external connections), and `process.env.PORT` awareness in Docker vs local dev.""",

"""**Debug Scenario:**
A developer's React `key` prop prevents unwanted re-mounts but accidentally causes wanted re-mounts to not happen:

```tsx
<SearchResults key={query} results={filteredResults} />
// key=query: remounts when query changes ✓ (resets scroll, state)

// But:
<UserProfile key={activeTab} userId={userId} />
// key=activeTab: remounts when tab changes (fine)
// BUT also remounts when userId changes (userId is not in the key!)
// When userId changes, the component should reset — key doesn't change!
```

Show: including all relevant "reset triggers" in the key (`key={`${userId}-${activeTab}`}`), and understanding that `key` changes force a full remount (new DOM, new state, new refs — expensive for complex components). Alternative: `useEffect([userId], resetState)` for soft resets without remounting.""",

"""**Debug Scenario:**
A developer's Prisma query returns records from a soft-deleted table because they forgot to add the `deletedAt: null` filter:

```ts
// Model has: deletedAt DateTime? (soft deletes — null = not deleted)
const users = await prisma.user.findMany({
  where: { role: 'admin' },
  // Missing: deletedAt: null!
});
// Returns deleted admins!
```

Show: adding `deletedAt: null` to all queries, implementing a Prisma middleware/extension that automatically adds `WHERE deletedAt IS NULL` to all findMany queries, and `prisma.$extends({ query: { user: { findMany({ args, query }) { args.where = { ...args.where, deletedAt: null }; return query(args); } } } })`.""",

]

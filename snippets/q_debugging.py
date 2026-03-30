"""
snippets/q_debugging.py — BATCH 7: 56 brand-new Debugging questions
Zero overlap with batches 1-6 archives.
"""

Q_DEBUGGING = [

'''**Debug Scenario:**
A developer's Node.js process memory grows steadily from 200MB to 2GB over 24 hours with no obvious leak in application code:

```ts
const EventEmitter = require('events');
const emitter = new EventEmitter();

app.post('/subscribe', (req, res) => {
  emitter.on('data', (d) => res.write(d)); // Listener added per request, never removed!
  req.on('close', () => { /* forgot to remove emitter listener */ });
});
```

Each HTTP request adds an event listener to the global emitter that's never removed (no `emitter.off`). After thousands of requests, the emitter holds thousands of stale listeners (and their closures, keeping `res` alive). Show: `emitter.once('data', handler)` for single-fire listeners, storing the handler reference for `emitter.off('data', handler)` in `req.on('close', ...)`, `emitter.setMaxListeners(20)` to detect leaks early (Node.js warns at 11 by default), and heap snapshot analysis in Chrome DevTools.''',

'''**Debug Scenario:**
A developer's `async/await` error is silently swallowed in an Express route handler:

```ts
app.get('/users', async (req, res) => {
  const users = await db.users.findMany(); // If this throws...
  res.json(users);
  // ...Express doesn't know! req hangs forever until timeout
});
```

In Express 4, unhandled promise rejections in route handlers don't trigger the error middleware — the request hangs. Show: wrapping with a `asyncWrapper` HOF: `const wrap = (fn) => (req, res, next) => fn(req, res, next).catch(next)`, using `express-async-errors` package (monkey-patches Express), or upgrading to Express 5 (which handles async errors natively), and global `process.on('unhandledRejection', ...)` as a circuit breaker.''',

'''**Debug Scenario:**
A developer's `Promise.all` fails silently because one promise rejects but it's not in the array:

```ts
async function processOrders(orders: Order[]) {
  const savePromise = db.save(orders); // NOT in Promise.all!
  await Promise.all([
    sendConfirmationEmails(orders),
    updateInventory(orders),
  ]);
  await savePromise; // If this rejects, it's an unhandled rejection by then
}
```

`savePromise` is created before `Promise.all`, so if it rejects while `Promise.all` is running, the rejection is unhandled (Node.js 15+ exits on unhandled rejections). Show: including all promises in `Promise.all`, using `Promise.allSettled` for non-critical tasks, and the subtle timing issue where a rejected promise not in `Promise.all` fires its rejection event independently.''',

'''**Debug Scenario:**
A developer's React component causes "Maximum update depth exceeded" because of a missing dependency in `useEffect`:

```tsx
const [filters, setFilters] = useState({ search: '', category: '' });

useEffect(() => {
  // Fetch with current filters:
  fetchProducts(filters).then(setProducts);
  // Update filter stats (triggers re-render → useEffect runs again!):
  setFilters(prev => ({ ...prev, lastFetched: Date.now() })); // Infinite loop!
}, [filters]); // 'filters' changes every time → re-run → update filters → re-run
```

`setFilters` inside the `useEffect` updates `filters`, which is a dep, which triggers the effect again. Show: separating the stats update from the product fetch (different `useEffect` with different deps), using a `useRef` for `lastFetched` (doesn't trigger re-render), and the React ESLint exhaustive-deps rule catching this pattern.''',

'''**Debug Scenario:**
A developer's `try/catch` doesn't catch errors from async event listeners:

```ts
try {
  emitter.emit('process-data', payload);
  // Event listener is async — errors escape the try/catch!
} catch (err) {
  logger.error('Failed to process', err); // Never called on async listener error
}

emitter.on('process-data', async (payload) => {
  await heavyProcessing(payload); // If this throws, the error goes to 'unhandledRejection'
});
```

`emitter.emit` is synchronous — it returns before the async listener's promise settles. Errors from the async listener escape to `unhandledRejection`. Show: wrapping the listener in `.catch()`  (`async (payload) => { try { await heavyProcessing(payload); } catch (err) { emitter.emit('error', err); } }`), listening to `emitter.on('error', ...)`, and `EventEmitter2` for async-aware emit.''',

'''**Debug Scenario:**
A developer's `JSON.stringify` unexpectedly produces `null` for a `Date` stored in state:

```ts
const event = { title: 'Meeting', date: new Date('2024-06-15') };
const serialized = JSON.stringify(event);
// '{"title":"Meeting","date":"2024-06-15T00:00:00.000Z"}' ← date is a string now!

const parsed = JSON.parse(serialized);
parsed.date.getMonth(); // TypeError: parsed.date.getMonth is not a function!
```

`JSON.stringify` calls `.toISOString()` on Date objects (via `toJSON`), producing a string — so `JSON.parse` gives a string, not a Date. Show: using a custom reviver in `JSON.parse` to reconstruct Dates, `superjson` library (handles `Date`, `Map`, `Set`, `bigint` etc.), and Zod's `z.coerce.date()` for safe parsing.''',

'''**Debug Scenario:**
A developer's `axios` interceptor causes an infinite retry loop on 401 errors:

```ts
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const newToken = await refreshToken();
      error.config.headers.Authorization = `Bearer ${newToken}`;
      return axios(error.config); // Retried request also gets 401 → retried again → loop!
    }
    return Promise.reject(error);
  }
);
```

If the token refresh succeeds but the retried request still gets 401 (e.g., insufficient permissions, not expiry), the interceptor fires again — infinite loop. Show: adding a `_retry` flag to `error.config` (`if (error.config._retry) return Promise.reject(error); error.config._retry = true`), and checking the original URL isn't the token refresh endpoint itself.''',

'''**Debug Scenario:**
A developer's SQL query is vulnerable to second-order SQL injection via a stored value:

```ts
// First request: Stores malicious username
await db.query('INSERT INTO users (name) VALUES ($1)', ["'; DROP TABLE users; --"]);
// Parameterized — safe ✓ (stored as literal string)

// Second request: Uses stored value UNSAFELY
const user = await db.query('SELECT * FROM users WHERE name = \'' + storedUsername + '\'');
// storedUsername = "'; DROP TABLE users; --"
// Executes: SELECT * FROM users WHERE name = ''; DROP TABLE users; --'
```

Safe writes + unsafe reads = second-order injection. The value was safely stored but unsafely used later. Show: ALWAYS using parameterized queries even for data read from the database (`db.query('SELECT ... WHERE name = $1', [storedUsername])`), and an ORM like Prisma that makes parameterized queries the default.''',

'''**Debug Scenario:**
A developer's WebSocket connection disconnects silently after 60 seconds of inactivity:

```ts
const ws = new WebSocket('wss://api.example.com/ws');
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => handleMessage(e.data);
// No heartbeat! Load balancer/proxy closes idle connections after 60s
ws.onclose = (e) => console.log('Disconnected', e.code, e.reason);
```

AWS ALB, nginx, and cloud load balancers close idle TCP connections after 60 seconds by default. Show: implementing a ping/pong heartbeat (`setInterval(() => ws.send(JSON.stringify({ type: 'ping' })), 30_000)`, clear interval on close), the WebSocket `ping` frame (server-side heartbeat), and reconnection with exponential backoff on `onclose`.''',

'''**Debug Scenario:**
A developer's `useLayoutEffect` causes a "Warning: useLayoutEffect does nothing on the server" in a Next.js SSR context:

```tsx
function MeasuredComponent() {
  const ref = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    setWidth(ref.current!.offsetWidth); // Needs DOM — can't run on server
  }, []);
}
```

`useLayoutEffect` doesn't run during SSR — React warns about it. Show: the standard solution `const useIsomorphicLayoutEffect = typeof window !== 'undefined' ? useLayoutEffect : useEffect`, using `useEffect` when the DOM measurement isn't needed before first paint, and `suppressHydrationWarning` as a last resort for elements that differ between server and client renders.''',

'''**Debug Scenario:**
A developer's `for...in` loop on an array produces unexpected behavior because it iterates prototype properties:

```ts
Array.prototype.customMethod = () => 'custom';

const arr = [1, 2, 3];
for (const key in arr) {
  console.log(key); // '0', '1', '2', 'customMethod' — unexpected!
}
```

`for...in` iterates ALL enumerable properties including inherited ones from the prototype. Show: using `for...of` for arrays (iterates values, not indices), `arr.forEach`/`arr.map` for functional iteration, `for...in` with `Object.prototype.hasOwnProperty.call(obj, key)` check for safe object iteration, and why `for...in` is generally wrong for arrays.''',

'''**Debug Scenario:**
A developer's `console.log` shows `{}` for a non-empty object in Chrome DevTools:

```ts
const obj = { users: [], loaded: false };
console.log(obj); // Shows: {} in collapsed view!
// Expanding it shows the properties — but the collapsed view is misleading
```

Chrome DevTools lazy-evaluates object references in `console.log` — if the object is mutated after logging, the logged output reflects the CURRENT state (not the state at log time). Show: `console.log(JSON.parse(JSON.stringify(obj)))` for a snapshot (but loses non-JSON types), `console.log({ ...obj })` for a shallow copy, structured clone (`structuredClone(obj)`), and the Chrome DevTools `Store as global variable` feature for debugging.''',

'''**Debug Scenario:**
A developer's TypeScript code compiles successfully but `undefined is not a function` at runtime because of optional chaining misuse:

```ts
const config = getConfig();
const port = config?.server?.getPort();
// If config is undefined: port = undefined (no error)
// But if config exists and server exists, but getPort doesn't exist:
// TypeError: config.server.getPort is not a function
```

`?.` short-circuits to `undefined` if a value in the chain is null/undefined — but it doesn't protect against calling a non-function. Show: `typeof config?.server?.getPort === 'function'` check, TypeScript strict null checks catching `getPort()` returning `undefined`, and `!` non-null assertion vs `?.` optional chaining (different guarantees).''',

'''**Debug Scenario:**
A developer's `parseInt` returns `NaN` despite receiving a seemingly valid number string:

```ts
const userInput = '  42px  ';
console.log(parseInt(userInput));        // 42 — works (parses up to non-numeric)
console.log(parseInt('0x1F'));           // 31 — hexadecimal
console.log(parseInt('123', 10));        // 123 — correct base-10
console.log(parseInt('   '));            // NaN
console.log(parseInt('', 10));           // NaN

// The bug:
const value = parseInt(req.query.id);    // If req.query.id is an array: parseInt(['1','2']) = 1 (!)
```

`parseInt` coerces its argument to string — arrays become comma-joined. Show: `Number(value)` as a stricter alternative (NaN for partial parses like '42px'), `+value` (same as Number), always passing radix 10 (`parseInt(v, 10)`), and validating `req.query.id` is a string before parsing.''',

'''**Debug Scenario:**
A developer's fetch request to a REST API fails with CORS errors only in production:

```ts
// Works in development (Vite proxy):
const data = await fetch('/api/users').then(r => r.json());

// Fails in production with: 
// "Access-Control-Allow-Origin header missing"
```

In development, Vite's `proxy` option forwards `/api/*` to the backend (same origin, no CORS). In production, the frontend is hosted on `cdn.example.com` and makes cross-origin requests to `api.example.com` — no CORS headers. Show: adding CORS middleware to the API server (`cors({ origin: 'https://cdn.example.com', credentials: true })`), pre-flight `OPTIONS` handling, credentials CORS (`withCredentials: true` on fetch + `Access-Control-Allow-Credentials: true` server-side), and why `Access-Control-Allow-Origin: *` can't be used with credentials.''',

'''**Debug Scenario:**
A developer's Prisma query returns stale data after an update because of the connection pool caching:

```ts
await prisma.product.update({ where: { id: 'p1' }, data: { price: 99 } });
const product = await prisma.product.findUnique({ where: { id: 'p1' } });
console.log(product?.price); // Still shows 49! (stale read)
```

Prisma's connection pool can route the `findUnique` to a different replica (read replica) that hasn't received the write yet. Show: adding `$transaction([update, findUnique])` to ensure both operations on the same connection, using `prisma.$queryRaw` with `SET TRANSACTION` isolation level, the `directUrl` (primary) vs `url` (replica) Prisma configuration, and explicitly routing reads to the primary after writes.''',

'''**Debug Scenario:**
A developer's `Object.assign` doesn't perform a deep merge, causing nested property deletion:

```ts
const defaults = { server: { host: 'localhost', port: 3000, ssl: true }, db: { url: '...' } };
const userConfig = { server: { port: 8080 } };

const config = Object.assign({}, defaults, userConfig);
// Expected: { server: { host: 'localhost', port: 8080, ssl: true }, db: { url: '...' } }
// Actual:   { server: { port: 8080 }, db: { url: '...' } }
// userConfig.server REPLACES defaults.server entirely!
```

`Object.assign` does a shallow merge. Show: deep merge using Lodash `_.merge(defaults, userConfig)`, recursive custom `deepMerge` function, structured clone + object spread for pure objects, and the spread operator having the same shallow-merge issue (`{...defaults, ...userConfig}`).''',

'''**Debug Scenario:**
A developer's CSS-in-JS (styled-components) causes class name mismatches during SSR with Next.js:

```
Warning: Prop `className` did not match.
Server: "sc-abc123"
Client: "sc-def456"
```

Styled-components generates class names based on a counter — in SSR, it starts from 0, but on the client it continues from wherever the last client render left off (or resets differently). Show: adding `ServerStyleSheet` + `_document.tsx` integration for SSR, using the `babel-plugin-styled-components` (stable class names based on component name + file), and styled-components v6's `displayName` feature (deterministic class names without Babel plugin).''',

'''**Debug Scenario:**
A developer's `Array.prototype.sort` produces different orderings across browsers for equal elements:

```ts
const users = [
  { name: 'Alice', score: 100 },
  { name: 'Bob',   score: 100 },  // Same score as Alice!
  { name: 'Carol', score: 100 },
];

users.sort((a, b) => b.score - a.score);
// Chrome: [Alice, Bob, Carol] (stable — original order preserved for equals)
// Older Safari: [Carol, Alice, Bob] (unstable — arbitrary order for equals)
```

JavaScript `Array.sort` is guaranteed stable since ES2019, but older engines aren't. Show: adding a tiebreaker (`b.score !== a.score ? b.score - a.score : a.name.localeCompare(b.name)`), use of `Intl.Collator` for locale-aware string comparisons, and the ECMAScript 2019 stability guarantee.''',

'''**Debug Scenario:**
A developer's event delegation stops working when a child button is clicked because `event.target` points to an icon inside the button:

```ts
list.addEventListener('click', (e) => {
  if (e.target.dataset.action === 'delete') { // Works only if the <li> itself is clicked!
    deleteItem(e.target.dataset.id);
  }
});

// HTML: <li data-action="delete" data-id="1"><button><svg>...</svg></button></li>
// Clicking the SVG: e.target = <svg> (no dataset.action!)
```

`e.target` is the element actually clicked — which may be a deeply nested child. Show: using `e.target.closest('[data-action="delete"]')` to walk up to the intended element, `e.currentTarget` (always the element the listener is attached to, not the target), and element matching with `.matches('[data-action]')`.''',

'''**Debug Scenario:**
A developer's Redis `INCR` counter skips values under concurrent load:

```ts
// Naive counter without atomic increment:
const current = parseInt(await redis.get('counter') ?? '0');
await redis.set('counter', current + 1); // Read-modify-write: NOT atomic!

// Two concurrent requests both read '5', both set '6' — one increment lost!
```

`GET + SET` is a non-atomic read-modify-write — race condition. Show: using `INCR` command (atomic: `redis.incr('counter')`), `INCRBY` for incrementing by N, Redis transactions with `MULTI/EXEC` + `WATCH` for conditional increments, and Lua scripts for complex atomic operations.''',

'''**Debug Scenario:**
A developer's GitHub Actions CI pipeline runs `npm install` on every push but doesn't use the cache:

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
  with:
    node-version: '20'
- run: npm install  # Always fresh install — cache never used!
```

`actions/cache` isn't configured, and `actions/setup-node`'s built-in cache isn't enabled. Show:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'      # or 'yarn', 'pnpm'
```

Also shows the manual cache approach (`actions/cache` using `~/.npm` keyed on `package-lock.json` hash), and `npm ci` instead of `npm install` for reproducible installs in CI.''',

'''**Debug Scenario:**
A developer's IndexedDB transaction fails silently because it's accessed after the transaction completes:

```ts
const txn = db.transaction('users', 'readwrite');
const store = txn.objectStore('users');

store.put({ id: '1', name: 'Alice' });

await new Promise(resolve => txn.oncomplete = resolve);

// BUG: Accessing transaction after it's committed:
const request = store.get('1'); // InvalidStateError: transaction has finished
```

IDB transactions auto-commit when no more requests are queued — the transaction is done after `oncomplete` fires. Show: reading from the store BEFORE `oncomplete` (within the same transaction), opening a new transaction for the read, and wrapping IDB operations in a library like `idb` (Jake Archibald) that provides proper Promise semantics.''',

'''**Debug Scenario:**
A developer's `navigator.geolocation.getCurrentPosition` works in development but always triggers the error callback in production:

```ts
navigator.geolocation.getCurrentPosition(
  (pos) => setLocation(pos),
  (err) => console.error('Geolocation denied', err)); // Always fires in production!
```

In production, the site is served over HTTP (not HTTPS) — the Geolocation API requires a secure context (HTTPS or localhost). Also, the user may have denied the permission. Show: checking `navigator.permissions.query({ name: 'geolocation' })` for the current permission state, enforcing HTTPS in production (mandatory for location API), and handling `err.code` values (`PERMISSION_DENIED: 1`, `POSITION_UNAVAILABLE: 2`, `TIMEOUT: 3`).''',

'''**Debug Scenario:**
A developer's Next.js `getServerSideProps` function causes high server CPU because it's called on every request including prefetches:

```ts
export async function getServerSideProps(context) {
  const products = await db.products.findMany(); // Heavy query!
  return { props: { products } };
}
// Next.js's <Link prefetch> calls this handler for every link in the viewport!
```

Every `<Link>` that enters the viewport triggers a prefetch request to `getServerSideProps` — even for pages not yet visited. Show: disabling prefetch for pages with heavy SSR (`<Link prefetch={false}>`), migrating to ISR (`getStaticProps` + `revalidate`) for content that doesn't need per-request freshness, and caching the DB query result for the remainder of the request window (`cache('...', () => db.query())`).''',

'''**Debug Scenario:**
A developer's regex fails to match multiline strings because `.` doesn't match newlines by default:

```ts
const text = "Hello\nWorld";
const match = text.match(/Hello.World/);
// null! '.' does not match '\n' unless the 's' (dotAll) flag is used
```

Show: using the `s` flag (`/Hello.World/s`) for dotAll mode (`.` matches `\n`), `[\s\S]` as a pre-ES2018 workaround, `m` (multiline) flag changes `^`/`$` to match line starts/ends (not the same as `s`), and the regex flags: `i` (case insensitive), `g` (global), `m` (multiline), `s` (dotAll), `u` (Unicode), `v` (Unicode sets, ES2024).''',

'''**Debug Scenario:**
A developer's cookie is not sent to the API because of `SameSite` and `Secure` attribute mismatches:

```ts
// Server sets cookie:
res.cookie('session', token, {
  httpOnly: true,
  // Missing: sameSite and secure attributes
});

// Client fetch:
await fetch('/api/data', { credentials: 'include' }); // Cookie not sent!
```

Modern browsers default to `SameSite=Lax` — cookies with `SameSite=Lax` are sent on same-origin requests but not on cross-origin requests (even with `credentials: include`). And if the API is on a different subdomain, the cookie needs `SameSite=None; Secure`. Show: setting `{ sameSite: 'none', secure: true }` for cross-domain cookies, `{ sameSite: 'lax', secure: false }` for localhost development, and the difference between `SameSite=Strict` (never cross-site), `Lax` (GET navigations only), and `None` (all cross-site if Secure).''',

'''**Debug Scenario:**
A developer's `setInterval` inside a React component accumulates multiple intervals rather than replacing the previous one:

```tsx
function LiveCounter() {
  const [count, setCount] = useState(0);
  const [interval, setInterval] = useState(1000);

  useEffect(() => {
    const id = setInterval(() => setCount(c => c + 1), interval);
    // Missing cleanup! Previous interval keeps running when 'interval' changes
  }, [interval]); // Re-runs when interval changes, but doesn't clear old one
}
```

Each time `interval` changes, a new `setInterval` is created without clearing the previous. After 5 changes, 5 intervals fire simultaneously. Show: returning `() => clearInterval(id)` from the effect, the `useInterval` custom hook pattern, and `setCount(c => c + 1)` (functional update — doesn't need `count` as a dep).''',

'''**Debug Scenario:**
A developer's `Promise.race` doesn't actually cancel the losing promises:

```ts
const result = await Promise.race([
  fetchCritical(),
  new Promise<never>((_, reject) => setTimeout(reject, 5000, new Error('Timeout'))),
]);
// fetchCritical() still runs in the background even after the timeout wins!
```

`Promise.race` only races the settlement — the underlying operations (HTTP request, DB query) are not cancelled. Show: using `AbortController` with the race: pass `signal` to `fetch`, calling `controller.abort()` when the timeout wins, `React Query` and `TanStack Query` using `AbortController` automatically for cancelled queries, and the cleanup pattern in `useEffect` races.''',

'''**Debug Scenario:**
A developer's Zustand store actions don't reflect state changes when called in rapid succession:

```ts
const useStore = create((set, get) => ({
  items: [] as Item[],
  addItem: (item: Item) => {
    const current = get().items; // Gets state at call time
    set({ items: [...current, item] });
  },
}));

// Called rapidly:
store.getState().addItem(item1); // items: [item1]
store.getState().addItem(item2); // items: [item1, item2] — actually fine in Zustand
// Zustand's set is synchronous — no stale closure issue like useState
```

Zustand actually handles this correctly. The real bug: using `useState` with callbacks for the same pattern:

```ts
const [items, setItems] = useState([]);
// In a loop:
setItems([...items, item1]); // 'items' is stale in the closure!
setItems([...items, item2]); // Both use the same original 'items' → only item2 added!
setItems(prev => [...prev, item2]); // ✓ Uses functional update
```

Show: functional state updates in React (`setItems(prev => [...prev, item])`), and Zustand's `set(state => ({ items: [...state.items, item] }))` functional form.''',

'''**Debug Scenario:**
A developer's fetch with `keepalive: true` for analytics doesn't work when the page is closing because the payload is too large:

```ts
window.addEventListener('beforeunload', () => {
  fetch('/api/analytics', {
    method: 'POST',
    keepalive: true,
    body: JSON.stringify(largeEventBatch), // 200KB payload
  });
  // In Chrome, keepalive requests are limited to 64KB! Larger requests are silently dropped.
});
```

The `keepalive` flag has a 64KB payload limit. Show: using `navigator.sendBeacon('/api/analytics', payload)` (65536 byte limit, queued by browser), compressing the payload before sending, batching events and sending regularly instead of on unload, and `visibilitychange` to `'hidden'` as a more reliable unload hook than `beforeunload`.''',

'''**Debug Scenario:**
A developer's module federation remote module fails to load in production due to `publicPath` misconfiguration:

```js
// webpack.config.js of remote app:
module.exports = {
  output: {
    publicPath: 'auto',  // Fine in development!
    // In production, CDN serves from 'https://assets.cdn.example.com/'
    // but the main app (host) is at 'https://app.example.com/'
    // 'auto' resolves relative to the host — loads wrong URLs
  },
};
```

`publicPath: 'auto'` uses the current document's base URL to resolve chunk URLs. When the host and remote have different domains, chunks resolve to the wrong base. Show: setting an explicit `publicPath` for the remote (`publicPath: 'https://assets.cdn.example.com/'`), or using the `__webpack_public_path__` runtime variable for dynamic configuration, and Module Federation's `remoteEntry.js` URL configuration in the host.''',

'''**Debug Scenario:**
A developer's CSS animation causes janky 30fps performance because it's animating `height` instead of `transform`:

```css
.panel {
  height: 0;
  overflow: hidden;
  transition: height 300ms ease;
}
.panel.open {
  height: 200px;
}
/* Smooth in Firefox but janky in Chrome on complex pages */
```

Animating `height` triggers Layout → Paint → Composite on every frame (browser's most expensive path). Show: using `max-height` trick (limited but avoids layout), Grid animation (`grid-template-rows: 0fr → 1fr`, GPU-accelerated in modern browsers), animating `transform: scaleY()` (cheap: Composite only), `FLIP` animation technique for animating height changes, and the Chrome DevTools Performance panel showing "Layout" recalculations.''',

'''**Debug Scenario:**
A developer's SVG animation flickers on scroll because it uses `position: fixed` combined with CSS transforms:

```css
.svg-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(var(--angle));
  will-change: transform;
}
/* When scrolling on iOS Safari: occasional white flicker */
```

iOS Safari has known issues with `position: fixed` + CSS transforms — particularly when scrolling (the fixed element may repaint unexpectedly). Show: using `position: absolute` with JavaScript positioning for the SVG, avoiding `transform` on `position: fixed` elements (use `top/left` adjustments instead), setting `transform: translateZ(0)` (forces GPU layer, may reduce flicker), and testing in actual iOS Safari vs simulators.''',

'''**Debug Scenario:**
A developer's WebAssembly module instantiation throws "Wasm code generation disallowed by embedder" in production:

```ts
const wasmModule = await WebAssembly.instantiateStreaming(fetch('/module.wasm'));
// Error in production: "Wasm code generation disallowed by embedder"
```

The Content Security Policy on the production server has `script-src 'self'` without `'unsafe-eval'` or `'wasm-unsafe-eval'`. WebAssembly JIT compilation is treated as dynamic code generation and blocked by CSP. Show: adding `'wasm-unsafe-eval'` to the `script-src` directive (Chrome 97+, Firefox, Safari), the older `'unsafe-eval'` fallback, and why `'unsafe-eval'` for JS (bad) is distinct from `'wasm-unsafe-eval'` (safer — only allows Wasm JIT, not arbitrary eval).''',

'''**Debug Scenario:**
A developer's drag-and-drop implementation stops working on touch devices because it's built with mouse events only:

```ts
element.addEventListener('mousedown', startDrag);
document.addEventListener('mousemove', moveDrag);
document.addEventListener('mouseup', endDrag);
// Works on desktop. On mobile: no drag at all!
```

Mobile browsers fire `touch*` events, not `mouse*` events (though some simulate mouse events after touch — causing double-firing). Show: adding parallel `touchstart`, `touchmove`, `touchend` listeners with `e.touches[0]` for coordinates, `e.preventDefault()` in `touchstart` to stop scroll interference, or switching to the `Pointer Events` API (`pointerdown`, `pointermove`, `pointerup`) which unifies mouse and touch (`pointer-events: auto`).''',

'''**Debug Scenario:**
A developer's `localStorage` write fails silently in Safari's private browsing mode:

```ts
try {
  localStorage.setItem('key', 'value');
} catch (e) {
  // QuotaExceededError thrown in Safari private mode — even for the first write!
}
// App assumes localStorage works and breaks when it doesn't
```

Safari private mode limits `localStorage` to 0 bytes — any write throws `QuotaExceededError`. Show: wrapping all `localStorage` operations in try/catch, an `isLocalStorageAvailable()` check (`try { localStorage.setItem('__test', '1'); localStorage.removeItem('__test'); return true; } catch { return false; }`), falling back to an in-memory Map, and `sessionStorage` (also limited in private mode).''',

'''**Debug Scenario:**
A developer's Vitest test fails on Windows CI but passes on Mac because of `path.join` vs forward slashes:

```ts
// Test imports a file by constructing the path:
const filePath = `src/components/${componentName}.tsx`;
// import(filePath) → fails on Windows with ENOENT!
// Windows expects: 'src\\components\\ComponentName.tsx'
```

Hardcoded forward slashes in import paths cause issues on Windows. Show: using `path.join('src', 'components', `${componentName}.tsx`)` (OS-aware), `path.resolve(__dirname, ...)` for absolute paths, and the fact that Node.js module resolution actually handles forward slashes on Windows (the issue is usually with `fs` operations, not `import`). Also check for case-sensitivity differences between Mac (case-insensitive) and Linux CI (case-sensitive).''',

'''**Debug Scenario:**
A developer's `useContext` causes all consumers to re-render when any part of the context value changes:

```tsx
const AppContext = createContext({ user: null, theme: 'light', locale: 'en', notifications: [] });

function Layout() {
  const [notifications, setNotifications] = useState([]);
  const [user, setUser] = useState(null);

  return (
    <AppContext.Provider value={{ user, notifications, theme: 'light', locale: 'en' }}>
      {/* New object every render → ALL consumers re-render even if user didn't change */}
      <ThemeToggle />     {/* Only needs theme */}
      <UserAvatar />      {/* Only needs user */}
      <NotifBadge />      {/* Only needs notifications */}
    </AppContext.Provider>
  );
}
```

A single monolithic context causes unnecessary re-renders. Show: splitting into separate contexts (`ThemeContext`, `UserContext`, `NotifContext`) each with its own provider, `useMemo` for the context value (`useMemo(() => ({ user, notifications }), [user, notifications])`), and `use-context-selector` library for selector-based subscriptions.''',

'''**Debug Scenario:**
A developer's environment variables are undefined at runtime in a Vite React app but defined in `.env`:

```ts
// .env:
SECRET_KEY=abc123
VITE_API_URL=https://api.example.com

// Component:
console.log(import.meta.env.SECRET_KEY);   // undefined!
console.log(import.meta.env.VITE_API_URL); // "https://api.example.com" ✓
```

Vite only exposes env variables prefixed with `VITE_` to the browser (for security — don't expose server secrets). Variables without the prefix remain server-only. Show: renaming to `VITE_SECRET_KEY` (not recommended for secrets), using server-side env for sensitive values, `import.meta.env.MODE` (`'development'` or `'production'`), and `VITE_` prefix convention vs `NEXT_PUBLIC_` in Next.js.''',

]

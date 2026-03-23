"""
snippets/q_debugging.py — BATCH 5: 28 brand-new Debugging questions
Zero overlap with batch1, batch2, batch3, or batch4 archives.
"""

Q_DEBUGGING = [

"""**Debug Scenario:**
A React component conditionally renders a hook, which violates the Rules of Hooks:

```tsx
function UserProfile({ isLoggedIn }) {
  if (!isLoggedIn) {
    return <LoginPrompt />;  // early return BEFORE hooks
  }
  const user = useCurrentUser(); // called conditionally!
  const { data } = useQuery(['user', user.id], fetchUser);
  return <Profile user={data} />;
}
```

Hooks must be called in the same order on every render. The conditional early return changes the hook call order. Show: restructuring to hoist ALL hooks before any conditional `return`, or splitting into two components (`<AuthenticatedProfile>` contains all hooks, `<UserProfile>` decides which to render), and the ESLint rule `react-hooks/rules-of-hooks` that catches this pattern at development time.""",

"""**Debug Scenario:**
A developer uses `Object.assign({}, defaultConfig, userConfig)` to merge configs, but deeply nested properties are overwritten instead of merged:

```ts
const defaultConfig = { server: { port: 3000, timeout: 5000 }, db: { poolSize: 10 } };
const userConfig    = { server: { port: 8080 } };

const config = Object.assign({}, defaultConfig, userConfig);
// Result: { server: { port: 8080 }, db: { poolSize: 10 } }
//         ^^^^^^^^^^^^^^^^^^^^^^^^
// server.timeout is lost! Object.assign is shallow.
```

Show: deep merge using `JSON.parse(JSON.stringify(base))` (only for JSON-safe configs), recursive `deepMerge(target, source)` that recursively merges nested objects, `lodash.merge` as a well-tested solution, and the structural difference between lodash `merge` (mutates target) and lodash `mergeWith` (custom merger per field).""",

"""**Debug Scenario:**
A React app fails with "Objects are not valid as a React child" but the component looks correct:

```tsx
function ErrorDisplay({ error }) {
  return <div>{error}</div>;  // error is an Error object, not a string
}

<ErrorDisplay error={new Error('Not found')} />
```

React can render strings, numbers, booleans, arrays, and React elements — but NOT plain objects (including `Error` instances). Show: rendering `error.message` instead of the entire error object, adding a fallback `String(error)` for unknown error shapes, the TypeScript fix (type `error` as `string | Error` and narrow before rendering), and a generic `<ErrorDisplay error: unknown>` component that handles all error shapes gracefully.""",

"""**Debug Scenario:**
A form validation function uses `async/await` inside a loop but the validations aren't running in parallel:

```ts
async function validateAll(fields: Field[]) {
  const errors: ValidationError[] = [];
  for (const field of fields) {
    const error = await validateField(field); // sequential — each waits for the last
    if (error) errors.push(error);
  }
  return errors;
}
// Time: sum of all validation times (e.g., 5 × 200ms = 1000ms)
```

Show: replacing the sequential `for...await` loop with `Promise.all(fields.map(validateField))` for concurrent validation (total time ≈ max single validation time, ~200ms), `Promise.allSettled` if some validations should not cancel others on failure, and error filtering from the settled results.""",

"""**Debug Scenario:**
A `useEffect` in a custom hook has a missing dependency that causes a stale callback. The developer added the dep to the array but now ESLint warns about the `useCallback` in the parent:

```tsx
// Custom hook:
function useSearch(onResults: (data: Result[]) => void) {
  useEffect(() => {
    fetchResults().then(onResults);
  }, [onResults]); // onResults added per ESLint warning
}

// Parent component:
<SearchWidget onResults={handleResults} />
// handleResults is a new function reference every render
// → triggers useSearch's effect on every parent render
```

Show: the root cause (non-memoized callback in parent), wrapping `handleResults` with `useCallback` in the parent, and the alternative of storing `onResults` in a `useRef` inside the hook (the ref holds the latest callback, the effect only runs on the relevant deps change, not the callback).""",

"""**Debug Scenario:**
A developer uses `window.open(url, '_blank')` inside an asynchronous event handler. Modern browsers block this as a popup:

```tsx
async function handleExport() {
  const url = await generateExportUrl(); // async operation
  window.open(url, '_blank');            // popup blocked!
}
<button onClick={handleExport}>Export</button>
```

Browsers only allow `window.open` when called synchronously within a user gesture handler. The `await` breaks the synchronous execution chain. Show: opening the window synchronously (before `await`) and then assigning `window.location.href` once the URL is ready, or creating an `<a target="_blank">` element and programmatically clicking it, or navigating within the same window instead of a popup.""",

"""**Debug Scenario:**
A developer tests a React component with `@testing-library/react` using `screen.findByText` but the test times out:

```ts
const heading = await screen.findByText('Welcome back');
// Timeout: Unable to find an element with text 'Welcome back'
```

`findByText` uses exact matching by default. The rendered text is "Welcome back, Alice!" — the full string doesn't match the search text "Welcome back" exactly. Show: using `{ exact: false }` option (`screen.findByText('Welcome back', { exact: false })`), using a regex (`/Welcome back/`), `findByRole('heading', { name: /welcome back/i })` for more semantically meaningful queries, and `getByText` vs `findByText` (async) vs `queryByText` (returns null instead of throwing).""",

"""**Debug Scenario:**
A developer uses `React.createPortal` to render a modal inside `document.body`, but the modal's click events bubble up to a parent component's `onClick` handler:

```tsx
function Page() {
  return (
    <div onClick={() => console.log('Page clicked!')}>
      <Modal />  {/* Rendered via portal into document.body */}
    </div>
  );
}
```

Portal children are OUTSIDE the DOM hierarchy of the parent, but React's synthetic events STILL bubble through the React component tree (not the DOM tree). Clicking inside the modal triggers the `Page`'s `onClick`. Show: calling `e.stopPropagation()` in the modal's root `div`, the distinction between DOM event bubbling and React synthetic event bubbling for portals, and checking `e.target` in the parent's handler to ignore events originating from the modal.""",

"""**Debug Scenario:**
A TypeScript API handler maps a Prisma query result directly to the response, accidentally exposing `passwordHash` and `twoFactorSecret` to the client:

```ts
async function getUserHandler(req, res) {
  const user = await prisma.user.findUnique({ where: { id: req.params.id } });
  res.json(user); // exposes ALL fields including sensitive ones!
}
```

Show: using Prisma's `select` to explicitly list safe fields (`select: { id: true, name: true, email: true }`), a `toPublicUser(user: User): PublicUser` mapping function that picks only safe fields, TypeScript's `Omit<User, 'passwordHash' | 'twoFactorSecret'>` type to enforce exclusion at compile time, and an ESLint custom rule that flags `res.json(prismaResult)` without a field selection.""",

"""**Debug Scenario:**
A component renders a list with duplicate `key` props, causing React to silently skip rendering some items:

```tsx
{products.map((product) => (
  <ProductCard key={product.category} product={product} />
))}
// Multiple products in the same category → duplicate keys
```

React uses keys to identify elements for reconciliation. Duplicate keys cause React to treat them as the same element — some items may not render, or update incorrectly. Show: using a truly unique key (`product.id` or `product.sku`), generating a unique key from multiple fields (`key={${product.category}-${product.id}}`), and why array index as key is problematic only when the list can be reordered or filtered (stable lists where key-as-index is acceptable).""",

"""**Debug Scenario:**
A Next.js API route that accepts multipart form data (file uploads) throws `SyntaxError: Unexpected token` because Next.js tries to parse the body as JSON by default:

```ts
export async function POST(request: Request) {
  const body = await request.json(); // fails for multipart!
}
```

`request.json()` calls `JSON.parse` on the body, which fails for `multipart/form-data` content. Show: using `await request.formData()` for multipart forms in the Next.js App Router, accessing uploaded files with `formData.get('file') as File`, reading file contents with `file.arrayBuffer()`, and setting the Next.js route config `export const config = { api: { bodyParser: false } }` for Pages Router routes that handle multipart data.""",

"""**Debug Scenario:**
A developer uses `useCallback` to memoize a function, but the memoized function still changes reference every render:

```ts
const handleClick = useCallback(() => {
  console.log(count);
}, [count]);

// handleClick reference changes every time count changes → re-renders children
```

The developer expected `useCallback` to return a stable function, but `count` changes frequently. The function MUST change when `count` changes to capture the latest value. Show: the core misunderstanding — `useCallback` memoizes based on deps, which is correct here (the function needs the current `count`). The solution is redesigning so the child only receives stable callbacks, using `useRef` to access current `count` inside a stable callback, and `startTransition` to defer the re-renders triggered by count changes.""",

"""**Debug Scenario:**
A React app uses `Date.now()` for unique IDs in client-side rendered components. After a server-side render (SSR), the IDs differ between server and client causing hydration errors:

```ts
const [uniqueId] = useState(() => `id-${Date.now()}`);
// Server: id-1703234567890 | Client: id-1703234567912 — hydration mismatch!
```

`Date.now()` returns different values on server and client (millisecond difference). Show: using React's `useId()` hook instead (deterministic, SSR-safe), or generating the ID with a seeded counter that resets to the same value on server and client, and the `useEffect` workaround for rare cases: initialize with `null` on server, set the real ID in `useEffect` (client-only).""",

"""**Debug Scenario:**
A floating point precision bug causes a monetary calculation to fail:

```ts
const price = 1.1;
const tax   = 0.1;
const total = price + tax;
console.log(total);          // 1.2000000000000002
console.log(total === 1.2);  // false!
```

JavaScript uses IEEE 754 double-precision floating point — binary fractions can't represent all decimals exactly. Show: multiplying to integers before arithmetic (`Math.round((price + tax) * 100) / 100`), using `Number.EPSILON` for comparison (`Math.abs(total - 1.2) < Number.EPSILON`), using the `Decimal.js` or `big.js` library for arbitrary precision, and why monetary values should be stored as integers (cents) in both the database and application.""",

"""**Debug Scenario:**
A Zustand store action uses `get()` to read state, but reads stale values when multiple actions are dispatched in rapid succession:

```ts
const addItem = () => set(state => ({
  items: [...state.items, newItem],
  total: get().items.reduce((sum, i) => sum + i.price, 0), // reads stale state
}));
```

Inside `set(fn)`, using `get()` reads the CURRENT stored state (before this update is applied), not the updated state from `fn`. Show: computing `total` from the updated `items` inside the `set` callback:

```ts
set(state => {
  const items = [...state.items, newItem];
  return { items, total: items.reduce((sum, i) => sum + i.price, 0) };
});
```

And using `immer` middleware to avoid returning a new object (mutate the draft directly).""",

"""**Debug Scenario:**
A developer adds `async` to a function used as a React event handler, and now errors are not caught by the component's error boundary:

```tsx
<form onSubmit={async (e) => {
  e.preventDefault();
  await submitForm(data); // throws, but error boundary doesn't catch it
}}>
```

Error boundaries only catch errors thrown during React's rendering phase — not inside event handlers, and not inside async functions. Show: wrapping the async handler in `try/catch` with `setState({ error })`, using a `useErrorHandler()` hook from `react-error-boundary` that internally calls `setState` to trigger the boundary, and the correct mix of boundary + handler-level error handling.""",

"""**Debug Scenario:**
A CSS transition on a React component doesn't play when the component first mounts — only on subsequent state changes:

```tsx
function Alert({ type }) {
  return (
    <div
      className={`alert alert-${type}`}  // type changes: 'info' → 'error'
      style={{ transition: 'background 0.3s' }}
    >
      Notification
    </div>
  );
}
```

CSS transitions work when a property CHANGES between two states. On mount, there's no "previous" state to transition from — the browser applies the initial value instantly. Show: adding a brief `setTimeout(addActiveClass, 10)` after mount to trigger the transition, using CSS `animation` instead of `transition` for enter animations, the Framer Motion `<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>` approach, and the React ecosystem `react-transition-group` `<CSSTransition>` component.""",

"""**Debug Scenario:**
A developer receives a `CORS` error when making a fetch request from `localhost:3000` to `localhost:4000`:

```
Access to fetch at 'http://localhost:4000/api/data' from origin 'http://localhost:3000' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

Even `localhost` to `localhost` on different ports is cross-origin. Show: adding `cors` middleware on the Express server (port 4000) with `origin: 'http://localhost:3000'`, why `mode: 'no-cors'` in fetch is NOT the fix (it makes the response opaque — unreadable), the Vite dev server `proxy` config for avoiding CORS in development, and handling the `OPTIONS` preflight request (CORS preflight for non-simple requests).""",

"""**Debug Scenario:**
A React `useReducer` action mutates the state object and the component doesn't re-render:

```ts
function reducer(state, action) {
  switch(action.type) {
    case 'ADD_ITEM':
      state.items.push(action.item); // mutates state!
      return state;  // returns same reference
  }
}
```

React compares state by reference. Returning the same (mutated) object reference means React sees no state change and skips re-render. Show: the immutable update (`return { ...state, items: [...state.items, action.item] }`), using Immer (`produce(state, draft => { draft.items.push(action.item) })`) for ergonomic immutable updates, and why Redux Toolkit uses `createSlice` with Immer to prevent this mistake.""",

"""**Debug Scenario:**
A developer uses `Array.sort()` to sort a list of products by price, but the sort order is incorrect for 3-digit prices:

```ts
const prices = [10, 100, 2, 30, 200];
prices.sort(); // [10, 100, 2, 200, 30] — wrong! (lexicographic)
```

Without a comparator, `Array.sort()` converts elements to strings and sorts lexicographically: `'10' < '100' < '2'`. Show: passing a numeric comparator `(a, b) => a - b`, the `Intl.Collator` for locale-aware string sorting, and chained sort for multiple criteria `(a, b) => a.price - b.price || a.name.localeCompare(b.name)`.""",

"""**Debug Scenario:**
A React app stores the current user in localStorage and uses `JSON.parse(localStorage.getItem('user'))` in the initial state. On first load (no stored user), `JSON.parse(null)` returns `null` — but subsequent code expects a `User` object, causing TypeScript-ignored runtime errors:

```ts
const [user, setUser] = useState<User>(JSON.parse(localStorage.getItem('user')!));
// On first load: user is null but type says User — TypeScript non-null assertion bypasses safety
```

Show: proper null handling (`JSON.parse(localStorage.getItem('user') ?? 'null') as User | null`), initializing with `null` as the legitimate state type (`useState<User | null>(null)`), a `useLocalStorage<T>(key, defaultValue)` hook that handles JSON parsing and null defaults, and Zod schema validation of the stored user object (in case it was corrupted or from an old schema version).""",

"""**Debug Scenario:**
A developer dispatches multiple Redux actions in succession inside a `useEffect`, causing multiple re-renders:

```ts
useEffect(() => {
  dispatch(setLoading(true));
  dispatch(setUser(null));
  dispatch(clearCart());
  dispatch(setLoading(false));
  // 4 separate store updates → 4 re-renders
}, []);
```

Show: using Redux Toolkit's `createAction` actions inside a single `dispatch` with a combined action (`dispatch(resetSession())` where `resetSession` handles setting loading, user, cart, etc. in one reducer call), React 18's automatic batching (all dispatches in a `useEffect` ARE already batched in React 18 with `createRoot` — so this may not actually be 4 re-renders), and `redux-batch` middleware for older Redux setups.""",

"""**Debug Scenario:**
A streaming API endpoint sends server-sent events (SSE) but the browser closes the connection after 30 seconds. Users report the live feed "dying" after exactly 30 seconds regardless of activity:

```ts
// Server:
res.write(`data: ${JSON.stringify(event)}\n\n`);
// Browser: EventSource disconnects at exactly 30s
```

The disconnect isn't from the browser — it's likely a load balancer, reverse proxy (nginx/Cloudflare), or CDN with a hardcoded 30-second timeout for idle connections. Show: configuring nginx `proxy_read_timeout` to a longer value, sending a SSE heartbeat comment (`": keepalive\n\n"`) every 15 seconds to prevent idle timeout, and adding `EventSource` reconnect logic with exponential backoff (`source.onerror = () => setTimeout(reconnect, delay)`).""",

"""**Debug Scenario:**
A React component tree throws an unrecoverable error every time it tries to render a video player. The error boundary catches it, but when the user clicks "Try Again" (which calls `reset()`), the component re-crashes immediately:

```tsx
function VideoPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  useEffect(() => {
    videoRef.current!.src = getVideoUrl(); // getVideoUrl() throws
  }, []);
  return <video ref={videoRef} />;
}
```

`getVideoUrl()` always throws (bad config). Clicking Reset re-mounts `VideoPage` which triggers the same `useEffect` which throws again. Show: the error boundary `reset()` + props key trick (`key={retryKey}` that increments to force a fresh mount), fixing the root cause (null checking `getVideoUrl()`), and the `react-error-boundary` `fallbackRender` pattern with props passed to the fallback for context.""",

"""**Debug Scenario:**
A developer uses `element.addEventListener('click', handler, { once: true })` expecting the handler to fire once and auto-remove. But in React, the component re-renders and re-runs the `useEffect` that adds the listener again:

```ts
useEffect(() => {
  element.addEventListener('click', handleClick, { once: true });
  // No cleanup! After handleClick fires, React re-renders → useEffect re-runs → listener added again
}, [someState]);
```

`{ once: true }` removes the listener after ONE fire, but the `useEffect` runs again (due to `someState` dep change) and re-adds it — creating a new listener. Show: adding a `return () => element.removeEventListener('click', handleClick)` cleanup (even with `{ once }`, cleanup handles the case where the component unmounts before the click), and whether `{ once: true }` is even needed (the cleanup handles removal).""",

"""**Debug Scenario:**
A developer implements infinite scroll using `IntersectionObserver` but the observer fires immediately on mount — before the user scrolls — causing a premature data fetch:

```ts
useEffect(() => {
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) loadMore(); // fires immediately!
  });
  observer.observe(sentinelRef.current);
}, []);
```

`IntersectionObserver` fires its callback synchronously on the first observation, checking if the element is already in the viewport. The sentinel element IS in the viewport on initial mount when the list is short. Show: skipping the first callback invocation with a `hasInitialized` ref, setting `rootMargin: '200px'` to load earlier (before reaching the sentinel), and threshold configuration to control precisely when `isIntersecting` becomes `true`.""",

"""**Debug Scenario:**
A developer mistakenly uses `JSON.stringify` to deep-compare two objects in a performance-critical render path:

```ts
function hasChanged(prev: Config, next: Config): boolean {
  return JSON.stringify(prev) !== JSON.stringify(next); // slow for large objects
}
```

`JSON.stringify` serializes the entire object on every call — O(n) in object size. For a 5MB config object, this is called on every render. Show: structural comparison using a fast `shallowEqual` for the top level (if shallow equals, skip), only deep-comparing on shallow difference, using `fast-deep-equal` npm package for reliable deep comparison without serialization overhead, and the specific case where JSON.stringify IS OK (small, guaranteed JSON-safe objects).""",

"""**Debug Scenario:**
A developer uses `Array.prototype.reduce` to transform an array but gets `undefined` as the result when the array is empty:

```ts
const items: number[] = [];
const total = items.reduce((acc, n) => acc + n);
// TypeError: Reduce of empty array with no initial value
```

`Array.reduce` without an initial value throws on empty arrays. With an initial value, it works correctly even on empty arrays. Show: always providing an explicit initial value (`items.reduce((acc, n) => acc + n, 0)`), the TypeScript type signature difference (`reduce<U>(..., initialValue: U): U` vs `reduce(...): T`), and common reduce gotchas: object accumulator mutation vs returning a new object, and accumulator type mismatch.""",

]

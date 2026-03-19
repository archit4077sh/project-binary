"""
snippets/q_debugging.py — BATCH 4: 28 brand-new Debugging questions
Zero overlap with batch1, batch2, or batch3 archives.
"""

Q_DEBUGGING = [

"""**Debug Scenario:**
A Next.js middleware adds `x-user-id` to request headers to pass the authenticated user ID to Server Components. But inside a Server Component, `headers().get('x-user-id')` returns `null`.

Investigation shows the middleware sets the header on the `request`, but doesn't forward it using `NextResponse.next({ request: { headers: newHeaders } })` — instead it just calls `NextResponse.next()` without propagating the header mutation.

Show: the correct middleware pattern for forwarding custom request headers to Server Components using `NextResponse.next({ request: { headers: requestHeaders } })`, why header mutations on the original request object don't propagate without this pattern, and reading the header safely in a Server Component.""",

"""**Debug Scenario:**
A developer adds `React.StrictMode` to their application and suddenly their form's `<input>` loses focus on every keystroke. The form was working before `StrictMode`:

```tsx
function Form() {
  const [fields, setFields] = useState({ name: '' });
  const Input = () => <input value={fields.name} onChange={e => setFields({ name: e.target.value })} />;
  return <form><Input /></form>;
}
```

The `Input` component is defined INSIDE `Form`. `StrictMode` double-invokes renders, and every render creates a NEW `Input` function reference — React sees it as a new component type and unmounts/remounts it (losing focus).

Show: moving `Input` outside the `Form` function (at module scope), why component definitions inside components are an anti-pattern (new type reference = unmount/remount on render), and `useRef` on the input as a temporary workaround.""",

"""**Debug Scenario:**
A multi-step form uses `localStorage` to persist progress. In Safari private mode, `localStorage.setItem()` throws a `QuotaExceededError` but the form crashes instead of gracefully degrading.

```ts
localStorage.setItem('form-progress', JSON.stringify(data)); // throws in Safari private
```

Safari's private mode sets `localStorage` quota to 0 bytes. The `try/catch` is missing. Show: wrapping all `localStorage` calls in a `try/catch`, creating a `safeLocalStorage` wrapper with silent failure on `QuotaExceededError`, falling back to in-memory storage when localStorage is unavailable, and a `isLocalStorageAvailable()` check using a test write/read/delete.""",

"""**Debug Scenario:**
A REST API uses `Long` (64-bit integers) for IDs. In JavaScript, integers above `Number.MAX_SAFE_INTEGER` (2^53-1) lose precision. User IDs over 9 trillion are silently corrupted:

```ts
const response = await fetch('/api/user/9007199254740993');
const user = await response.json();
console.log(user.id); // 9007199254740992 — precision lost!
```

`JSON.parse` converts JSON numbers to JavaScript `number` type which is a 64-bit float. Show: the server-side fix (serialize large IDs as strings in JSON), client-side: using a JSON parser that handles BigInt (`json-bigint` library), and the API contract decision — string IDs from inception to avoid this class of bug entirely.""",

"""**Debug Scenario:**
A `<Select>` component from a component library shows the placeholder text ("Select an option") even after the user selects a value. The component's `value` prop is correctly set to `'option1'`.

```tsx
<Select value={selectedOption} onChange={setSelectedOption} options={options} />
// Shows placeholder even when selectedOption = 'option1'
```

Investigation reveals `options` is defined as inline object literals:

```ts
const options = [{ value: 'option1', label: 'One' }]; // new array every render
```

The `<Select>` uses referential equality to find the selected option (`options.find(o => o === value)` instead of `o.value === value`). It compares object identity, not value. Show: the correct comparison by `option.value`, the fix using a stable `options` reference with `useMemo`, and why inline object arrays in JSX are a maintenance footgun.""",

"""**Debug Scenario:**
A production error log shows frequent `TypeError: Cannot read properties of undefined (reading 'map')` errors from a specific React component. The component fetches data and renders a list:

```tsx
function ProductList({ categoryId }) {
  const { data } = useQuery(['products', categoryId], () => fetchProducts(categoryId));
  return <ul>{data.products.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

The error happens in the render phase before data is fetched (`data` is `undefined` initially). Show: optional chaining `data?.products?.map(...)`, default value `{ data: { products: [] } }`, the `isLoading` guard, and TypeScript preventing this at compile time by typing `data` as `ProductsResponse | undefined` (which requires null checking before access).""",

"""**Debug Scenario:**
A React app renders a `<Map>` component (Mapbox). When the map container is resized (responsive layout), the map tiles don't fill the new dimensions — there's a gray area at the edges.

Mapbox initializes with the container's dimensions and doesn't automatically detect resize. The fix is to call `map.resize()` after the container dimensions change.

Show: using `ResizeObserver` to watch the map container element and call `map.resize()` on every dimension change, the `useEffect` cleanup to disconnect the observer, and why `window.addEventListener('resize', ...)` is insufficient (catches window resize but not container resize from layout changes like sidebar collapse).""",

"""**Debug Scenario:**
A developer uses `useEffect` to synchronize a controlled `<textarea>` scroll position with a preview panel. The scroll sync works but causes an infinite loop:

```ts
useEffect(() => {
  previewRef.current.scrollTop = textareaRef.current.scrollTop; // syncs scroll
}, [scrollTop]); // scrollTop from useState, updated by textarea onScroll
```

Setting `previewRef.current.scrollTop` triggers the preview's scroll event, which updates `previewScrollTop` state, which re-triggers the `useEffect`... but wait, the effect uses `textareaRef.current.scrollTop` (the source). Show: why this specific pattern doesn't create an infinite loop (the effect reads from textarea, writes to preview — not the source of the state that triggered it), and demonstrate an actual scroll sync infinite loop and its fix with `isUserScrolling` ref flag.""",

"""**Debug Scenario:**
A GraphQL subscription in a React component leaks memory. The subscription isn't cancelled when the component unmounts because the cleanup function isn't returned from `useEffect`:

```ts
useEffect(() => {
  const sub = apolloClient.subscribe({ query: PRICE_SUBSCRIPTION }).subscribe({
    next: (data) => setPrices(data.prices),
  });
  // Bug: should return () => sub.unsubscribe();
}, []);
```

Show: the correct cleanup return, how to verify the leak using Chrome DevTools Memory profiler (take heap snapshot before and after repeated mount/unmount, compare `Subscription` objects), and why React `StrictMode`'s double-invoke exposes this class of leak in development.""",

"""**Debug Scenario:**
A `useForm` hook from `react-hook-form` shows validation errors for a field that the user hasn't touched yet, on initial page load. The form shows error messages before the user has interacted:

```ts
const { formState: { errors } } = useForm({
  resolver: zodResolver(schema),
  mode: 'onSubmit', // ← should only validate on submit
});
```

The issue isn't `mode` — a parent component is calling `trigger()` on mount to validate the entire form immediately (for some pre-population logic). Show: the `shouldFocusError: false` option, replacing `trigger()` on mount with `setValue` for pre-population (which doesn't trigger validation unless `shouldValidate: true` is passed), and the `touchedFields` state to conditionally show errors only for interacted fields.""",

"""**Debug Scenario:**
A React app has a custom `useFetch` hook that caches responses in a module-level `Map`. During Vitest testing, cache entries from one test pollute subsequent tests:

```ts
// Outside component — module-level:
const cache = new Map<string, unknown>();

export function useFetch<T>(url: string): { data: T | null; loading: boolean } {
  if (cache.has(url)) return { data: cache.get(url) as T, loading: false };
  // ...
}
```

Module-level variables persist across test runs in the same Jest/Vitest worker. Show: clearing the cache in `afterEach` by exporting a `clearCache()` function, moving the cache inside a React Context (scoped to the app tree, reset by remounting the Provider in each test), and why module-level singletons are generally test-hostile.""",

"""**Debug Scenario:**
A `<NumberInput>` component allows the user to type decimal numbers. When the user types `1.` (with a trailing dot), the input immediately changes to `1` (the dot is lost), preventing them from typing `1.5`:

```ts
const [value, setValue] = useState<number>(0);
<input value={value} onChange={e => setValue(Number(e.target.value))} />
// '1.' → Number('1.') = 1 → loses the dot
```

Converting to `number` immediately drops formatting needed for mid-input states. Show: storing the value as a string internally and parsing to number only in `onBlur`, the `NaN` guard (empty or invalid input shows 0 or nothing), and a `useNumberInput` hook that exports both `displayValue: string` (for the input) and `numericValue: number | null` (for form logic).""",

"""**Debug Scenario:**
A Next.js app's `robots.txt` file blocks all crawlers on the production site. The file exists at `public/robots.txt`:

```
User-agent: *
Disallow: /
```

This was intended for the staging environment but was shipped to production. The SEO team discovers 4 days later that Google has de-indexed the site.

Show: the proper environment-aware `robots.txt` generation using Next.js `app/robots.ts` (returns `MetadataRoute.Robots`), where the Disallow path is conditionally `['/']` on staging and `[]` (allow all) on production based on `process.env.VERCEL_ENV === 'production'`, and monitoring with Google Search Console alerts for sudden drop in indexed pages.""",

"""**Debug Scenario:**
A developer uses `Array.from({ length: size }, (_, i) => i)` to generate page number arrays in a `<Pagination>` component. React DevTools shows this component re-renders on every parent state change:

```tsx
function Pagination({ currentPage, totalPages, onPageChange }) {
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1); // new array every render
  return pages.map(p => <button onClick={() => onPageChange(p)}>{p}</button>);
}
```

`Array.from` always creates a new array reference — but `Pagination` is wrapped in `React.memo`. `React.memo` compares `props` shallowly — `pages` is not a prop here. The real issue is `onPageChange` is an inline arrow function in the parent (new reference each render).

Show: `useCallback` on `onPageChange` in the parent, and `useMemo` on `pages` if `totalPages` changes rarely.""",

"""**Debug Scenario:**
A multi-language React app uses `i18next` for translations. After switching the language from English to French, some strings update but others remain in English — specifically strings inside `React.memo`'d components.

```ts
// Memoized component:
const PremiumBadge = React.memo(({ plan }) => {
  const { t } = useTranslation(); // uses i18next context
  return <span>{t('badge.premium')}</span>;
});
```

`React.memo` compares props, and `plan` hasn't changed, so `PremiumBadge` doesn't re-render. But `t()` is a function that reads from the i18next context — the memo prevents it from seeing the language change.

Show: passing `language` as a prop to `PremiumBadge` (so memo re-renders when language changes), the `i18next.on('languageChanged')` listener approach, and why `React.memo` and context consumers require careful design.""",

"""**Debug Scenario:**
A `<DataTable>` component with sorting causes rapid flickering when the user clicks a sort column header. Investigation shows:

```ts
const sortedData = data.sort((a, b) => a[sortCol] > b[sortCol] ? 1 : -1); // mutates data!
```

`Array.prototype.sort` mutates the array in place. Every re-render re-sorts the same array (which is already sorted), but React also re-renders because the array reference from state changes (the state is set to the same mutated array — same reference, no re-render... so why flicker?).

Show: actually the issue is the component passes `data` to a child that animates additions/removals — mutating the array changes existing items' positions, confusing the animation. Show using `[...data].sort(...)` for an immutable sort and why array mutation is always dangerous in React's data flow.""",

"""**Debug Scenario:**
A Playwright test for a file download fails on CI:

```ts
const [download] = await Promise.all([
  page.waitForEvent('download'),
  page.click('button[data-testid="export"]'),
]);
expect(download.suggestedFilename()).toBe('report.csv');
```

The test passes locally but fails in CI with "No events of type 'download' were received before timeout." The CI environment uses Chromium in headless mode. In headless Chromium, some download behaviors require explicit handling.

Show: configuring Playwright to use `acceptDownloads: true` in the browser context, the `headless: true` explicit config, setting a `downloadPath` in the browser context for CI, and checking if the website uses `Content-Disposition: attachment` header (required for download events in headless mode).""",

"""**Debug Scenario:**
A developer uses `Promise.race` to implement an API call timeout, but the losing promise (the actual fetch) continues running in the background after the timeout wins:

```ts
const result = await Promise.race([
  fetch('/api/slow-endpoint'),
  new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 5000)),
]);
```

`Promise.race` resolves/rejects with the winner, but all other promises continue executing. The slow fetch still completes 30 seconds later, consuming server resources.

Show: using `AbortController` to cancel the fetch when the timeout occurs:
```ts
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);
const result = await fetch('/api/slow-endpoint', { signal: controller.signal });
clearTimeout(timeoutId);
```""",

"""**Debug Scenario:**
A React component that fetches paginated data with `useSWRInfinite` shows duplicate items when new items are inserted into the database between page loads:

```ts
const { data, size, setSize } = useSWRInfinite(
  (index) => `/api/items?page=${index + 1}`,
  fetcher
);
```

When page 1 is loaded with items 1-10, then a new item is inserted at position 1, loading page 2 returns items 11-20 but item 11 was item 10 before the insertion — so item 10 appears on both pages.

Show: switching to cursor-based pagination (`/api/items?after=lastId`), the SWR key function using `data?.[data.length - 1]?.cursor`, and de-duplicating items client-side using a `Map` by ID as a safety net.""",

"""**Debug Scenario:**
A React component uses `addEventListener` in a `useEffect` to detect clicks outside a dropdown. After the component re-renders, there are two event listeners attached (one from the initial mount, one from the re-render):

```ts
useEffect(() => {
  document.addEventListener('click', handleClose);
  // Missing return cleanup!
}, [isOpen]); // Re-attaches every time isOpen changes
```

Each time `isOpen` changes, a new listener is added without removing the previous one. Show: the correct cleanup function (`return () => document.removeEventListener('click', handleClose)`), running the `linter` rule `react-hooks/exhaustive-deps` which catches this, and the alternative using an `AbortController` signal for event listener cleanup.""",

"""**Debug Scenario:**
A Next.js app's API route returns a large JSON response (8MB). Users on mobile experience 30+ second load times for a dashboard page that calls this endpoint.

Investigation reveals the endpoint fetches 50,000 rows from the database and returns all of them. The dashboard only renders the first 20 visible rows.

Show: adding server-side pagination (`LIMIT 20 OFFSET $page * 20`), cursor-based pagination for infinite scroll, response compression (`Content-Encoding: gzip` — Next.js Route Handlers compress by default but confirm), and client-side data virtualization so that even when all data IS loaded, only visible rows are in the DOM.""",

"""**Debug Scenario:**
A `<Toast>` notification system renders toasts via a React context. When multiple toasts appear simultaneously (5+ in under a second), some disappear instantly while others stay visible for the wrong duration.

```ts
const [toasts, setToasts] = useState<Toast[]>([]);
const addToast = (msg, duration = 3000) => {
  setToasts(prev => [...prev, { id: Date.now(), msg, duration }]);
  setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), duration); // closure bug
};
```

`id` in the `setTimeout` closure is captured from the outer function but `Date.now()` is called at different times — however the real bug is `id` isn't defined in scope at the time `setTimeout` is set. Show: the closure fix using the toast ID consistently, and `useRef` to maintain a stable ID counter instead of `Date.now()` (to avoid collisions when multiple toasts are added in the same millisecond).""",

"""**Debug Scenario:**
A developer reports that Redux `dispatch` inside a `useEffect` causes a state update loop:

```ts
useEffect(() => {
  if (data && !initialized) {
    dispatch(initializeState(data));
  }
}, [data, initialized, dispatch]);
```

`dispatch` is stable (never changes in Redux — same reference throughout app lifetime). `data` might change. `initialized` changes after dispatch fires (from `false` to `true`). The loop happens if `initialized` doesn't actually flip to `true` — perhaps the `initialized` reducer has a bug.

Show: adding a `console.log` inside the effect to count invocations, using Redux DevTools time-travel to inspect `initialized` value after each dispatch, and the reducer bug (missing `return { ...state, initialized: true }`).""",

"""**Debug Scenario:**
A CSS-in-JS library (`@emotion/react`) generates a class name collision in production between two unrelated components. Both end up with class `css-abc123`.

Class names in Emotion are hashes of the CSS content. If two completely different components have identical CSS content (e.g., both are `color: red; font-size: 14px;`), they get the same hash and share the class — this is INTENTIONAL deduplication, not a bug.

Show why this is generally fine (same styles = same class = smaller DOM), the case where it causes problems (component-specific selectors like `.parent .css-abc123:first-child` that rely on class uniqueness), and using `label` in Emotion's `css` prop (`css({ label: 'my-button', color: 'red' })`) to add a component-specific prefix to the generated class name.""",

"""**Debug Scenario:**
A TypeScript error appears only in `tsc --strict` mode but not in regular `tsc`:

```ts
function getUser(id: string) {
  return users.find(u => u.id === id); // type: User | undefined (strict)
  //                                             ^^^^^^^^^^ without strict: User
}

getUser('1').name; // Error in strict, OK without strict
```

Without `strictNullChecks`, TypeScript doesn't track `undefined` in union types — `find` returns `User` instead of `User | undefined`. Show: enabling `strict: true` in `tsconfig.json` (enables `strictNullChecks` + 7 other checks), fixing the callers with optional chaining `getUser('1')?.name`, and why migrating incrementally from non-strict to strict uses `// @ts-strict-ignore` comments (with a plan to remove them).""",

"""**Debug Scenario:**
A developer implements `useCountdown(targetDate)` by storing `remainingSeconds` in `useState` and decrementing it with `setInterval`. The countdown drifts — after 1 hour, it's 3–5 seconds behind.

```ts
useEffect(() => {
  const id = setInterval(() => {
    setRemaining(prev => prev - 1);
  }, 1000);
  return () => clearInterval(id);
}, []);
```

`setInterval` fires at approximately 1000ms but can drift due to browser throttling, tab inactivity, and JavaScript event loop delays. Over time, small delays accumulate.

Show: fixing the drift by computing `remaining` from `targetDate - Date.now()` on each tick (absolute time reference, not relative decrement), why this is immune to drift, and `requestAnimationFrame` as an alternative for smoother visual countdown displays.""",

"""**Debug Scenario:**
A React apps uses `createContext` for a feature flags context. A `<FeatureFlagsProvider>` is at the root. When Cypress E2E tests run, feature flags show their defaults instead of test-specific values.

```tsx
// Test wants new-checkout=true, but sees false
cy.visit('/checkout');
```

Cypress tests hit the real app which reads flags from the server. No mechanism exists to override flags in tests. Show: adding a `?flags=new-checkout:true` URL parameter that the `<FeatureFlagsProvider>` reads (for testing only, stripped in production), an MSW handler that returns specific flag values based on a `cy.intercept`, and the `window.__TEST_FLAGS__` injection approach via `cy.window()` for non-API flag overrides.""",

"""**Debug Scenario:**
A production React app shows the error "Maximum update depth exceeded" triggered by a `useEffect` that depends on an object prop:

```ts
useEffect(() => {
  applyConfig(config);
}, [config]); // config is { theme: 'dark', lang: 'en' } — new object each render
```

The parent renders a new `config` object literal each time. `useEffect` compares dependencies with `Object.is` — a new object reference each render causes the effect to re-run infinitely.

Show: the developer options — (1) destructure the individual primitive values as dependencies (`[config.theme, config.lang]`), (2) stabilize the object in the parent with `useMemo`, (3) use the `useDeepCompareEffect` custom hook for complex object deps (only runs when deep equality changes), and why option 3 has hidden costs (deep comparison on every render).""",

]

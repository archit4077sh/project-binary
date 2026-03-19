"""
snippets/q_debugging.py — BATCH 3: 28 brand-new Debugging questions
Zero overlap with batch1 or batch2 archives.
"""

Q_DEBUGGING = [

"""**Debug Scenario:**
A production Next.js app logs `Warning: Maximum update depth exceeded` in Sentry for ~2% of sessions. The warning stack trace points to a `useEffect` inside `<UserSettings>`.

```ts
useEffect(() => {
  setPreferences(prev => ({ ...prev, ...userPrefs }));
}, [userPrefs]);
```

`userPrefs` comes from a selector: `const userPrefs = useSelector(s => ({ theme: s.theme, lang: s.lang }))`. Redux's `useSelector` returns a new object reference on every call even when values are equal. Diagnose the infinite loop and show the fix using `shallowEqual` as the selector equality function.""",

"""**Debug Scenario:**
A React Native app (Expo) crashes on Android when navigating to a `<WebView>` screen with a large `injectedJavaScript` string. The crash log shows:

```
TransactionTooLargeException: data parcel size X bytes
```

Android's `Binder` IPC has a 1MB transaction limit. The injected JavaScript string is 800KB (includes a bundled library). Show how to: serve the JS as a local file using Expo's `Asset` API, use `source={{ uri }}` to load from the bundle, and implement code splitting in the injected script.""",

"""**Debug Scenario:**
A unit test for a date formatting utility passes in CI (Linux) but fails for one developer on Windows:

```ts
test('formats date correctly', () => {
  expect(formatDate(new Date('2024-01-15'))).toBe('Jan 15, 2024');
  // Fails on Windows: 'January 15, 2024'
});
```

`formatDate` uses `toLocaleDateString()`. Diagnose the OS locale difference (Windows `en-US` uses full month names by default while Linux uses abbreviated), and show two fixes: use `Intl.DateTimeFormat` with explicit `month: 'short'` option, or mock `Date.prototype.toLocaleDateString` in tests to ensure consistent output.""",

"""**Debug Scenario:**
A React component that fetches and displays stock prices re-renders 60 times per second because the WebSocket sends 60 messages/second. Even though `React.memo` is used, the component still re-renders on every message.

```ts
const price = useSelector(s => s.stocks[symbol]);
// price changes on every message (new number value)
```

The value genuinely changes (stock prices fluctuate), but re-rendering 60fps is wasteful when the human eye can't distinguish updates faster than ~15fps. Show: throttling the Redux store updates to 15fps using a middleware, `useDeferredValue` to skip renders during heavy updates, and `react-spring` for smooth visual interpolation between values.""",

"""**Debug Scenario:**
A styled-components `ThemeProvider` in a Storybook story doesn't apply the theme — components render with default styles instead of themed ones. The same code works in the actual app.

```ts
// Storybook decorator:
const withTheme = (Story) => (
  <ThemeProvider theme={theme}><Story /></ThemeProvider>
);
```

Investigation reveals Storybook uses a different version of `styled-components` than the app (Storybook's peer dep: v5, app: v6). The `ThemeProvider` from Storybook's bundle and the `ThemeProvider` the components use are different instances, so context doesn't propagate.

Show the fix: aliasing styled-components in Webpack config so only one instance is used, and verifying with `styled-components.version`.""",

"""**Debug Scenario:**
A `<Popover>` component registers a `click` event listener on `document` to close itself when the user clicks outside. In React Testing Library tests, clicking outside doesn't close the popover.

```ts
useEffect(() => {
  document.addEventListener('click', handleClickOutside);
  return () => document.removeEventListener('click', handleClickOutside);
}, []);
```

RTL's `fireEvent.click` triggers synthetic events that don't bubble to `document` by default. `userEvent.click` does bubble, but RTL's `render` wraps the component in a `#root` div. Show: why the event doesn't reach `document` in some setups, using `userEvent.click(document.body)` vs `fireEvent.click(document)`, and the pointer-events-based alternative using `userEvent.pointer`.""",

"""**Debug Scenario:**
An Electron app built with React shows white flicker when switching between the main window and child windows. The flicker lasts ~100ms and is caused by the browser-view background being white during render.

Setting `backgroundColor: '#1a1a1a'` on `BrowserWindow` creates the window with the correct background before React renders. But the React CSS sets `background-color: var(--bg-color)` from a CSS variable and there's a brief period where the variable isn't loaded.

Show how to inline the critical background CSS in the `<head>` before the stylesheet loads, using the same technique as FOUC prevention — a synchronous `<style>` tag that reads the user's theme preference from `localStorage`.""",

"""**Debug Scenario:**
A production React app shows users an error screen with `Invariant Violation: ReactDOM.render is no longer supported in React 18`. The error appears only in Cypress E2E tests, not in the actual app.

Investigation reveals Cypress's `cy.mount()` uses the old React 17 `ReactDOM.render` API internally. The app upgraded to React 18's `createRoot`, but the Cypress component testing setup wasn't updated.

Show: updating `cypress/support/component.ts` to use `createRoot`, the correct mount command for React 18, and any migration steps for existing test fixtures.""",

"""**Debug Scenario:**
A paginated API endpoint returns duplicate items when new items are inserted between page requests. User sees item #50 on page 1 and again on page 2 because a new item shifted the offset.

```
Page 1: OFFSET 0 LIMIT 10 → items 1-10
// New item inserted at position 5
Page 2: OFFSET 10 LIMIT 10 → items 11-20 (but item 11 was item 10 before insertion)
→ item 10 appears on both pages
```

Show the fix using cursor-based pagination (stable `id`-based cursor instead of numeric offset), the API contract change, and how `useInfiniteQuery` needs to be updated to use the cursor from the response instead of a computed page number.""",

"""**Debug Scenario:**
A form with `autocomplete="new-password"` still triggers browser autofill on Chrome. Browsers aggressively autofill password fields even when `autocomplete` is set to prevent it.

Investigate the Chrome-specific behavior where `autocomplete="new-password"` was honored in Chrome 86 but broken in Chrome 100+. Show workarounds: dynamically injecting the `autocomplete` attribute after mount, using a visible-but-off-screen fake credential field to trick the browser, and the `input.setAttribute('autocomplete', 'new-password')` direct DOM manipulation approach that bypasses React's synthetic attribute handling.""",

"""**Debug Scenario:**
A React app's `key` prop is set on list items using array index. After the user deletes an item at index 2, the animation library (`framer-motion`) plays the wrong animation — the item at index 2 disappears instead of the deleted item animating out.

```tsx
items.map((item, i) => (
  <motion.div key={i} exit={{ opacity: 0 }}>  {/* Bug: keyed by index */}
```

Show: why index keys cause React to reuse DOM elements for the wrong items after deletion (React matches by position, not identity), the fix using stable IDs as keys, and how Framer Motion uses keys to track which element is which for exit animations.""",

"""**Debug Scenario:**
A developer adds a `console.log(process.env)` to a Server Component during debugging and accidentally ships it to production. The log dumps all environment variables (including `DATABASE_URL`, `JWT_SECRET`) to Vercel's function logs, which are accessible to any team member.

Show how `console.log(process.env)` in a Server Component leaks all env vars (including private ones), the correct way to expose only `NEXT_PUBLIC_*` vars to the client, and a pre-commit hook or ESLint rule that prevents `process.env` from being logged directly.""",

"""**Debug Scenario:**
A Next.js app shows different content for logged-in vs logged-out users. The CDN (Cloudflare) is caching the logged-in version and serving it to logged-out users.

```ts
// Route Handler sets:
Cache-Control: s-maxage=3600, stale-while-revalidate=60
// But doesn't vary by auth state
```

Show the fix: `Vary: Cookie` or `Cache-Control: private` for authenticated responses, `Cache-Control: public, s-maxage=3600` only for public responses, and the Cloudflare Cache Rule that bypasses the cache for requests with a `session` cookie.""",

"""**Debug Scenario:**
A complex `useEffect` hook has 8 dependencies. Every time one changes, the full effect runs (including an expensive API call). The developer wants the effect to only call the API when `userId` changes but still have access to the latest values of the other 7 dependencies.

```ts
useEffect(() => {
  const data = computeWith(dep1, dep2, dep3, dep4, dep5, dep6, dep7);
  api.call(userId, data); // Only should re-run when userId changes
}, [userId, dep1, dep2, dep3, dep4, dep5, dep6, dep7]); // runs on any change
```

Show: the `useRef` pattern for "latest value refs," the split-effect pattern (one effect for `userId` changes that reads from refs), and when this pattern is safe vs when it creates bugs.""",

"""**Debug Scenario:**
A team migrates from `axios` to native `fetch` and discovers their request interceptors (used for adding auth headers and retrying on 401) no longer work.

The `axios` interceptors pattern:
```ts
axios.interceptors.request.use(addAuthHeader);
axios.interceptors.response.use(null, retryOn401);
```

Show how to implement the equivalent with native `fetch`: a custom `apiFetch` wrapper, a `withAuth` higher-order function, and an automatic 401 retry with token refresh using the refresh token from an HttpOnly cookie. Handle the case where multiple simultaneous requests fail with 401 (only refresh once, queue others).""",

"""**Debug Scenario:**
A `useMutation` from React Query v5 doesn't show an error toast when the server returns a 422 status. The mutation's `onError` callback is not triggered.

```ts
const mutation = useMutation({
  mutationFn: async (data) => {
    const res = await fetch('/api/submit', { method: 'POST', body: JSON.stringify(data) });
    return res.json(); // ← Bug: doesn't throw on 4xx
  },
  onError: (error) => toast.error(error.message), // never called
});
```

Native `fetch` doesn't throw on 4xx/5xx responses — it only throws on network errors. Show the fix (check `res.ok`), the custom `throwIfError` utility for all API calls, and typing the error as `ApiError` instead of `unknown`.""",

"""**Debug Scenario:**
A GraphQL client using `@apollo/client` makes 12 network requests on a dashboard page instead of the expected 3. Apollo DevTools shows the extra requests are duplicate queries with different variables appearing in the cache as separate entries.

Investigation reveals `useQuery` is called with inline object variables:

```ts
const { data } = useQuery(GET_USER, {
  variables: { filter: { active: true } }, // New object every render
});
```

Apollo compares variables by reference (shallow) for cache key generation. A new object reference = cache miss = new request. Show the fix using `useMemo` for variables, the Apollo `canonicalStringify` deep comparison option, and the `fetchPolicy: 'cache-first'` setting that prevents re-fetching.""",

"""**Debug Scenario:**
A `<DateRangePicker>` component allows selecting a start and end date. When the user selects an end date earlier than the start date, the UI shows the dates reversed but the `onChange` prop receives them in the correct order (start < end). The component silently reorders.

A test explicitly checks for the user's selected order (user selected end first) and the reversal in `onChange` is unexpected behavior. Show: the UX decision (should the component silently reorder or show a validation error?), how to make the behavior explicit via a `reorderOnOverlap` prop with TypeScript, and a unit test that documents the expected behavior.""",

"""**Debug Scenario:**
A Next.js API route handles webhook events from Stripe. Occasionally, Stripe sends duplicate webhook events (their retry mechanism), and the database records a charge twice. The route handler processes events idempotently... except for a race condition when two duplicate events arrive within 50ms of each other.

Show the database-level fix using a unique constraint on `stripe_event_id`, the PostgreSQL upsert (`INSERT ... ON CONFLICT DO NOTHING`), and how to test the race condition with a Vitest test that fires two concurrent webhook handlers and verifies only one database record is created.""",

"""**Debug Scenario:**
A developer reports a memory leak in a React component that renders a `<video>` element. Memory grows continuously while on the page, never released even after the video pauses.

```ts
useEffect(() => {
  const mediaSource = new MediaSource();
  videoRef.current.src = URL.createObjectURL(mediaSource);
  // No cleanup!
}, []);
```

`URL.createObjectURL` creates a blob URL that holds a reference to the `MediaSource` object until `URL.revokeObjectURL` is called. Show the complete cleanup: `URL.revokeObjectURL(url)`, `mediaSource.endOfStream()`, and removing all `SourceBuffer` objects. Explain why the garbage collector can't clean up blob URLs automatically.""",

"""**Debug Scenario:**
An E2E Playwright test for a dropdown menu is flaky — 30% of the time it fails with "Element is not visible" when trying to click a menu item. The menu opens correctly but the items fail the visibility check.

Chrome DevTools shows the dropdown menu uses `opacity: 0 → 1` as its open animation (200ms `transition`), and Playwright's click checks visibility before the animation completes.

Show Playwright's `waitForSelector` with `state: 'visible'`, `toBeVisible()` with a custom `timeout`, the `waitFor` with `{ state: 'stable' }` to wait for animation completion, and configuring `actionTimeout` globally in `playwright.config.ts`.""",

"""**Debug Scenario:**
A React app renders a canvas-based chart that calls `ctx.drawImage(offscreenCanvas, ...)`. In Safari, the chart displays blank on first render but appears after window resize.

The issue: `offscreenCanvas` is drawn to before it's appended to the DOM on Safari. Safari requires the canvas to be in the document before `drawImage` can use it as a source.

Show: the timing fix using `useLayoutEffect` (runs synchronously after DOM update), the Safari-specific workaround using `HTMLCanvasElement` instead of `OffscreenCanvas` as the rendering target, and a feature detection check `'OffscreenCanvas' in window`.""",

"""**Debug Scenario:**
A `<CheckboxGroup>` component allows selecting multiple options. After submitting the form and resetting with `form.reset()`, the checkboxes visually appear unchecked but `form.get('options')` still returns the previously selected values.

The checkboxes are controlled components:
```tsx
<input type="checkbox" checked={selected.includes(option)} onChange={...} />
```

React's controlled component should prevent this. Investigation shows `form.reset()` directly manipulates DOM values, bypassing React's state. Show why native `form.reset()` conflicts with React controlled inputs, and the correct reset: call `setSelected([])` (update React state) instead of or in addition to `form.reset()`.""",

"""**Debug Scenario:**
A Next.js app's `middleware.ts` is calling a rate-limiting function that uses `new Date()` for time comparison. In Vercel Edge Runtime, the `Date` object is based on the worker's time which can drift from true UTC by several seconds. Rate limiting windows are inaccurate.

Show: using `Deno.now()` (available in some edge runtimes) or `performance.now()` relative timestamps, synchronizing with a time endpoint on startup, and why using Redis `TIME` command (server-time) is more reliable than relying on edge worker clocks for rate limiting.""",

"""**Debug Scenario:**
A complex React form with 50 fields uses `react-hook-form` with `resolver: zodResolver(schema)`. Validation runs on every keystroke (`mode: 'onChange'`) and causes a 200ms delay on each keypress because the Zod schema is deeply nested and complex.

Profile confirms Zod validation takes 180ms on each `onChange`. Show: deferring validation to `mode: 'onBlur'` for complex schemas, lazy Zod schemas (`z.lazy()`) for circular schemas, splitting validation into field-level (fast) and cross-field (deferred), and using `startTransition` to run validation without blocking the keystroke.""",

"""**Debug Scenario:**
A team's GitHub Actions CI pipeline runs 300 unit tests in 4 minutes locally but 25 minutes in CI. The slow tests all involve `fs.readFile` and `path.resolve` operations.

Investigation shows the tests are running without proper mocking of the file system operations, so each test actually reads from disk. In CI, the file system is slower (shared EBS volume). Beyond mocking, show: using `memfs` for in-memory file system mocking, the `__mocks__` directory pattern for automatic Jest mocking of `fs`, and Jest's `--runInBand` vs `--maxWorkers` for I/O-bound tests.""",

"""**Debug Scenario:**
An `<InfiniteList>` component using `react-window`'s `VariableSizeList` doesn't scroll to the correct item after the list data is filtered. `scrollToItem(index)` scrolls to the visual position of the old index, not the filtered index.

```ts
listRef.current.scrollToItem(filteredItems.indexOf(targetItem));
// Scrolls to wrong position because VariableSizeList cached old row heights
```

`VariableSizeList` caches computed item heights. After filtering, the cached heights are stale. Show: calling `listRef.current.resetAfterIndex(0)` to clear the height cache after filtering, reinstating the correct `itemSize` function that maps to filtered items, and why the scroll position bug only manifests after filtering (not on initial render).""",

"""**Debug Scenario:**
A team's React app has a subtle UI bug: a `<Dropdown>` shows the wrong option as selected after the user picks an option and the component re-renders with new `options` props. The selected value in state is '3' but the dropdown shows the option labeled 'Beta' instead of 'Gamma'.

```ts
// options order changes between renders:
// Render 1: [{ id: '1', label: 'Alpha' }, { id: '2', label: 'Beta' }, { id: '3', label: 'Gamma' }]
// Render 2: [{ id: '2', label: 'Beta' }, { id: '1', label: 'Alpha' }, { id: '3', label: 'Gamma' }]
```

The dropdown uses the selected index (not ID) to track selection: `selectedIndex = options.findIndex(o => o.id === selected)`. When the options array reorders, the index changes. Show: always using stable IDs (not indices) as selected values, sorting the options array before rendering to ensure stable order, and the correct `findIndex` vs `find` usage for option lookup by ID.""",

]

"""
snippets/q_debugging.py — 28 FRESH Debugging questions (mix of debugging + code generation)
Zero overlap with archived set.
"""

Q_DEBUGGING = [

"""**Debug Scenario:**
A checkout form resets all field values whenever the user switches tabs in the browser and switches back. The form uses `useForm` from react-hook-form with `defaultValues` from an API call.

```ts
const { data: defaults } = useQuery(['user-defaults'], fetchDefaults);
const form = useForm({ defaultValues: defaults });
```

When the tab regains focus, the query refetches, `defaults` changes reference, and `useForm` re-initializes. Diagnose the problem and show the correct `react-hook-form` pattern for async default values that doesn't accidentally reset the form.""",

"""**Debug Scenario:**
A `<Select>` dropdown component uses a `ref` to position the dropdown menu relative to the trigger button. On initial render the menu appears at position (0, 0) for ~100ms before snapping to the correct position.

```ts
const triggerRef = useRef<HTMLButtonElement>(null);
const [menuPos, setMenuPos] = useState({ top: 0, left: 0 });

useEffect(() => {
  const rect = triggerRef.current!.getBoundingClientRect();
  setMenuPos({ top: rect.bottom, left: rect.left });
}, [isOpen]);
```

Explain why there's a flash at (0,0), and show the correct solution using `useLayoutEffect` vs `useEffect` with an analysis of when each fires relative to paint.""",

"""**Debug Scenario:**
A developer reports that removing a console.log statement from a component makes a bug disappear — the component renders correctly without the log but incorrectly with it. The log is:

```ts
console.log('render', Date.now());
```

This should be a no-op. Explain the class of bugs where adding logging changes program behavior in JavaScript, and diagnose whether this is a timing issue, a side-effect issue, or a StrictMode double-invoke issue.""",

"""**Debug Scenario:**
A production error tracking system shows a recurring error: `TypeError: Cannot read properties of undefined (reading 'map')` in a component that receives an array prop. The error only happens for ~0.1% of users and is unreproducible in development.

```tsx
function UserList({ users }: { users: User[] }) {
  return users.map(u => <UserCard key={u.id} user={u} />);
}
```

The TypeScript type says `users: User[]` — never undefined. Investigate: what causes a typed-as-non-nullable prop to be `undefined` at runtime, and implement defensive programming that catches this at the component boundary without hiding the real bug.""",

"""**Debug Scenario:**
A multi-page form wizard stores state in React context. When the user navigates from Step 3 back to Step 1 using the browser's back button, the form state is correct but the URL doesn't reflect the current step, so refreshing the page always goes to Step 3 (the last visited step).

Design a URL-synchronized form wizard where:
- The URL always reflects the current step (`?step=1`, `?step=2`, etc.)
- Browser back/forward navigate between steps
- Form state persists through navigation (not lost on back)
- Deep-linking to a specific step validates that previous steps were completed""",

"""**Debug Scenario:**
A dashboard WebSocket connection logs `WebSocket is already in CLOSING or CLOSED state` errors intermittently. The connection is managed in a custom hook.

```ts
useEffect(() => {
  const ws = new WebSocket(url);
  ws.onmessage = handler;
  return () => ws.close();
}, [url]);
```

The cleanup closes the socket, but in React 18 development StrictMode, the effect runs twice: open → close → open again. The second open finds the socket still in `CLOSING` state. Diagnose and fix without disabling StrictMode or adding `if (ws.readyState === WebSocket.OPEN)` guards.""",

"""**Debug Scenario:**
A table component implements column resizing by dragging column headers. The drag handler reads `startX` from a closure:

```ts
const startX = useRef(0);
const onMouseDown = (e: MouseEvent) => {
  startX.current = e.clientX;
  document.addEventListener('mousemove', onMouseMove);
};
const onMouseMove = (e: MouseEvent) => {
  const delta = e.clientX - startX.current; // always 0
};
```

`startX.current` is always 0 inside `onMouseMove` even though `onMouseDown` sets it correctly. Explain why `useRef` can exhibit stale values in event listener closures and show the correct fix.""",

"""**Debug Scenario:**
Sentry shows a recurring error: `DOMException: Failed to execute 'removeChild' on 'Node': The node to be removed is not a child of this node`. It happens when a portal-rendered modal is quickly opened and closed.

```ts
useEffect(() => {
  const el = document.createElement('div');
  document.body.appendChild(el);
  return () => document.body.removeChild(el); // fails intermittently
}, []);
```

React's concurrent mode can run cleanup before re-running effects, but the cleanup tries to remove a node that was already removed. Diagnose the exact sequence of events and show a robust portal cleanup pattern.""",

"""**Debug Scenario:**
An autocomplete input makes API requests as the user types. Requests are debounced 300ms. The bug: if the user types "ab" then clears to "a", sometimes the response for "ab" arrives after "a" and overwrites the "a" suggestions with "ab" suggestions.

```ts
const [query, setQuery] = useState('');
const [results, setResults] = useState([]);
useEffect(() => {
  const timer = setTimeout(() => {
    fetchSuggestions(query).then(setResults);
  }, 300);
  return () => clearTimeout(timer);
}, [query]);
```

The debounce cancels extra *requests* but not *stale responses*. Fix this using an ignore flag, AbortController, and explain the difference between the two approaches for this case.""",

"""**Debug Scenario:**
A Next.js app built with `output: 'export'` (static HTML export) shows blank pages in production when users navigate directly to URLs like `/products/123`. It works fine when navigating from the home page.

Explain why static exports fail on direct URL access for dynamic routes, the difference between client-side routing (SPA) and server-rendered routing, and show the Nginx/Apache rewrite rule that makes the static export work as an SPA with clean URLs.""",

"""**Debug Scenario:**
A `react-hook-form` controlled `<DatePicker>` shows the wrong date when the form is reset. `reset({ date: new Date() })` is called but the DatePicker UI shows the previous date.

```ts
const { control, reset } = useForm<FormValues>();
<Controller
  control={control}
  name="date"
  render={({ field }) => <DatePicker {...field} />}
/>
```

After `reset()`, `field.value` has the new date but the DatePicker component doesn't re-render. Investigate: is this a controlled component issue with the DatePicker library, a reference equality issue, or a `Controller` reset behavior?""",

"""**Debug Scenario:**
A production React app shows the error: `Rendered more hooks than during the previous render`. The error only happens when a user toggles a specific feature flag.

```tsx
function Dashboard({ featureEnabled }) {
  if (featureEnabled) {
    const data = useDashboardData(); // hook conditional on flag
    return <NewDashboard data={data} />;
  }
  const legacyData = useLegacyData();
  return <LegacyDashboard data={legacyData} />;
}
```

Explain the Rules of Hooks and why conditional hooks break React's reconciler. Show three refactoring approaches: early return, component splitting, and conditional hook wrapper.""",

"""**Debug Scenario:**
A `SortableList` using `@dnd-kit/sortable` works correctly on desktop but on iOS Safari, drag-and-drop doesn't register any touch events. The items appear to be draggable visually but don't respond to touch.

Investigation shows `@dnd-kit` requires a `PointerEvent` polyfill for older iOS versions, but the app targets iOS 15+. Diagnose why iOS Safari 15 may not fire the expected pointer events during drag and show the dnd-kit touch sensor configuration.""",

"""**Debug Scenario:**
A chart component using `canvas` 2D rendering renders at half the expected resolution on Retina/high-DPI screens. Text and lines appear blurry.

```ts
const ctx = canvas.getContext('2d');
canvas.width = containerWidth;
canvas.height = containerHeight;
// draws at 1x resolution on 2x screens
```

Show the complete fix using `devicePixelRatio` — both the canvas size scaling and the CSS size restoration — and explain why skipping the CSS reset makes the canvas appear 2x too large.""",

"""**Debug Scenario:**
An Intersection Observer is set up to trigger analytics when a section enters the viewport. In production, the callback fires immediately on page load before the user has scrolled, even for sections far below the fold.

```ts
const observer = new IntersectionObserver(callback);
observer.observe(section);
```

Explain why IntersectionObserver fires synchronously on `observe()` with `isIntersecting: false` initially, and how a misconfigured `threshold` or `rootMargin` with a large positive value could cause off-screen elements to report as intersecting immediately.""",

"""**Debug Scenario:**
A React app uses `React.lazy` + `Suspense` for code splitting route components. After a new deployment, some users see a blank white screen with no error message on certain routes.

Investigation reveals they're hitting a `ChunkLoadError` — the old chunk filenames were deleted after the new build. The Error Boundary only catches render errors, not dynamic import failures (which are async and don't propagate to the nearest ErrorBoundary).

Show how to catch `ChunkLoadError` specifically (it happens before render), add automatic page refresh logic, and prevent the blank screen.""",

"""**Debug Scenario:**
A form that submits data using a Server Action shows an unhandled exception in the browser when the server throws a validation error, instead of showing the error in the form fields.

```ts
async function submitForm(formData: FormData) {
  'use server';
  if (!validate(formData)) throw new Error('Invalid data'); // unhandled on client
}
```

Server Actions that throw propagate to the nearest Error Boundary or crash the app. Redesign the action to return a typed result instead of throwing, and show how `useActionState` (React 19) handles the result correctly.""",

"""**Debug Scenario:**
An animated counter component using `requestAnimationFrame` runs too fast on high-refresh-rate monitors (120Hz/144Hz). The counter was designed assuming 60fps.

```ts
let progress = 0;
function animate() {
  progress += 0.016; // assumes 16.7ms per frame (60fps)
  if (progress < 1) requestAnimationFrame(animate);
}
```

Fix the animation to be frame-rate independent using `performance.now()` timestamps and delta time, and show the correct pattern for all `requestAnimationFrame` animations.""",

"""**Debug Scenario:**
A `<FileUpload>` component allows dragging files. After the user drops a file, the page navigates away (browser opens the file) instead of the component handling it.

```ts
dropzone.addEventListener('drop', (e) => {
  const file = e.dataTransfer!.files[0];
  handleFile(file);
});
```

Diagnose the missing `e.preventDefault()` and `e.stopPropagation()` calls, explain exactly what browser default behavior fires on file drop, and show the complete drag-and-drop implementation that prevents page navigation.""",

"""**Debug Scenario:**
A Material UI `Autocomplete` component shows stale options after the user clears the input. The options are fetched from an API based on the input value.

```tsx
const [inputVal, setInputVal] = useState('');
const { data: options } = useQuery(['options', inputVal], () => fetchOptions(inputVal));

<Autocomplete
  options={options ?? []}
  onInputChange={(_, value) => setInputVal(value)}
/>
```

When the user clears the input (empty string), the query key changes to `['options', '']` and fetches a new set of options. But the dropdown still shows the previous options during the loading state. Show how to use `keepPreviousData` (React Query v4) or `placeholderData` (v5) correctly here, and whether it's the right UX.""",

"""**Debug Scenario:**
A server-rendered Next.js page shows different content to the same user on subsequent requests because a `Math.random()` call in a Server Component produces different values each render.

```tsx
// Server Component:
const randomTip = tips[Math.floor(Math.random() * tips.length)];
```

Beyond the obvious fix (seed the randomness), diagnose why this causes specific problems in Next.js: (1) hydration mismatch if the component is also client-side, (2) different content on CDN cache misses, (3) A/B test contamination. Show the correct approach for "random but stable" server-rendered content.""",

"""**Debug Scenario:**
A custom `useScript` hook that dynamically loads a third-party script fires its `onLoad` callback twice in development.

```ts
useEffect(() => {
  const script = document.createElement('script');
  script.src = src;
  script.onload = onLoad;
  document.head.appendChild(script);
  return () => document.head.removeChild(script);
}, [src]);
```

React 18 StrictMode mounts → unmounts → remounts. The second mount appends a new script, but as the first script was already downloaded and cached by the browser, `onload` fires immediately. Show a `useScript` implementation that handles StrictMode correctly using a module-level cache of loaded scripts.""",

"""**Debug Scenario:**
A `<Tooltip>` component positions itself relative to its trigger but appears outside the viewport for triggers near the edges. The positioning logic reads `getBoundingClientRect()` correctly but doesn't account for viewport overflow.

```ts
const rect = trigger.getBoundingClientRect();
setPos({ top: rect.bottom + 8, left: rect.left });
// Doesn't check if pos.left + tooltipWidth > window.innerWidth
```

Implement viewport-aware tooltip positioning that automatically flips the tooltip to the top when there's no room below, and shifts horizontally when the tooltip would overflow the right edge. Show the complete positioning calculation.""",

"""**Debug Scenario:**
A React component tree using `useContext` has 15 components subscribed to a `DataContext`. Profiling shows every one of those 15 components re-renders when any part of the context changes, even unrelated fields.

The context value is a large object `{ users, reports, settings, filters }`. Changing only `filters` causes all 15 components to re-render, including those that only read `users`.

Without reaching for `use-context-selector`, redesign the context splitting strategy — splitting into `UsersContext`, `ReportsContext`, etc. — and show the before/after render count in React DevTools.""",

"""**Debug Scenario:**
A Playwright E2E test fails intermittently because an element transitions from `display: none` to `display: block` during a CSS animation and Playwright can't click it during the transition.

```ts
await page.click('.modal-button'); // fails: element not visible
```

Show the correct Playwright waiting strategy using `waitForSelector` with `state: 'visible'`, `locator.waitFor()`, and the difference between Playwright's actionability checks (visible, stable, enabled). Explain why `await page.waitForTimeout(500)` is an anti-pattern.""",

"""**Debug Scenario:**
A production Node.js/Next.js server shows increasing memory usage over 48 hours, eventually requiring a restart. Heap snapshots show an ever-growing `Map` attached to a module-level `RequestCache` object.

```ts
// lib/cache.ts (module-level singleton)
const RequestCache = new Map<string, { data: unknown; timestamp: number }>();
```

The cache has no eviction policy. In serverless environments (Vercel), module-level caches reset per cold start — but this app runs on a long-lived Node.js server. Implement a proper cache with TTL eviction and max-size enforcement.""",

"""**Debug Scenario:**
A `<DragAndDropBoard>` using `react-beautiful-dnd` shows visual lag of ~100ms between the drag start and the dragged item appearing to move. The lag only occurs on the first drag in a session.

Chrome DevTools Performance tab shows a large "Recalculate Style" event (45ms) on drag start, caused by applying a global CSS class that triggers cascade recalculation across all board items.

Show the fix using `will-change: transform` preloaded on potential drag targets, CSS `contain: layout`, and why `requestAnimationFrame` scheduling of the class application reduces the perceived lag.""",

"""**Debug Scenario:**
A Next.js app shows a hydration mismatch error on a page that renders a greeting based on time of day:

```tsx
// Server renders at 10:00 AM:
<h1>Good morning, Alice!</h1>
// Client hydrates at 10:00 AM but getHours() returns different value due to timezone:
<h1>Good afternoon, Alice!</h1>
```

The server runs in UTC, the user's browser is UTC+5:30. Explain exactly when hydration mismatches occur (server HTML !== first client render), why React throws vs warns depending on severity, and show three strategies: (1) render greeting client-only with `useEffect`, (2) pass the server-calculated greeting as a prop, (3) use `suppressHydrationWarning` and when it's acceptable.""",

]

"""
snippets/q_react.py — 28 FRESH React questions (mix of debugging + code generation)
Zero overlap with archived set.
"""

Q_REACT = [

"""**Task (Code Generation):**
Implement a `useEventCallback` hook that always has a stable reference (like `useCallback([])`) but always calls the latest version of the callback. This is needed for event handlers passed to memoized child components.

```ts
// Usage target:
const handleClick = useEventCallback((e: MouseEvent) => {
  console.log(latestState); // always fresh, no stale closure
});
// handleClick reference never changes between renders
```

Implement the hook. Explain why this pattern is safer than `useCallback` with a full dep array, and where it can go wrong (e.g., calling the handler during render).""",

"""**Debug Scenario:**
A `useAsync` hook runs a fetch and calls `setState` with the result. In production, users occasionally see a brief flash of a previous user's data when switching accounts.

```ts
function useAsync(fn: () => Promise<unknown>) {
  const [state, setState] = useState({ loading: true, data: null });
  useEffect(() => {
    fn().then(data => setState({ loading: false, data }));
  }, [fn]);
}
```

The `fn` prop is stable (wrapped in `useCallback`). Identify the race condition and fix it without using a library. Explain how React 18's `startTransition` could help here and whether it actually eliminates the need for an abort flag.""",

"""**Task (Code Generation):**
Build a `<Portal>` component that renders children into a DOM node outside the React tree (for modals, tooltips, dropdowns). Requirements:
- Works with SSR (no `document` access during server render)
- Cleans up the DOM node on unmount
- Forwards `ref` to the inner container
- Accepts a `container` prop (defaults to `document.body`)

Show the full implementation and explain why `createPortal` alone isn't sufficient for the SSR + cleanup requirements.""",

"""**Debug Scenario:**
A custom `usePrevious` hook is used across the dashboard to compare prop changes. A bug report says it returns the *current* value instead of the previous one in React 18.

```ts
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  useEffect(() => {
    ref.current = value;
  });
  return ref.current;
}
```

Explain precisely when `ref.current` is updated relative to render in React 18's concurrent mode. Is the bug real or a misuse of the hook? Show a version that behaves correctly even under concurrent rendering.""",

"""**Task (Code Generation):**
Implement a `useIntersectionObserver` hook that lazily loads data when a sentinel element enters the viewport. Requirements:
- Accepts `threshold` and `rootMargin` options
- Returns `[sentinelRef, isIntersecting]`
- Disconnects the observer when the component unmounts OR when `isIntersecting` becomes true (one-shot mode configurable via `once` option)
- Works correctly if the sentinel element is conditionally rendered

Show usage in a infinite-scroll list.""",

"""**Debug Scenario:**
A `<MultiSelect>` component loses focus after every keystroke when the user is typing in its search input. The component tree looks like:

```tsx
function MultiSelect({ options, onSelect }) {
  const [query, setQuery] = useState('');
  const filtered = options.filter(o => o.label.includes(query));
  
  return (
    <Dropdown>
      <Input value={query} onChange={e => setQuery(e.target.value)} />
      {filtered.map(o => <Option key={o.id} {...o} />)}
    </Dropdown>
  );
}
```

The `Dropdown` wrapper is defined inside `MultiSelect`'s render. Identify the root cause and fix it. Why does defining a component inside another component's render function cause this specific behavior?""",

"""**Task (Code Generation):**
Implement a `useVisibilityChange` hook that detects when the browser tab becomes hidden/visible (Page Visibility API) and automatically pauses/resumes a polling interval.

```ts
// Target API:
const { isVisible } = useVisibilityChange({
  onHide: () => stopPolling(),
  onShow: () => resumePolling(),
});
```

Then implement a `usePolling(fn, interval)` hook that uses `useVisibilityChange` internally — polling only when the tab is visible and immediately re-fetching when the tab becomes visible again after being hidden.""",

"""**Debug Scenario:**
A context-based theme system causes every component that calls `useTheme()` to re-render whenever any part of the theme changes, even if that component only reads one token (e.g., `theme.colors.primary`).

```tsx
const ThemeContext = createContext<Theme>({} as Theme);
export const useTheme = () => useContext(ThemeContext);
```

The theme object is memoized at the provider level. Yet changing `theme.spacing.lg` re-renders a button that only uses `theme.colors.primary`. Diagnose and fix this without adding a library, using only React primitives.""",

"""**Task (Code Generation):**
Implement a `<ErrorBoundary>` component that:
- Catches render errors and shows a fallback UI
- Exposes a `reset()` method via a `resetKeys` prop (re-mounts children when any key changes)
- Calls an `onError(error, errorInfo)` callback for logging
- Works as a typed React component (no class component in the public API — wrap it)

Show the class component implementation + a functional wrapper with the `resetKeys` pattern.""",

"""**Debug Scenario:**
A `useFormField` hook manages input state and validation. The `validate` function is called on every keystroke and is expensive (runs a regex + async API call). Using `useCallback` doesn't help because `validate` has many deps.

```ts
const validate = useCallback(async (val: string) => {
  if (!REGEX.test(val)) return 'Invalid format';
  const exists = await api.checkExists(val);
  return exists ? 'Already taken' : null;
}, [REGEX, api]); // both stable
```

Despite stable deps, the validate function reference changes. The React ESLint plugin isn't flagging anything. What causes `useCallback` to return a new reference even with stable deps? Prove your answer.""",

"""**Task (Code Generation):**
Write a `useDeferredState<T>` hook that behaves like `useState` but defers expensive re-renders using `startTransition` automatically. The hook should:
- Expose `[deferredValue, setValue]` — reads stay fast, writes are deferred
- Accept a `isPending` flag in the returned tuple
- Work correctly if multiple `setValue` calls happen before the transition commits

Compare this to React's built-in `useDeferredValue` and explain when to use each.""",

"""**Debug Scenario:**
The app uses a render-prop-based `<DataProvider>` that fetches data and renders children with the result. After a migration to React 18, the `children` function is being called twice with the loading state before settling on the data state.

```tsx
<DataProvider url="/api/data">
  {({ loading, data }) => loading ? <Spinner /> : <Table rows={data} />}
</DataProvider>
```

Explain why StrictMode in React 18 causes this double-invocation and whether it indicates a real bug. Show how to make `DataProvider` StrictMode-safe.""",

"""**Task (Code Generation):**
Implement a `useLocalStorage<T>` hook with:
- Synchronization across tabs via `storage` event
- TypeScript generics with a required serializer/deserializer or default JSON
- SSR safety (returns `initialValue` during SSR)
- Handling of `JSON.parse` errors (corrupted localStorage values)

```ts
const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');
```
Show the full implementation including the cross-tab sync logic.""",

"""**Debug Scenario:**
A `<VirtualList>` uses `useRef` to store scroll position and a `ResizeObserver` to detect container size changes. After adding a second `ResizeObserver` for row heights, the list occasionally renders blank until the user scrolls.

The blank render only happens when both observers fire in the same animation frame. Diagnose the race condition between two `ResizeObserver` callbacks both calling `setState`, and explain how React 18's automatic batching affects this specific case.""",

"""**Task (Code Generation):**
Build a `useUndoRedo<T>` hook for managing undo/redo history of any state value.

Requirements:
- `[state, setState, { undo, redo, canUndo, canRedo, history }]` API
- Max history depth configurable (evicts oldest on overflow)
- Batches rapid successive `setState` calls within a debounce window into a single history entry
- Does NOT store the entire state tree each time — stores a diff/patch if possible

Show the implementation and an example with a text editor component.""",

"""**Debug Scenario:**
A radio group component conditionally renders options based on an `options` prop. When the options list changes, the previously selected option sometimes remains visually selected even though the `value` prop has been reset.

```tsx
options.map((opt, i) => (
  <input
    type="radio"
    key={i}  // keyed by index
    name="group"
    value={opt.value}
    checked={value === opt.value}
  />
))
```

Explain the exact reconciliation behavior that causes the visual inconsistency when keyed by index, with a concrete example showing DOM reuse.""",

"""**Task (Code Generation):**
Implement a `useAsync<T>` hook that manages the full lifecycle of an async operation:

```ts
const { data, error, loading, run, cancel } = useAsync(fetchReports);
```

Requirements:
- `run(...args)` executes the async function
- `cancel()` aborts in-flight requests (AbortController)
- Prevents setState after unmount
- `data` and `error` reset when `run` is called again
- `loading` is true only during active requests, not between calls

Include TypeScript generics for the function signature.""",

"""**Debug Scenario:**
A memoized `<ChartPanel>` re-renders on every parent tick despite wrapping in `React.memo`. React DevTools shows the `series` prop as the culprit — it changes reference every render. But `series` is produced by a `useMemo` with a stable `data` dependency.

```ts
const series = useMemo(() => transformData(data), [data]);
```

`transformData` is imported from a utility module. Adding `console.log('recomputed')` confirms the memo IS being recalculated. Yet `data` hasn't changed (confirmed with `Object.is`). What can cause a `useMemo` to recompute when its dependencies haven't changed?""",

"""**Task (Code Generation):**
Write a `<Transition>` component (no libraries) that animates children in/out using CSS classes.

```tsx
<Transition show={isOpen} enterClass="fade-in" leaveClass="fade-out" duration={300}>
  <Modal />
</Transition>
```

Requirements:
- Mounts the child when `show` becomes true, unmounts after leave animation completes
- Does not rely on `setTimeout` for the duration — uses `transitionend` event
- Handles rapid show/hide toggling correctly (cancels in-progress transitions)
Show the full implementation.""",

"""**Debug Scenario:**
A team reports that calling `ReactDOM.flushSync` inside a `useEffect` throws an error in production but not in development.

```ts
useEffect(() => {
  ReactDOM.flushSync(() => setState(next)); // Error: flushSync was called from inside a lifecycle method
}, [dep]);
```

Explain when `flushSync` is and isn't safe to call, why the error differs between dev/prod, and what the correct alternative is when you need synchronous DOM updates after an effect.""",

"""**Task (Code Generation):**
Implement a compound component pattern for a `<Tabs>` component:

```tsx
<Tabs defaultIndex={0}>
  <Tabs.List>
    <Tabs.Tab index={0}>Overview</Tabs.Tab>
    <Tabs.Tab index={1}>Details</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel index={0}><Overview /></Tabs.Panel>
  <Tabs.Panel index={1}><Details /></Tabs.Panel>
</Tabs>
```

Requirements:
- Context-based state sharing (no prop drilling)
- Keyboard navigation (Arrow keys, Home, End)
- ARIA attributes (`role="tablist"`, `aria-selected`, `aria-controls`)
- TypeScript-typed sub-components with `displayName`""",

"""**Debug Scenario:**
A `<DatePicker>` calendar renders a grid of 42 day cells. Clicking a date fires `onSelect` correctly, but the selected date highlighted in the grid is always one day behind — the highlight updates on the *next* click, not the current one.

```tsx
const [selected, setSelected] = useState<Date | null>(null);
const handleDayClick = (date: Date) => {
  setSelected(date);
  onSelect(selected); // stale closure!
};
```

Beyond the obvious `onSelect(date)` fix, explain in detail why closures in event handlers capture stale state in React, and show two additional patterns that would have prevented this bug.""",

"""**Task (Code Generation):**
Create a `useKeyboardShortcut` hook that registers global keyboard shortcuts and properly handles:
- Modifier combos: `Ctrl+Shift+K`, `Cmd+K`
- Input field exclusion (shortcuts don't fire when user is typing in textarea/input)
- Preventing browser default behaviors (`e.preventDefault()` only when shortcut is handled)
- Cleanup on unmount

```ts
useKeyboardShortcut('mod+k', () => openCommandPalette()); // mod = Ctrl or Cmd
useKeyboardShortcut('Escape', closeModal, { allowInInput: true });
```""",

"""**Debug Scenario:**
After upgrading React from 17 to 18 with `createRoot`, an analytics hook that fires on every route change fires twice on initial load.

```ts
useEffect(() => {
  analytics.track('page_view', { path: location.pathname });
}, [location.pathname]);
```

In React 17, this fired exactly once on mount. In React 18 with StrictMode, it fires twice. But the team confirms this is production (StrictMode disabled). Why does the effect fire twice on initial load in React 18 even without StrictMode?""",

"""**Task (Code Generation):**
Implement a `useMediaQuery(query: string): boolean` hook that:
- Uses `window.matchMedia` to evaluate CSS media queries
- Updates reactively when the media query result changes
- Is SSR-safe (returns a configurable `defaultValue` on the server)
- Doesn't add a new event listener on every render

```ts
const isDesktop = useMediaQuery('(min-width: 1024px)');
const prefersDark = useMediaQuery('(prefers-color-scheme: dark)');
```

Show the implementation and explain the `addListener` vs `addEventListener` API difference.""",

"""**Debug Scenario:**
A controlled `<NumberInput>` component allows the user to type decimal numbers. When the user types "1.0", the input immediately snaps to "1" because the parent `parseInt`s the value and sets state.

```tsx
<input
  value={value}
  onChange={e => onChange(parseInt(e.target.value, 10))}
/>
```

The UX requirement is: allow the user to type freely (including "1.", "1.0", "0.0") but only propagate valid, fully-entered numbers to the parent. Design and implement an `UncontrolledNumberInput` that meets this requirement without fighting React's controlled input model.""",

"""**Task (Code Generation):**
Build a `<Virtualized>` component that renders only visible rows in a large list without using any virtualization library.

Requirements:
- Uses `IntersectionObserver` (NOT `scroll` events) to detect row visibility
- Renders a fixed-height placeholder for off-screen rows to maintain scrollbar integrity
- Handles dynamic row heights via `ResizeObserver`
- `windowSize` prop controls how many rows above/below viewport to keep mounted

Show the implementation. Explain the tradeoffs vs react-window.""",

"""**Debug Scenario:**
A `useFormValidation` hook runs async validators in parallel using `Promise.all`. When the user submits a form with 5 fields, network errors on field 2 cause fields 3-5 to never resolve their error state — they're stuck in `validating: true`.

```ts
const results = await Promise.all(fields.map(field => validate(field)));
```

`Promise.all` rejects on first failure. Fix the validator to collect all results including failures, and explain the difference between `Promise.all`, `Promise.allSettled`, and `Promise.any` in the context of form validation.""",

]

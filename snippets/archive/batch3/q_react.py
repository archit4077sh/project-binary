"""
snippets/q_react.py — BATCH 3: 28 brand-new React questions
Zero overlap with batch1 or batch2 archives.
"""

Q_REACT = [

"""**Task (Code Generation):**
Implement a `useFocusTrap` hook that traps keyboard focus inside a modal container (WCAG 2.1 requirement):

```ts
const { containerRef } = useFocusTrap({ active: isOpen });
return <div ref={containerRef}>{children}</div>;
```

The hook must:
- On activation, move focus to the first focusable element inside the container
- Cycle Tab/Shift+Tab through focusable descendants (`a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])`)
- Return focus to the previously focused element on deactivation
- Handle dynamically added/removed focusable elements (use MutationObserver)

Show the complete implementation.""",

"""**Debug Scenario:**
A `<ComboBox>` component uses `useId()` to link its `<input>` with a `<listbox>` via `aria-controls`. After a page transition (Next.js App Router soft navigation), the generated ID changes, silently breaking the ARIA association.

```tsx
const id = useId(); // stable per mount, but page transition remounts
<input aria-controls={`${id}-listbox`} />
<ul id={`${id}-listbox`} role="listbox">
```

Explain why `useId()` generates different values across remounts, the ARIA requirement that `aria-controls` references a stable ID, and show a fix using a prop-driven stable ID with a `useId()` fallback.""",

"""**Task (Code Generation):**
Build a `<ResizablePanel>` component that allows users to drag a divider to resize two adjoining panels:

```tsx
<ResizablePanel
  direction="horizontal"
  initialSplit={60} // 60% left, 40% right
  min={20} max={80}
  onResize={({ leftPct, rightPct }) => saveLayout({ leftPct, rightPct })}
>
  <LeftPanel />
  <RightPanel />
</ResizablePanel>
```

Show: the drag state management, pointer event handling (supports touch and mouse), CSS `flex-basis` for panel sizing, and how to prevent text selection during drag.""",

"""**Debug Scenario:**
A React 18 app uses `useSyncExternalStore` to subscribe to a global config object. On server-side rendering, the store returns different values than `getServerSnapshot` specifies, causing a hydration warning.

```ts
const config = useSyncExternalStore(
  store.subscribe,
  () => store.get(),        // client snapshot
  () => ({ theme: 'light' }) // server snapshot
);
```

The server renders with `theme: 'dark'` (from the request cookie) but `getServerSnapshot` always returns `light`. Diagnose and show how to pass request-scoped server state into `getServerSnapshot` without breaking the hook's contract.""",

"""**Task (Code Generation):**
Implement a generic `<TreeView>` component for rendering hierarchical data with:
- Expand/collapse nodes (controlled and uncontrolled modes)
- Keyboard navigation: arrow keys to expand/collapse, home/end to jump to first/last
- Multi-select with Shift+click and Ctrl+click
- Virtualized rendering for trees with >1000 nodes
- ARIA tree/treeitem roles with correct `aria-expanded`, `aria-selected`, `aria-level`

Show the data type definition, the recursive node renderer, and the keyboard handler.""",

"""**Debug Scenario:**
A `useTimeout` hook is used to auto-dismiss a toast notification after 5 seconds. During Cypress tests, `cy.clock()` is used to fast-forward time, but the toast never dismisses.

```ts
function useTimeout(fn: () => void, delay: number) {
  useEffect(() => {
    const id = setTimeout(fn, delay);
    return () => clearTimeout(id);
  }, [fn, delay]);
}
```

Investigation shows `fn` changes reference on every render (it's an inline arrow function), causing the effect to re-run and reset the timer. Diagnose the stale reference + Cypress clock interaction, and fix both the hook and the test.""",

"""**Task (Code Generation):**
Implement a `useMeasure` hook that returns accurate layout measurements for a DOM element, updated on resize:

```ts
const [ref, { width, height, top, left }] = useMeasure<HTMLDivElement>();
return <div ref={ref}>Width: {width}px</div>;
```

Requirements:
- Uses `ResizeObserver` for size changes
- Uses `IntersectionObserver` for position changes (element moves in scroll container)
- Debounces measurement updates to avoid layout thrashing
- SSR-safe (returns zero values on server)
- TypeScript generic constrains ref to `HTMLElement` subtypes""",

"""**Debug Scenario:**
A radio button group inside a React `<form>` element submits the wrong value. The component uses controlled inputs:

```tsx
const [selected, setSelected] = useState('option-a');
// Clicking option-b shows option-b selected visually, but form.get('choice') === 'option-a'
<input type="radio" name="choice" value="option-b" checked={selected === 'option-b'} onChange={() => setSelected('option-b')} />
```

React's controlled radio button requires synchronous re-render between `onChange` and the browser's form data collection. In React 18 concurrent mode, state updates can be deferred. Show why this causes a mismatch and the fix using `flushSync` or a non-concurrent event handler.""",

"""**Task (Code Generation):**
Build a `useAnimatedNumber` hook that smoothly animates a numerical value from its previous to its new value:

```ts
const displayValue = useAnimatedNumber(rawCount, {
  duration: 600,
  easing: 'easeOutCubic',
  formatter: (n) => `$${n.toFixed(2)}`,
});
```

Show: `requestAnimationFrame` loop with proper frame-rate independence, cubic easing implementation, cleanup on fast value changes (cancel previous animation), and how to pause animation when the tab is hidden (`document.visibilityState`).""",

"""**Debug Scenario:**
A custom `useWindowSize` hook causes every component that uses it to re-render on every window resize event — even when only width changes and the consuming component only uses height.

```ts
const { width, height } = useWindowSize();
```

Show three progressive fixes: (1) throttle resize events, (2) allow selector-based subscriptions so components only re-render when their dimension of interest changes, (3) use `useSyncExternalStore` with a size snapshot for the canonical React 18 approach.""",

"""**Task (Code Generation):**
Implement a `<Stepper>` component for multi-step forms that:
- Shows steps with status (completed ✓, current ●, upcoming ○)
- Allows navigation back to completed steps but not to future steps
- Persists step completion state across browser refreshes (sessionStorage)
- Emits `onStepChange(from, to)` for analytics
- Is fully keyboard accessible (Tab to navigate between step indicators, Enter to jump to a completed step)

Show the state management, the step indicator rendering, and the sessionStorage integration.""",

"""**Debug Scenario:**
A component renders markdown content using `dangerouslySetInnerHTML`. After a content update, links inside the rendered HTML have click handlers attached via `document.querySelectorAll('a[data-internal]')` in a `useEffect`. When the content changes and React re-renders the HTML, the old event listeners leak because they were attached to DOM nodes that got replaced.

Diagnose why React replaces (not patches) innerHTML on re-render, and show the correct pattern using event delegation (`container.addEventListener('click', handler)`) that doesn't require re-attaching listeners on every content change.""",

"""**Task (Code Generation):**
Build a `useVirtualKeyboard` hook that detects when the mobile virtual keyboard is open and adjusts viewport height:

```ts
const { isKeyboardOpen, viewportHeight } = useVirtualKeyboard();
// viewportHeight: actual visible area above the keyboard
```

Modern API: use `window.visualViewport` (`resize` event watches actual viewport). Legacy fallback: compare `window.innerHeight` before and after `focus` on inputs. Show both approaches, the React hook, and a CSS variable `--viewport-height` that gets updated so fullscreen layouts don't get obscured by the keyboard.""",

"""**Debug Scenario:**
A filterable list component uses `useMemo` to compute filtered results. Profiling shows `useMemo` is recomputing on every keystroke even when the `items` array hasn't changed:

```ts
const filtered = useMemo(
  () => items.filter(item => item.name.includes(query)),
  [items, query] // items is from a zustand store
);
```

The Zustand store's `items` selector creates a new array on every store update (even for unrelated state changes) because of `state.items.filter(...)` in the selector. Show how to fix the Zustand selector first, then explain why fixing the selector is more important than optimizing `useMemo`.""",

"""**Task (Code Generation):**
Implement a `<ContextMenu>` component that shows a right-click context menu:

```tsx
<ContextMenu
  trigger={<FileItem file={file} />}
  items={[
    { label: 'Open', icon: <OpenIcon />, action: () => open(file) },
    { label: 'Rename', shortcut: 'F2', action: () => startRename(file) },
    { type: 'separator' },
    { label: 'Delete', danger: true, action: () => deleteFile(file) },
  ]}
/>
```

Requirements: positions intelligently at click coordinates (flips when near viewport edge), closes on Escape/outside click/scroll, supports keyboard navigation, renders in a Portal.""",

"""**Debug Scenario:**
A `<DataGrid>` component renders 500 rows. Sorting a column causes a 2-second freeze in the browser. The sort runs in the event handler:

```ts
const handleSort = (col: Column) => {
  const sorted = [...rows].sort((a, b) => compare(a[col.key], b[col.key]));
  setRows(sorted);
};
```

The sort itself takes 20ms; the 2-second freeze is React re-rendering 500 rows. Show three solutions: (1) `startTransition` to defer the non-urgent sort update, (2) virtualization to render only visible rows, (3) moving the sort to a Web Worker and show how to communicate with it from a React hook.""",

"""**Task (Code Generation):**
Implement a `useScrollRestoration` hook for a Next.js app that remembers scroll position per route:

```ts
// On page A at scroll position 800px → navigate to page B → back → 
// page A scroll restores to 800px
useScrollRestoration();
```

Requirements:
- Stores scroll position by `pathname + search` (not hash)
- Saves on `popstate` / route change start
- Restores after route change complete + layout painted (`requestAnimationFrame`)
- Works with both Back button and programmatic navigation
- Integrates with Next.js App Router's navigation events""",

"""**Debug Scenario:**
A complex form uses `react-hook-form` with `mode: 'onChange'`. When a user fills the last field, the entire form re-renders (200+ fields) for every keystroke.

Profile reveals `watch()` is called at the top level without a field name (watches all fields), and the component that calls `watch()` wraps the entire form:

```ts
const values = watch(); // subscribes to ALL field changes
```

Show the fix using field-level `watch('fieldName')` subscriptions, the `useWatch` hook, and `<Controller>` with isolated re-renders. Measure the improvement in render count.""",

"""**Task (Code Generation):**
Build a `createStore<T>` function (zero dependencies, ~50 lines) that provides a React-friendly observable store:

```ts
const counterStore = createStore({ count: 0 });
counterStore.setState(s => ({ count: s.count + 1 }));

// In component (only re-renders when count changes):
const count = counterStore.use(s => s.count);
```

Show: pub/sub notification, selector-based subscription with equality checks, `useSyncExternalStore` integration, batched updates using `queueMicrotask`, and TypeScript inference of the state shape.""",

"""**Debug Scenario:**
A `<Tooltip>` that shows on hover has a race condition: rapidly moving the mouse in and out causes multiple tooltips to appear simultaneously and not dismiss.

```ts
const [visible, setVisible] = useState(false);
<div
  onMouseEnter={() => setTimeout(() => setVisible(true), 200)}
  onMouseLeave={() => setVisible(false)}
/>
```

The delayed show timer fires after the hide has already run. Show the complete fix with `useRef` to track the timer ID and cancel it on `onMouseLeave`, and explain why `useEffect` with a dependency on `visible` would create a worse race condition.""",

"""**Task (Code Generation):**
Implement a `useInfiniteScroll` hook that loads more data when a sentinel element enters the viewport:

```ts
const { items, loadMore, isLoading, hasMore, sentinelRef } = useInfiniteScroll({
  fetchFn: (cursor) => api.getItems({ cursor, limit: 20 }),
});
// Attach sentinelRef to a div at the bottom of the list
<div ref={sentinelRef} />
```

Requirements: uses `IntersectionObserver`, prevents duplicate fetches during in-flight requests, supports cursor-based and page-based pagination, handles fetch errors with retry, cleans up observer on unmount.""",

"""**Debug Scenario:**
A server-side rendered React component tree includes a third-party `<Map>` component that accesses `window.google` on render. In Next.js, this causes:

```
ReferenceError: window is not defined
```

The third-party component isn't SSR-compatible and can't be modified. Show three valid workarounds: (1) `next/dynamic` with `ssr: false`, (2) a client-side only rendering guard with `isMounted` state, (3) `typeof window !== 'undefined'` guard.  For each, explain when it renders null vs a loading state, and which approach avoids layout shift.""",

"""**Task (Code Generation):**
Build a `<ColorPicker>` component with:
- A 2D saturation/lightness gradient canvas (click to pick color)
- A hue slider
- An alpha (opacity) slider
- Hex/RGB/HSL input fields that sync bidirectionally with the sliders
- Outputs `{ hex, rgb, hsl, alpha }`

Show the HSL↔RGB conversion functions, the canvas gradient rendering using `CanvasGradient`, and how to handle the color model synchronization without infinite update loops.""",

"""**Debug Scenario:**
A Next.js App Router page uses a Server Component to fetch user data and passes it to a Client Component. The Server Component re-renders on every navigation even when the data hasn't changed because the fetch isn't cached.

```tsx
// Server Component:
const user = await fetch('/api/user', { cache: 'no-store' }); // always fresh
```

The developer wants the user data to be cached for 60 seconds. Explain the difference between `cache: 'no-store'`, `next: { revalidate: 60 }`, and `React.cache()` for request deduplication within a single render tree. Show the correct combination for "cache 60s, deduplicate within request".""",

"""**Task (Code Generation):**
Implement a `useGesture` hook that recognizes common touch gestures:

```ts
const bind = useGesture({
  onSwipeLeft: () => goToNext(),
  onSwipeRight: () => goToPrev(),
  onPinch: ({ scale }) => setZoom(scale),
  onLongPress: () => showContextMenu(),
  threshold: { swipe: 50, longPress: 500 },
});
<div {...bind()} />
```

Show: pointer event handling for cross-device support, velocity-based swipe detection, pinch distance calculation from two touch points, long press with cancel on move, and cleanup.""",

"""**Debug Scenario:**
After migrating from Create React App to Vite, the app's `process.env.REACT_APP_API_URL` references all return `undefined`. Vite doesn't inject `process.env` — it uses `import.meta.env.VITE_*` instead.

Beyond the mechanical migration (`REACT_APP_` → `VITE_`), show: how to maintain backward compatibility during migration using Vite's `define` config to polyfill `process.env`, how to update `.env` files, and the key security difference between Create React App's env variable exposure and Vite's `VITE_` prefix convention.""",

"""**Task (Code Generation):**
Build a `<MentionInput>` (like Slack's `@mention`) that:
- Shows a dropdown of users when the user types `@`
- Filters the user list based on text after `@`
- Inserts the mention as a styled chip and continues text input
- Exports the final value as both plain text and a structured format `{ text, mentions: User[] }`
- Supports keyboard navigation in the dropdown

Show the input split/merge logic, the dropdown positioning relative to the cursor, and the value serialization.""",

"""**Debug Scenario:**
A custom rich text editor stores content as a JSON tree. When the user presses Ctrl+Z (undo), the editor reverts correctly — but the React component's local state (cursor position, selection range) is NOT reverted, causing the cursor to jump to position 0.

The undo system reverts the document content `useState` but there's no undo for `selectionState`. Design an integrated undo stack that stores both document and selection state in every history entry, and show how to restore them atomically in a single `setState` call to prevent a render between document and selection restore.""",

]

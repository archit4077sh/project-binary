"""
snippets/q_react.py — BATCH 5: 28 brand-new React questions
Zero overlap with batch1, batch2, batch3, or batch4 archives.
"""

Q_REACT = [

"""**Task (Code Generation):**
Build a `useControllable<T>` hook that supports both controlled and uncontrolled usage of a prop:

```ts
// Uncontrolled (manages its own state):
<Accordion />

// Controlled (caller manages state):
<Accordion open={isOpen} onOpenChange={setIsOpen} />

// Inside Accordion:
const [open, setOpen] = useControllable({
  value: props.open,
  defaultValue: false,
  onChange: props.onOpenChange,
});
```

Show: detecting controlled mode (`props.value !== undefined`), the TypeScript discriminated union for controlled vs uncontrolled prop types, a dev-mode warning when switching between controlled and uncontrolled (React's own warning pattern), and the `onChange` callback that is always called regardless of controlled/uncontrolled mode.""",

"""**Debug Scenario:**
A form using React Hook Form with Zod validation shows no errors in the UI, but `formState.isValid` is `false`. The submit button that's `disabled={!isValid}` is permanently disabled:

```ts
const { formState: { isValid, errors } } = useForm({
  resolver: zodResolver(schema),
  mode: 'onChange',
});
// errors: {} (empty) but isValid: false
```

The form has a field with `z.string().transform(Number)` — Zod transforms are applied during parsing and the result fails the downstream validator. The issue: `isValid` is `false` because Zod's `output` type after transform doesn't match the form's registered field type.

Show: using `z.coerce.number()` for input-to-number coercion (no transform needed), the difference between Zod `input` and `output` types with RHF, and using `zodResolver`'s `mode: 'async'` vs `mode: 'sync'`.""",

"""**Task (Code Generation):**
Implement a `<TreeView>` component with keyboard navigation and accessibility:

```tsx
<TreeView
  data={fileTree}
  renderNode={(node, { isExpanded, isSelected, level }) => (
    <FileNode node={node} expanded={isExpanded} level={level} />
  )}
  onSelect={(node) => openFile(node.path)}
  multiSelect
  defaultExpanded={['src', 'src/components']}
/>
```

Show: ARIA tree widget roles (`role="tree"`, `role="treeitem"`, `aria-expanded`, `aria-selected`, `aria-level`), keyboard navigation (Arrow keys to navigate, Enter/Space to select/expand, Home/End for first/last item), the flat list rendering with indentation (for virtualization compatibility), and the selection model for multi-select with Shift+click and Ctrl+click.""",

"""**Debug Scenario:**
A component uses `useId()` for generating accessible IDs but after a server-side render, the client generates different IDs causing a hydration mismatch:

```ts
const id = useId(); // Server: ':r0:' | Client: ':ra:' — mismatch!
```

Investigation reveals the component tree's insertion order differs between server and client because a CSS-in-JS library injects style tags that wrap the component differently on client.

Show: why `useId()` generates IDs based on the component's position in the React tree, how any tree shape difference between server/client causes mismatch, using `suppressHydrationWarning` as a bandaid, and the real fix: ensuring the client and server render the same component tree structure (move style injection to `<head>` to avoid affecting component order).""",

"""**Task (Code Generation):**
Build a `useResizable` hook for creating resizable panels:

```tsx
const { size, handleProps, isResizing } = useResizable({
  direction: 'horizontal',
  initialSize: 300,
  min: 200,
  max: 600,
  onResizeStart: () => disableTextSelection(),
  onResizeEnd: (finalSize) => saveLayoutPreference(finalSize),
});

<div style={{ width: size }}>
  <PanelContent />
  <div className="resize-handle" {...handleProps} />
</div>
```

Show: `mousedown`/`mousemove`/`mouseup` (and touch equivalents) on `document` during resize, calculating delta from the drag start position, clamping to min/max, cleanup of document listeners on unmount, and a `<ResizablePanel>` composite component that wraps the hook.""",

"""**Debug Scenario:**
A `<Tabs>` component's active tab indicator (a sliding underline) animates correctly on click, but when navigating via keyboard the animation starts from the wrong position — it jumps to position 0 before sliding:

```ts
// Indicator position is calculated from the active tab's offsetLeft
const indicatorLeft = tabs[activeIndex].current.offsetLeft;
// On keyboard nav: focus changes before the tab element fully renders at new position
```

After keyboard navigation changes `activeIndex`, React re-renders, but the tab element's `offsetLeft` is read in a `useEffect` which fires after paint — there's one frame where the indicator renders at the new ref's position in the OLD layout before the ref updates.

Show: using `useLayoutEffect` instead of `useEffect` for synchronous DOM measurement before paint, the `getBoundingClientRect()` approach instead of `offsetLeft` for cross-transform compatibility, and `flushSync` to force synchronous state updates when the animation must start immediately after a state change.""",

"""**Task (Code Generation):**
Implement a `useMediaSession` hook for integrating with the browser's Media Session API:

```ts
useMediaSession({
  metadata: {
    title: track.name,
    artist: track.artist,
    album: track.album,
    artwork: [{ src: track.coverUrl, sizes: '512x512', type: 'image/jpeg' }],
  },
  handlers: {
    play:           () => play(),
    pause:          () => pause(),
    previoustrack:  () => playPrev(),
    nexttrack:      () => playNext(),
    seekto:         ({ seekTime }) => seekTo(seekTime),
    seekbackward:   ({ seekOffset = 10 }) => seekBy(-seekOffset),
    seekforward:    ({ seekOffset = 10 }) => seekBy(seekOffset),
  },
  playbackState: isPlaying ? 'playing' : 'paused',
  positionState: { duration, playbackRate: 1, position: currentTime },
});
```

Show: `navigator.mediaSession` availability check, updating `positionState` on every `timeupdate` event, cleanup of action handlers on unmount, and the PWA `manifest.json` setup for OS media controls on lock screen.""",

"""**Debug Scenario:**
A developer discovers their React app rerenders a parent component every time a child dispatches an event, even though the parent doesn't consume the event data. The architecture uses a custom event bus via context:

```tsx
// Context value contains both `emit` and `on` functions
const EventBusContext = createContext({ emit: () => {}, on: () => {} });
```

The context value is a fresh object on every render — all consumers re-render whenever the provider re-renders. Show: memoizing the context value with `useMemo`, separating the stable (never-changing) `emit`/`on` functions into a separate context from any stateful data, using `useRef` for the event bus internal state (doesn't trigger re-renders), and the `useReducer`/`dispatch` pattern as an alternative that provides a stable dispatch reference.""",

"""**Task (Code Generation):**
Build a `useVirtualScroll` hook from scratch for large lists:

```ts
const { virtualItems, totalHeight, scrollTo } = useVirtualScroll({
  count: 100000,
  itemHeight: 48,
  containerHeight: 600,
  overscan: 5,
});

<div style={{ height: 600, overflow: 'auto' }} ref={scrollRef}>
  <div style={{ height: totalHeight, position: 'relative' }}>
    {virtualItems.map(({ index, start }) => (
      <div style={{ position: 'absolute', top: start, height: 48 }} key={index}>
        <Row data={items[index]} />
      </div>
    ))}
  </div>
</div>
```

Show: computing the visible range from `scrollTop` and `containerHeight`, the `overscan` buffer above and below, the `scrollTo(index)` function that calls `scrollRef.current.scrollTop = index * itemHeight`, throttling scroll events with `requestAnimationFrame`, and variable-height extension using a height measurement cache.""",

"""**Debug Scenario:**
A `<DatePicker>` component built with Floating UI (Popper) positions the calendar dropdown correctly on first open, but after the user scrolls the page, the dropdown stays fixed at its initial position instead of following the trigger element:

```ts
const { floatingStyles } = useFloating({
  placement: 'bottom-start',
  // Missing update mechanism
});
```

Floating UI computes position once. Scroll or resize events aren't connected. Show: adding `autoUpdate` from Floating UI (`const cleanup = autoUpdate(reference, floating, update)`) that continuously repositions on scroll/resize, returning the cleanup in `useEffect`, and the `whileElementsMounted` option in `useFloating` that handles autoUpdate lifecycle automatically.""",

"""**Task (Code Generation):**
Implement a `useFocusTrap` hook for modal accessibility:

```ts
const { containerProps, activate, deactivate } = useFocusTrap({
  active: isModalOpen,
  initialFocus: 'first', // or CSS selector or ref
  returnFocus: true,      // restore focus to trigger on deactivate
  escapeDeactivates: true,
});

<div {...containerProps} role="dialog" aria-modal="true">
  <ModalContent />
</div>
```

Show: collecting all focusable elements inside the container (`a[href]`, `button`, `input`, `select`, `textarea`, `[tabindex]`), Tab/Shift+Tab cycle wrapping logic, saving and restoring the focused element before/after, the `Escape` key handler, and why `aria-modal="true"` alone is insufficient without a JavaScript focus trap.""",

"""**Debug Scenario:**
A developer wraps a third-party chart component in `React.memo`. In performance testing, the chart STILL re-renders on every parent update even though none of its props changed.

```tsx
const MemoChart = React.memo(ThirdPartyChart);
```

Investigation shows `ThirdPartyChart` internally uses `useContext(ThemeContext)` — `React.memo` prevents re-renders from parent props, but NOT from context changes. The theme context changes on every render because the provider value is an inline object.

Show: memoizing the context value in the provider, the difference between `React.memo` (blocks parent prop-driven re-renders) and context subscriptions (always re-render on context change), and using `useContextSelector` from `use-context-selector` to subscribe to only the relevant portion of the theme context.""",

"""**Task (Code Generation):**
Build a `<AnimatedCounter>` component that smoothly transitions between numeric values:

```tsx
<AnimatedCounter
  value={revenue}
  duration={1200}
  easing="easeOutExpo"
  formatter={(n) => `$${n.toLocaleString()}`}
  decimals={2}
/>
// Animates from old value to new value over 1.2 seconds
```

Show: calculating the interpolated value using `requestAnimationFrame`, the easing function library (implement `easeOutExpo`: `1 - Math.pow(2, -10 * progress)`) or using the Web Animations API, handling rapid value changes (cancel previous animation, start from current animated value), `prefers-reduced-motion` fallback (jump directly to final value), and the `useRef` for the animation frame ID cleanup.""",

"""**Debug Scenario:**
A Next.js page with a large number of `<Link>` components to server actions freezes the browser tab when the page first loads. React DevTools shows a massive render tree in the initial commit.

The page renders 2,000 product cards, each with a `<Link>` to the product detail page. The `<Link>` component prefetches each route on mount, creating 2,000 simultaneous prefetch requests.

Show: using `<Link prefetch={false}>` on non-critical items, implementing intent-based prefetch (prefetch only on `mouseenter`), batching visible links with `IntersectionObserver` so only links near the viewport are prefetched, and the `router.prefetch` API called imperatively inside a `mouseover` handler instead of declaratively.""",

"""**Task (Code Generation):**
Implement a `useCombobox` hook for an accessible autocomplete/combobox widget:

```ts
const {
  inputProps,
  listboxProps,
  getOptionProps,
  isOpen,
  activeIndex,
  selectedItem,
} = useCombobox({
  items,
  itemToString: (item) => item?.label ?? '',
  onSelectedItemChange: ({ selectedItem }) => onChange(selectedItem),
  filterItems: (items, inputValue) =>
    items.filter(i => i.label.toLowerCase().includes(inputValue.toLowerCase())),
});
```

Show: ARIA combobox pattern (input + listbox), keyboard handling (ArrowDown/Up navigate options, Enter selects, Escape closes, Tab transfers focus), `aria-activedescendant` pointing to the active option, and accessibility requirements from ARIA 1.2 combobox spec.""",

"""**Debug Scenario:**
A React component fetches data on a button click and stores it in local state. The component unmounts before the fetch completes (user navigates away), causing a warning:

```
Warning: Can't perform a React state update on an unmounted component.
```

```ts
async function handleFetch() {
  const data = await fetch('/api/data').then(r => r.json());
  setData(data); // component already unmounted!
}
```

Show: the `AbortController` pattern to cancel the fetch on unmount, the `useEffect` cleanup that calls `controller.abort()`, an `isMounted` ref as a guard for non-fetch async operations that can't be aborted, and why React 18 removed this specific warning (it's now only a warning for `setState` on committed-then-unmounted trees).""",

"""**Task (Code Generation):**
Build a `useGestureRecognizer` hook for touch gestures:

```ts
const { gestureProps } = useGestureRecognizer({
  onSwipeLeft:  () => nextSlide(),
  onSwipeRight: () => prevSlide(),
  onSwipeUp:    () => closeDrawer(),
  onPinchZoom:  ({ scale }) => setZoom(zoom * scale),
  onLongPress:  () => showContextMenu(),
  swipeThreshold: 50,   // min px to qualify as swipe
  longPressDuration: 600,
});

<div {...gestureProps}>
  <Carousel />
</div>
```

Show: tracking `touchstart`/`touchmove`/`touchend` coordinates, computing swipe direction and distance, two-finger distance delta for pinch zoom, `clearTimeout` on touchend to cancel long press, and `touch-action: none` CSS to prevent browser's default swipe behaviors.""",

"""**Debug Scenario:**
A React app's `<SearchInput>` uses controlled state but feels laggy — there's a visible delay between keystroke and character appearing in the input:

```tsx
<input value={query} onChange={e => setQuery(e.target.value)} />
```

The `onChange` → `setState` → re-render cycle is slow because it triggers a heavy re-render of the entire search results tree. 

Show: decoupling the input state from the results state (input is uncontrolled or has its own local state, debounced value drives results), `startTransition` wrapping the results update (not the input update), replacing the controlled input with `useRef` + `defaultValue` to make the input natively responsive, and using `useDeferredValue(query)` for showing stale results while new ones load.""",

"""**Task (Code Generation):**
Implement a `useIntersectionObserverList` hook that tracks which items in a list are visible:

```ts
const { visibleIds, registerRef } = useIntersectionObserverList({
  threshold: 0.5,     // consider visible when 50% is in viewport
  rootMargin: '0px',
});

{items.map(item => (
  <div key={item.id} ref={registerRef(item.id)}>
    <ArticleCard article={item} isVisible={visibleIds.has(item.id)} />
  </div>
))}
```

Show: a single `IntersectionObserver` instance observing all registered elements (not one observer per item), the `Map<Element, string>` for element-to-id lookup, the `Set<string>` of currently visible IDs in state, `registerRef(id)` returning a stable `RefCallback`, and cleanup of the observer when the last element is unregistered.""",

"""**Debug Scenario:**
A developer uses `useEffect(() => { ... }, [])` (empty deps) to register a global `keydown` handler. The handler references a state variable `activeTab` from the closure, but always reads the initial value (stale closure):

```ts
const [activeTab, setActiveTab] = useState(0);
useEffect(() => {
  window.addEventListener('keydown', (e) => {
    handleKeyForTab(activeTab); // always 0 — stale closure
  });
}, []);
```

Show: using `useRef` to hold the current `activeTab` value (updated in a separate `useEffect([activeTab])` that sets `ref.current = activeTab`), then reading `ref.current` inside the keydown handler, the alternative of using a functional updater `setActiveTab(prev => ...)` to avoid needing to read current value, and adding `activeTab` to the deps array with a corresponding `removeEventListener` cleanup.""",

"""**Task (Code Generation):**
Build a `<PrintTemplate>` system that renders a print-optimized version of a component:

```tsx
const { print, isPrinting } = usePrint({
  documentTitle: 'Invoice #1234',
  onBeforePrint: () => analytics.track('invoice_printed'),
  onAfterPrint: () => setIsPrinting(false),
});

// Main view:
<InvoiceView invoice={invoice} />
<button onClick={print}>Print Invoice</button>

// Print-only DOM:
<PrintTemplate isPrinting={isPrinting}>
  <InvoicePrintLayout invoice={invoice} />
</PrintTemplate>
```

Show: CSS `@media print` for showing/hiding print-only elements, `window.print()` wrapped with React lifecycle, a Portal that injects print content into `document.body`, and the `@page` CSS at-rule for print margins and page size.""",

"""**Debug Scenario:**
A `<Tooltip>` component uses `React.cloneElement` to attach event props to its child:

```tsx
function Tooltip({ children, content }) {
  return React.cloneElement(children, {
    onMouseEnter: () => show(),
    onMouseLeave: () => hide(),
    'aria-describedby': tooltipId,
  });
}
```

When the child component already has an `onMouseEnter` prop, `cloneElement` overwrites it — the child's original handler is lost.

Show: merging event handlers instead of overwriting them (call both the existing and the new handler), the render props pattern as an alternative to `cloneElement`, using the Slot pattern (`asChild` prop) from Radix UI, and TypeScript narrowing to ensure `children` is a single React element (not an array or string).""",

"""**Task (Code Generation):**
Implement a `useReorder` hook for drag-and-drop list reordering without external libraries:

```ts
const { items, reorderedItems, dragHandleProps, getItemProps } = useReorder({
  initialItems: todos,
  onReorder: (newOrder) => saveTodoOrder(newOrder),
});

{reorderedItems.map((item, i) => (
  <li key={item.id} {...getItemProps(i)}>
    <span {...dragHandleProps(i)}>⠿</span>
    {item.title}
  </li>
))}
```

Show: tracking the dragged item index and current hover index, swapping items in a local draft copy during drag, committing to state on `dragend`, CSS `cursor: grab`/`grabbing` on the handle, and HTML5 drag-and-drop API events (`dragstart`, `dragover`, `dragend`, `drop`).""",

"""**Debug Scenario:**
A React app wraps API calls in a custom `useApi` hook. During tests with `@testing-library/react`, the component renders but never shows the loaded data — it stays in the loading state:

```ts
// useApi.ts:
function useApi(url) {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch(url).then(r => r.json()).then(setData);
  }, [url]);
  return data;
}
```

Tests mock `fetch` using `jest.fn()` but `fetch` isn't globally available in JSDOM — `jest.fn()` replaces the global but `fetch` wasn't defined (JSDOM < 15 doesn't include `fetch`). The mock call never triggers.

Show: using `whatwg-fetch` polyfill in test setup, or `global.fetch = jest.fn(...)` before tests, `msw` as the standard solution (intercepts at the network level regardless of how fetch is called), and `waitFor(() => expect(screen.getByText('data')).toBeInTheDocument())` to handle async rendering.""",

"""**Task (Code Generation):**
Build a `createReducerContext` factory for creating typed context/reducer pairs:

```ts
const { Provider, useDispatch, useSelector } = createReducerContext({
  initialState: { count: 0, items: [] as string[] },
  reducers: {
    increment: (state) => ({ ...state, count: state.count + 1 }),
    addItem: (state, item: string) => ({ ...state, items: [...state.items, item] }),
    reset: () => ({ count: 0, items: [] }),
  },
});

// Usage:
const count = useSelector(s => s.count);
const dispatch = useDispatch();
dispatch.increment();
dispatch.addItem('hello');
```

Show: the factory creating a Context, a Provider component, the typed `useDispatch` that returns an object of type-safe action creators (not a raw dispatch function), and `useSelector` with a memoized comparator to prevent unnecessary re-renders.""",

"""**Debug Scenario:**
A multi-page form stores data in React state. When the user navigates to page 2 and then uses the browser Back button to go to page 1, the form data from page 1 is reset to initial values.

The form state is stored in each page component's local `useState` — navigating away unmounts the component, destroying the state. Show: lifting form state to the router level using `useLocation().state` (React Router's state passing), using a persistent global store (Zustand/Redux) for multi-step form data, or using `sessionStorage` as a persistence layer with a `useSessionStorage` hook that rehydrates on mount.""",

"""**Task (Code Generation):**
Implement a `<ContextMenu>` component that appears at the cursor position on right-click:

```tsx
<ContextMenu
  items={[
    { label: 'Edit', icon: <EditIcon />, onClick: handleEdit },
    { label: 'Delete', icon: <TrashIcon />, onClick: handleDelete, destructive: true },
    { type: 'separator' },
    { label: 'Share', icon: <ShareIcon />, submenu: shareOptions },
  ]}
>
  <div className="card">{/* Right-click on this */}</div>
</ContextMenu>
```

Show: `onContextMenu` handler that calls `preventDefault()` and stores cursor position, rendering the menu in a Portal positioned at `{ x, y }`, closing on `click` outside or `Escape`, clipping to viewport bounds (menu doesn't go off-screen), keyboard navigation (ArrowDown/Up), and submenu hover activation with a delay (prevent accidental submenu close when moving diagonally).""",

"""**Debug Scenario:**
A developer creates a custom `useThrottle` hook and uses it in a scroll handler. Under heavy scroll events, the throttled callback sometimes fires AFTER the component unmounts, setting state on a stale component:

```ts
function useThrottle(fn, delay) {
  const lastCall = useRef(0);
  return useCallback((...args) => {
    if (Date.now() - lastCall.current > delay) {
      lastCall.current = Date.now();
      fn(...args);
    }
  }, [fn, delay]);
}
```

If `fn` is `setState`, calling it after unmount causes the old "can't update unmounted" warning. Show: using an `isMountedRef` guard inside `fn`, the modern React 18 approach (this warning is suppressed for async operations), and using `useCallback` to ensure `fn` is always the latest closure value (not stale), with `useRef` for `fn` to avoid recreating the throttle on every render.""",

]

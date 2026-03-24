"""
snippets/q_react.py — BATCH 6: 56 brand-new React questions
Zero overlap with batches 1-5 archives.
Mix of code-generation and debugging tasks.
"""

Q_REACT = [

# ── Code Generation ──────────────────────────────────────────────────────────

"""**Task (Code Generation):**
Build a `useWhyDidYouRender` development hook that logs which props/state changed between renders:

```ts
function ProductCard({ product, onBuy }: Props) {
  useWhyDidYouRender('ProductCard', { product, onBuy });
  return <div>{product.name}</div>;
}
// Console: [ProductCard] Re-render because: onBuy changed (function reference)
```

Show: comparing previous and current props using `Object.keys`, detecting reference changes vs value changes, logging the diff with a readable format, disabling in production via `process.env.NODE_ENV`, and identifying when a parent passes a new function literal on every render vs a memoized callback.""",

"""**Task (Code Generation):**
Implement a `createFormSchema` builder with field-level async validators:

```ts
const loginSchema = createFormSchema({
  email: field(z.string().email())
    .asyncValidate(async (val) => {
      const exists = await api.checkEmailExists(val);
      if (!exists) return 'No account with this email';
    })
    .debounce(400),
  password: field(z.string().min(8)),
});

const { register, handleSubmit, errors } = useForm({ schema: loginSchema });
```

Show: running Zod sync validation first and skipping async if sync fails, cancelling pending async validation when the value changes (AbortController), setting `isValidating` state per-field while async runs, and integrating with React Hook Form's `resolver` option.""",

"""**Task (Code Generation):**
Build a `useIntersectionState<T>` hook that maps DOM visibility to typed state:

```ts
const { ref, state } = useIntersectionState<'below' | 'visible' | 'above'>({
  map: (entry) => {
    if (!entry.isIntersecting) return entry.boundingClientRect.top > 0 ? 'below' : 'above';
    return 'visible';
  },
  threshold: [0, 0.5, 1],
  rootMargin: '0px 0px -100px 0px',
});

<section ref={ref} className={`section section--${state}`}>...</section>
```

Show: the `IntersectionObserver` setup, attaching it to the `ref`, the typed `map` function that converts an `IntersectionObserverEntry` to a custom state value, cleanup on unmount, and a `useSectionScrollSpy` built on top of it for a table-of-contents highlighter.""",

"""**Task (Code Generation):**
Implement a `<VirtualGrid>` component for 2D virtualization of large datasets:

```tsx
<VirtualGrid
  columnCount={COLS}
  rowCount={ROWS}
  columnWidth={200}
  rowHeight={150}
  width={800}
  height={600}
  renderCell={({ rowIndex, columnIndex, style }) => (
    <div style={style}>
      <ProductTile product={data[rowIndex * COLS + columnIndex]} />
    </div>
  )}
/>
```

Show: computing the visible row/column range from `scrollTop`/`scrollLeft`, rendering only visible cells, absolute positioning each cell via `style.top/left`, an overscan of 2 rows/columns to prevent flicker during fast scrolling, and handling variable column widths with a cumulative offset array.""",

"""**Task (Code Generation):**
Build a `useResizeObserver` hook with debounced dimension reporting:

```ts
const { ref, width, height, entries } = useResizeObserver<HTMLDivElement>({
  debounce: 100,
  box: 'border-box',
  onResize: ({ width, height }) => {
    if (width < 600) setLayout('compact');
    else setLayout('full');
  },
});
```

Show: `ResizeObserver` setup and cleanup, the debounce implementation using `useRef` for the timer, accessing `contentBoxSize` vs `borderBoxSize` from the entry, and the CSS container query equivalent (for when JS measurement isn't needed).""",

"""**Task (Code Generation):**
Implement a `useDragAndDrop` hook for sortable lists without external libraries:

```ts
const { listRef, dragHandleProps, dropTargetProps, orderedItems } =
  useDragAndDrop<Task>({
    items: tasks,
    idKey: 'id',
    onReorder: (reorderedIds) => updateTaskOrder(reorderedIds),
    animation: 'spring',
  });
```

Show: tracking `dragstart`, `dragover`, `drop`, and `dragend` events, computing the reordered array by swapping dragged item into the hovered slot, CSS `will-change: transform` + `transition` for the animation, keyboard-accessible drag (Space to pick up, arrow keys to move, Space to drop), and touch event support via `touchstart`/`touchmove`/`touchend`.""",

"""**Task (Code Generation):**
Build a `useKeyboardShortcuts` hook with conflict detection:

```ts
useKeyboardShortcuts([
  { key: 'k', meta: true, action: () => openCommandPalette(), description: 'Open command palette' },
  { key: 's', meta: true, action: () => saveDocument(), description: 'Save document' },
  { key: 'Escape', action: () => closeModal(), description: 'Close modal' },
  { key: '/', action: () => focusSearch(), when: () => !isTyping, description: 'Focus search' },
]);
```

Show: attaching a single `keydown` listener to `window`, matching key combos (handling `meta` vs `ctrl` cross-platform), the `when` guard function, conflict detection (throw in development if two shortcuts share the same combo), and a `useKeyboardShortcutHelp()` hook that returns all registered shortcuts for a help dialog.""",

"""**Task (Code Generation):**
Implement a `useTimeline` hook for building animated step-by-step walkthroughs:

```ts
const { step, progress, goTo, next, prev, isFirst, isLast, play, pause } =
  useTimeline({
    steps: tourSteps,
    autoPlay: false,
    stepDuration: 4000,
    onComplete: () => markTourComplete(),
  });

<TourOverlay step={step} progress={progress} />
```

Show: the interval-based auto-advance, per-step duration override, smooth `progress` percentage (updated every 50ms within a step), pause/resume by clearing/restarting the interval, and persistence of "last step seen" in localStorage for resuming across page loads.""",

"""**Task (Code Generation):**
Build a `<Portal>` component that renders into named portal containers placed elsewhere in the DOM:

```tsx
<PortalTarget name="notifications" />
<PortalTarget name="modals" className="modal-layer" />

<Portal target="notifications">
  <Toast message="Saved!" />
</Portal>

<Portal target="modals">
  <ConfirmDialog onConfirm={deleteUser} />
</Portal>
```

Show: managing a `Map<string, HTMLElement>` registry for portal targets, the `PortalTarget` component registering itself on mount and unregistering on unmount, the `Portal` component using `createPortal` to the registered target, and a `PortalContext` that provides the registry without prop-drilling.""",

"""**Task (Code Generation):**
Implement a `useChunkedDataLoader<T>` hook for processing large datasets in chunks:

```ts
const { processed, progress, isProcessing, cancel } = useChunkedDataLoader({
  data: rawDataArray,
  chunkSize: 1000,
  processor: async (chunk) => chunk.map(transformItem),
  onChunkComplete: (chunk, pct) => setPartialResults(prev => [...prev, ...chunk]),
});
```

Show: processing each chunk in a `requestIdleCallback` or `setTimeout(0)` to yield to the browser, the `cancel` function using an `isCancelled` ref, UI progress percentage, and an `AbortSignal` version that cancels if the component unmounts.""",

"""**Task (Code Generation):**
Build a `useDeepPartialState<T>` hook for granular nested state updates without spreading:

```ts
const { state, setPath, reset } = useDeepPartialState<UserSettings>({
  theme: { mode: 'light', accent: '#4f46e5' },
  notifications: { email: true, push: false },
  privacy: { analytics: true, ads: false },
});

setPath('theme.accent', '#e11d48');
setPath('notifications.push', true);
```

Show: path parsing (`'theme.accent'` → `['theme', 'accent']`), immutable nested update using `structuredClone`, TypeScript `DeepPartial<T>` type, `setPath` generics ensuring the value type matches the path, and `reset(partial)` that merges a partial object into the initial state.""",

"""**Task (Code Generation):**
Implement a `useSearchableSortableList<T>` hook combining search, sort, and pagination:

```ts
const {
  items,
  query, setQuery,
  sortKey, sortDir, setSort,
  page, setPage, totalPages,
} = useSearchableSortableList({
  data: products,
  searchableFields: ['name', 'description', 'tags'],
  defaultSort: { key: 'name', dir: 'asc' },
  pageSize: 20,
});
```

Show: fast multi-field search normalizing to lowercase, stable sort with tie-break by index, resetting to page 1 when query or sort changes, memoizing filtered/sorted arrays to avoid recomputation on pagination change, and a `useMemo` dependency fingerprint to avoid stale data.""",

"""**Task (Code Generation):**
Build a `useStateMachine<States, Events>` hook for typed UI state machines:

```ts
const { state, send, matches } = useStateMachine<
  'idle' | 'loading' | 'success' | 'error',
  { type: 'SUBMIT' } | { type: 'RESOLVE'; data: User } | { type: 'REJECT'; error: string } | { type: 'RESET' }
>({
  initial: 'idle',
  transitions: {
    idle:    { SUBMIT: 'loading' },
    loading: { RESOLVE: 'success', REJECT: 'error' },
    success: { RESET: 'idle' },
    error:   { RESET: 'idle', SUBMIT: 'loading' },
  },
  onTransition: (from, to, event) => analytics.track(`state_${to}`),
});

send({ type: 'SUBMIT' });
if (matches('loading')) return <Spinner />;
```

Show: invalid transitions raising a console.warn in development, context stored alongside state, TypeScript narrowing of `event` type based on allowed transitions, and compare to `xstate/fsm`.""",

"""**Task (Code Generation):**
Implement a `withRetry<T>` HOC that adds automatic retry behavior to data-fetching components:

```tsx
const ResilientUserProfile = withRetry(UserProfile, {
  maxRetries: 3,
  backoff: 'exponential',
  shouldRetry: (error) => error.code !== 401,
  fallback: <ErrorFallback />,
  onMaxRetriesReached: (error) => logger.error('Profile load failed', error),
});

<ResilientUserProfile userId="u1" />
```

Show: wrapping the component in an error boundary, tracking retry count in a ref, scheduling the next render attempt with `setTimeout`, passing `retryCount` and `lastError` as additional props to the wrapped component, and resetting state when `userId` prop changes.""",

"""**Task (Code Generation):**
Build a `useScrollRestoration` hook that saves and restores scroll positions per route:

```ts
function ProductList() {
  const containerRef = useScrollRestoration('product-list');
  return (
    <div ref={containerRef} style={{ overflowY: 'auto', height: '100vh' }}>
      {products.map(p => <ProductCard key={p.id} {...p} />)}
    </div>
  );
}
```

Show: saving `scrollTop` to `sessionStorage` on scroll (debounced at 200ms), restoring it on mount via `useLayoutEffect`, using the route path + component key as the storage key, and handling the case where the content is not yet loaded (wait for children to render before restoring).""",

"""**Task (Code Generation):**
Implement a `useMultiSelect<T>` hook for handling complex multi-selection UX:

```ts
const {
  selectedIds,
  toggleSelect,
  selectAll,
  deselectAll,
  isSelected,
  selectedItems,
  rangeSelect,  // shift-click range
} = useMultiSelect<Product>({
  items: products,
  idKey: 'id',
  onSelectionChange: (ids) => setSelectedForBulkAction(ids),
});
```

Show: shift-click range selection (select all items between last clicked and current), Ctrl/Cmd+A for select-all, the `isSelected(id)` predicate, deriving `selectedItems` from the `Set<string>` of IDs without filtering the full array on every render, and keyboard-accessible selection with `aria-selected` attributes.""",

"""**Task (Code Generation):**
Build a `useAbortableFetch` hook wrapping `fetch` with automatic cancellation:

```ts
const { data, error, loading, abort } = useAbortableFetch<Order[]>({
  url: `/api/orders?status=${filter}`,
  deps: [filter],
  transform: (raw) => raw.orders.map(normalizeOrder),
  onSuccess: (orders) => updateOrderCache(orders),
  onError: (err) => {
    if (err.name !== 'AbortError') reportError(err);
  },
});
```

Show: creating an `AbortController` in effect, passing `controller.signal` to `fetch`, aborting on `deps` change or unmount, distinguishing `AbortError` from real errors, and the `retryOnNetworkError` option that uses exponential backoff before giving up.""",

"""**Task (Code Generation):**
Implement a `useModalStack` hook for layered modal management:

```ts
const { openModal, closeModal, closeAll, stack } = useModalStack();

openModal(<ConfirmDialog onConfirm={() => { closeModal(); deleteItem(); }} />);
// Multiple modals can stack:
openModal(<DetailsModal itemId={id} />);
// stack.length === 2

// Press Escape → closes the top-most modal
```

Show: the `stack` as an array of React elements, pushing/popping the stack on open/close, globally listening for `Escape` key (only closes the top-most modal), `aria-modal="true"` on the top-most modal, trapping focus inside the active modal (Tab/Shift+Tab cycle within it), and `data-modal-level` attribute for CSS stacking.""",

"""**Task (Code Generation):**
Build a `useAnimatedCounter` hook that smoothly animates a numeric value change:

```ts
const displayValue = useAnimatedCounter({
  value: totalRevenue,      // e.g. changes from 98,000 to 125,000
  duration: 800,
  easing: 'easeOutExpo',
  format: (v) => `$${Math.round(v).toLocaleString()}`,
});

<span className="metric">{displayValue}</span>
// Animates: "$98,000" → "$125,000" over 800ms
```

Show: `requestAnimationFrame` loop computing the interpolated value, easing functions as pure math functions (`value + (target - value) * easing(progress)`), aborting the animation when the component unmounts, restarting the animation from the current display value (not the initial) when target changes mid-animation, and the `spring` easing option using an overdamping equation.""",

"""**Task (Code Generation):**
Implement a `useCommandPalette` hook for building command-palette interfaces (like VS Code's Cmd+K):

```ts
const { isOpen, query, setQuery, results, selectedIndex, selectResult } =
  useCommandPalette({
    commands: registeredCommands,
    fuzzySearch: true,
    recentCommands: 5,   // show 5 most recent commands at top when query is empty
    onSelect: (cmd) => cmd.handler(),
  });
```

Show: fuzzy matching (rank commands by character subsequence match score), scoring algorithm (consecutive character bonuses, start-of-word bonuses), `useHotkeys`-style `Ctrl+K`/`Cmd+K` global listener to open/close, arrow key navigation with `selectedIndex`, and `useDebouncedValue(query, 100)` for search performance.""",

"""**Task (Code Generation):**
Build a `useSharedWorker` hook for sharing state across multiple browser tabs via SharedWorker:

```ts
const { state, dispatch } = useSharedWorker<AppState, AppAction>({
  worker: '/workers/shared-app.js',
  onMessage: (msg) => {
    if (msg.type === 'SYNC_STATE') setState(msg.state);
  },
});

// Dispatching from any tab updates state in ALL tabs:
dispatch({ type: 'ADD_TO_CART', item });
```

Show: the SharedWorker JS that maintains state and broadcasts to all connected ports, the React hook that connects to the worker via `new SharedWorker(url)`, port message handling, cleanup on unmount (`port.close()`), and a `BroadcastChannel` fallback when SharedWorker isn't supported.""",

"""**Task (Code Generation):**
Implement a `useMediaSession` hook for controlling background media playback via OS media keys:

```ts
useMediaSession({
  title: track.name,
  artist: track.artist,
  album: track.album,
  artwork: [{ src: track.coverUrl, sizes: '512x512', type: 'image/jpeg' }],
  handlers: {
    play:         () => audioRef.current?.play(),
    pause:        () => audioRef.current?.pause(),
    previoustrack: playPrev,
    nexttrack:    playNext,
    seekto:       (details) => { audioRef.current!.currentTime = details.seekTime!; },
  },
});
```

Show: setting `navigator.mediaSession.metadata`, registering action handlers with `navigator.mediaSession.setActionHandler`, the `playbackState` update (`'playing'` / `'paused'` / `'none'`), cleanup via `setActionHandler(action, null)` on unmount, and the `positionState` update for progress bar sync in the OS media controls.""",

"""**Task (Code Generation):**
Build a `useSmartTooltip` hook that positions a tooltip relative to its trigger, adjusting for viewport overflow:

```ts
const { triggerRef, tooltipRef, position, isOpen, open, close } =
  useSmartTooltip({
    placement: 'top',         // preferred placement
    fallbackPlacements: ['bottom', 'right', 'left'],
    offset: 8,
    showDelay: 300,
    hideDelay: 100,
  });

<button ref={triggerRef} onMouseEnter={open} onMouseLeave={close}>?</button>
<div ref={tooltipRef} style={position.styles}>Tooltip content</div>
```

Show: measuring trigger rect and tooltip rect, checking if preferred placement overflows the viewport, trying fallback placements in order, computing `top`/`left` CSS values from the chosen placement + offset, and updating position on window resize.""",

"""**Task (Code Generation):**
Implement a `useContainerQuery` hook for CSS container-query-like behaviour in JS:

```ts
const { containerRef, breakpoint } = useContainerQuery<HTMLDivElement>({
  breakpoints: {
    sm: 400,
    md: 640,
    lg: 960,
    xl: 1200,
  },
});

const cardCols = { sm: 1, md: 2, lg: 3, xl: 4 }[breakpoint] ?? 1;
```

Show: `ResizeObserver` on the container to get its width, computing the breakpoint by finding the largest breakpoint that fits, returning both the string breakpoint name and the raw number, and the `@container` CSS equivalent (pure CSS solution that doesn't need the hook for styling purposes).""",

"""**Task (Code Generation):**
Build a `useWebShare` hook wrapping the Web Share API with a clipboard fallback:

```ts
const { share, canShare, isSharing } = useWebShare({
  data: {
    title: article.title,
    text: article.excerpt,
    url: window.location.href,
  },
  onSuccess: () => showToast('Shared!'),
  onError: (err) => console.warn('Share failed', err),
  clipboardFallback: true,   // copy URL to clipboard if Web Share unavailable
});

<button onClick={share}>Share</button>
```

Show: `navigator.canShare(data)` check, `navigator.share(data)` async call, clipboard fallback using `navigator.clipboard.writeText(url)`, the `usePermission('clipboard-write')` status check, and an `isSharing` flag that prevents double-clicks.""",

"""**Task (Code Generation):**
Implement a `createSelectableContext<T>` factory for performance-optimal context:

```ts
const { Provider, useSelector } = createSelectableContext<AppState>();

// Only re-renders when the selected slice changes:
const username = useSelector(state => state.user.name);
const count    = useSelector(state => state.cart.itemCount);
```

Show: the implementation using `useRef` to hold the full state, a `Set` of subscriber functions (each selector + re-render trigger), calling subscribers only when their selected slice changes (using `Object.is`), the `Provider` wrapping `children` with the store ref and subscriber set in a non-rendering context value, and comparison to `use-context-selector`.""",

"""**Task (Code Generation):**
Build a `useTranslationEditor` hook for in-place translation editing:

```ts
const { t, isEditing, toggleEdit, pendingChanges, save } =
  useTranslationEditor({
    locale: 'en',
    namespace: 'checkout',
    onSave: (changes) => api.saveTranslations(changes),
  });

// In translateable components:
<p>{t('order.confirm', { orderId })}</p>
// In editing mode: renders an inline input for translators
```

Show: overriding the `t` function to render `<TranslationSlot key={key} value={value} onChange={...} />` in edit mode, tracking all changed translation keys in a `Map`, the `save` function posting only changed keys, and role-based access (only users with `can: 'edit-translations'` permission can toggle edit mode).""",

# ── Debugging ─────────────────────────────────────────────────────────────────

"""**Debug Scenario:**
A React component using `React.memo` is still re-rendering on every parent render despite props not changing:

```tsx
const ExpensiveChild = React.memo(({ onClick }: { onClick: () => void }) => {
  console.log('child render');
  return <button onClick={onClick}>Click</button>;
});

function Parent() {
  const [count, setCount] = useState(0);
  return (
    <>
      <ExpensiveChild onClick={() => setCount(c => c + 1)} />
    </>
  );
}
```

`onClick={() => setCount(...)}` creates a new function reference on every parent render — memo sees a new `onClick` every time. Show: wrapping `onClick` with `useCallback(() => setCount(c => c + 1), [])` to stabilize it, verifying with `useWhyDidYouRender`, and the `React.memo` custom comparator as an alternative.""",

"""**Debug Scenario:**
A form built with uncontrolled inputs and `useRef` doesn't reflect the default values from an API response:

```tsx
function EditForm({ user }: { user: User }) {
  const emailRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    if (emailRef.current) emailRef.current.value = user.email;
  }, []); // empty deps — only runs once, before user data arrives
}
```

The `useEffect` runs on mount where `user` may still be the initial empty state. Show: adding `user.email` to the dependency array, switching to controlled inputs, or resetting via the `key` prop (`key={user.id}` forces a full remount with correct initial values).""",

"""**Debug Scenario:**
A number input allows entering `-`, `.`, and `e` even though only positive integers should be accepted:

```tsx
<input
  type="number"
  onChange={(e) => {
    const val = parseInt(e.target.value);
    if (val >= 0) setQuantity(val);
  }}
/>
```

`type="number"` allows scientific notation characters during typing. `e.target.value` is an empty string for non-numeric input, so `parseInt('')` is `NaN`. Show: using `type="text"` with `inputmode="numeric"` and `pattern="[0-9]*"`, filtering with `/^[0-9]*$/.test(val)`, or using `onKeyDown` to block non-digit keys.""",

"""**Debug Scenario:**
A component uses `useLayoutEffect` to measure DOM dimensions, but dimensions are `0` on the first render:

```tsx
function AutosizedTextarea() {
  const ref = useRef<HTMLTextAreaElement>(null);
  const [height, setHeight] = useState(0);

  useLayoutEffect(() => {
    setHeight(ref.current!.scrollHeight); // always 0 on first render
  }, []);

  return <textarea ref={ref} style={{ height }} />;
}
```

Initial `height: 0` makes the textarea `0px` tall, so `scrollHeight` is also `0`. Show: using `height: 'auto'` as the initial value to let the browser determine natural height before JS overrides it, reading `scrollHeight` before overriding with state, and `useEffect` vs `useLayoutEffect` timing for visual measurements.""",

"""**Debug Scenario:**
A developer uses `React.cloneElement` to inject props into children, but the child's `ref` is lost:

```tsx
function Wrapper({ children }) {
  const ref = useRef();
  return React.cloneElement(children, { ref }); // overwrites child's existing ref
}
```

`React.cloneElement` replaces the existing `ref` with the new one. Show: using `React.forwardRef` in the child to support forwarding, a `mergeRefs` utility that calls both refs (`(node) => { origRef(node); newRef.current = node; }`), and `useImperativeHandle` for exposing a limited API instead of the raw DOM node.""",

"""**Debug Scenario:**
A `Suspense` boundary shows its fallback every time a user switches between tabs, even though data was already loaded on the first visit:

```tsx
<Suspense fallback={<Spinner />}>
  {activeTab === 'orders' && <OrdersTab />}
  {activeTab === 'profile' && <ProfileTab />}
</Suspense>
```

Conditional rendering with `&&` unmounts the inactive tab — on remount, Suspense re-suspends if `staleTime` is 0. Show: keeping hidden tabs mounted with CSS `hidden` attribute (`<div hidden={activeTab !== 'orders'}>`), using `staleTime: Infinity`, and React 18's `useDeferredValue` for avoiding Suspense fallback on tab switch.""",

"""**Debug Scenario:**
A hook wrapping a third-party subscription API leaks subscriptions:

```tsx
function useStockPrice(symbol: string) {
  const [price, setPrice] = useState(0);
  useEffect(() => {
    const sub = stockFeed.subscribe(symbol, setPrice);
    return sub; // BUG: returning an object, not a function!
  }, [symbol]);
}
```

React's cleanup must be a function. Returning an object causes React to ignore the cleanup — the subscription is never cancelled. Show: returning `() => sub.unsubscribe()`, checking strict mode behavior (effects run twice), and TypeScript typing that would catch this (`() => void`).""",

"""**Debug Scenario:**
React Profiler shows 12ms flamechart spikes for a `<Table>` rendering 200 rows with `formatCurrency` calls:

```tsx
{rows.map(row => (
  <tr key={row.id}>
    <td>{formatCurrency(row.amount, 'USD')}</td>
    <td>{formatCurrency(row.tax, 'USD')}</td>
    <td>{formatCurrency(row.total, 'USD')}</td>
  </tr>
))}
```

`formatCurrency` creates a new `Intl.NumberFormat` on every call (600 per render). Show: caching `Intl.NumberFormat` instances by `locale+currency` in a module-level `Map`, pre-computing formatted values in `useMemo`, virtualizing the table, and `React.memo` on the row with a custom comparator.""",

"""**Debug Scenario:**
React Query `useInfiniteQuery` loads the same page of data after "Load More" is clicked:

```ts
const { data, fetchNextPage } = useInfiniteQuery({
  queryKey: ['items'],
  queryFn: ({ pageParam }) => api.getItems({ page: pageParam }),
  getNextPageParam: (lastPage) => lastPage.nextPage,
  initialPageParam: 1,
});
```

`getNextPageParam` returns correctly but the API ignores the `page` parameter. Show: logging `pageParam` in `queryFn` to verify the received value, checking if `initialPageParam` matches the API's expected first page (0 vs 1), ensuring `getNextPageParam` returns `undefined` (not `null`) when there are no more pages.""",

"""**Debug Scenario:**
A component renders `categories.flatMap(...)` but throws "Objects are not valid as a React child":

```tsx
{categories.flatMap(cat => [
  <h2 key={cat.id}>{cat.name}</h2>,
  ...cat.items.map(item => <ItemCard key={item.id} item={item} />)
])}
```

For some categories, `cat.items` is an object (`{}`) instead of an array — spreading an object into JSX children fails. Show: defensive mapping (`(cat.items ?? []).map(...)`), Zod schema validation ensuring `items` is always an array, and TypeScript strict null checks catching `undefined` access.""",

"""**Debug Scenario:**
`useEffect` reads `document.title` but gets the previous route's title:

```tsx
useEffect(() => {
  analytics.track('page_view', { title: document.title }); // stale title
}, [pathname]);
```

`document.title` is set asynchronously by Next.js after React renders. Show: deferring with `setTimeout(() => analytics.track(..., { title: document.title }), 0)`, using the page title as a prop instead of reading `document.title`, and the Page Router vs App Router difference in title update timing.""",

"""**Debug Scenario:**
A React Native `FlatList` reads stale `filter` state in `renderItem`:

```ts
const [filter, setFilter] = useState('all');

<FlatList
  data={items}
  renderItem={({ item }) => (
    <Item item={item} isVisible={item.type === filter} />
  )}
/>
```

`renderItem` is cached and reuses old closure capturing old `filter`. Show: adding `extraData={filter}` to `FlatList`, using `useCallback(renderItem, [filter])`, and `keyExtractor` with `item.id` for stable reconciliation.""",

"""**Debug Scenario:**
`useTransition` shows `isPending: true` and flickers a loading bar even for nearly instant transitions:

```tsx
const [isPending, startTransition] = useTransition();

function handleTabChange(tab: string) {
  startTransition(() => setActiveTab(tab));
}

{isPending && <LoadingBar />}
```

`isPending` is `true` even for very fast (20ms) transitions. Show: the `useDelayedBoolean(isPending, 300)` pattern — only show loading if pending lasts > 300ms, and the role of Suspense integration with transitions vs using `isPending` alone.""",

"""**Debug Scenario:**
All context consumers re-render when only one part of a combined context changes:

```tsx
const AppContext = createContext({ user: null, theme: 'light', notifications: [] });

function NotificationBell() {
  const { notifications } = useContext(AppContext);
  // Re-renders on every theme or user change!
}
```

All consumers re-render when ANY context value changes. Show: splitting the context into independent domains (`UserContext`, `ThemeContext`, `NotificationsContext`), using `use-context-selector` library for fine-grained subscription, and Zustand subscriptions as an alternative.""",

"""**Debug Scenario:**
React Hook Form shows stale server-set validation errors after the user corrects the field and resubmits:

```tsx
async function onSubmit(data) {
  const serverErrors = await api.validateOnServer(data);
  serverErrors.forEach(e => setError(e.field, { message: e.message }));
}
// Old server error still shows on resubmit after correcting the field
```

`setError` adds errors but RHF doesn't auto-clear server-set errors on field change. Show: calling `clearErrors()` at the start of each `handleSubmit`, using `mode: 'onChange'` to validate on change, and `resetField(name)` to fully reset a field's value and error state.""",

"""**Debug Scenario:**
A multi-step wizard shows empty fields when navigating back to a previous step:

```tsx
function Wizard() {
  const [step, setStep] = useState(1);
  {step === 1 && <PersonalInfoStep />}
  {step === 2 && <AddressStep />}
}
```

Conditional rendering unmounts each step's component, destroying its local `useState`. Show: lifting state to the `Wizard` parent and passing down as props, using `useFormContext()` from React Hook Form (shared form state via context), and CSS `hidden` attribute to keep steps mounted while hiding them visually.""",

"""**Debug Scenario:**
A scroll-to-top button calls `window.scrollTo(0, 0)` but has no effect in a Next.js App Router layout:

```tsx
<button onClick={() => window.scrollTo(0, 0)}>Top</button>
```

Next.js App Router's scrollable element is an inner `<div>` with `overflow: auto`, not `window`. Show: using `document.getElementById('main-content').scrollTo(0, 0)`, a `useScrollContainer` context holding a ref to the scrollable element, and `scroll-behavior: smooth` + `scrollIntoView` as an alternative.""",

"""**Debug Scenario:**
`Array.from({ length: 10 }, ...)` in JSX triggers a React key warning:

```tsx
<div>
  {Array.from({ length: 10 }, (_, i) => (
    <SkeletonCard /> // Warning: each child needs a unique key
  ))}
</div>
```

The `SkeletonCard` components don't have `key` props. Show: adding `key={i}` (index is acceptable for static skeleton lists), the TypeScript type for `Array.from`'s map function, and `[...Array(10)].map((_, i) => <SkeletonCard key={i} />)` as an alternative.""",

"""**Debug Scenario:**
A custom `<Select>` dropdown built with `<ul>` loses keyboard accessibility:

```tsx
<ul role="listbox">
  {options.map(opt => (
    <li key={opt.value} onClick={() => select(opt)}>
      {opt.label}
    </li>
  ))}
</ul>
```

`<li>` elements are not focusable — Tab skips over them. Show: adding `tabIndex={0}` only to the focused option, using `role="option"` + `aria-selected` on each `<li>`, keyboard navigation with `onKeyDown` (arrows move focus, Enter selects, Escape closes), and the `aria-activedescendant` pattern.""",

"""**Debug Scenario:**
A Next.js Server Action always processes initial form values, ignoring user edits:

```tsx
'use server';
async function updateUser(prevState: any, formData: FormData) {
  const name = formData.get('name'); // always gets initial value
  await db.users.update({ name });
}
```

The bug: the `<input>` uses `defaultValue` (uncontrolled) but the Server Action should receive the current value. Show: verifying the form sends data correctly by logging `[...formData.entries()]` in the action, checking that the input `name` attribute matches `formData.get('name')`, and the difference between `value` (controlled) and `defaultValue` (uncontrolled) for Server Actions.""",

"""**Debug Scenario:**
CSS `height: 0` to `height: auto` transition doesn't animate:

```css
.panel { height: 0; overflow: hidden; transition: height 0.3s ease; }
.panel.open { height: auto; }
```

CSS can't interpolate between `0` and `auto`. Show: using `max-height` with a large value, the `interpolate-size: allow-keywords` + `height: calc-size(auto)` modern CSS solution, measuring the actual height in JS to set it explicitly, and the CSS Grid `grid-template-rows: 0fr` → `1fr` trick.""",

"""**Debug Scenario:**
React shows "Cannot update a component while rendering a different component" and the error traces to the function body (not useEffect):

```tsx
function Child({ onMount }) {
  onMount(computedValue); // called during render!
  return <div />;
}
```

`onMount` calls the parent's `setState` synchronously during render. Show: moving the call into `useEffect(() => { onMount(computedValue); }, [])`, and React 18 Strict Mode's double-render detection that surfaces these issues.""",

"""**Debug Scenario:**
A custom hook returns a new object reference on every render, causing infinite `useEffect` re-runs:

```ts
function useUserConfig(userId: string) {
  const config = { endpoint: `/api/users/${userId}`, headers: getHeaders() };
  return config; // new reference every render
}

useEffect(() => {
  fetch(userConfig.endpoint, ...)
}, [userConfig]); // re-fetches every render!
```

Show: memoizing inside the hook with `useMemo(() => ({ endpoint, headers }), [userId])`, passing individual primitive values to `useEffect` instead of an object, and stabilizing `getHeaders()` if it creates new objects on each call.""",

"""**Debug Scenario:**
`React.lazy` throws "Element type is invalid" even though the component exports correctly:

```ts
// feature.tsx:
export const Feature = () => <div>Feature</div>;
export default Feature;

// main.tsx:
const LazyFeature = React.lazy(() => import('./feature'));
// Error: Element type is invalid
```

The module shape may be wrong — `React.lazy` requires a default export. A barrel file may re-export only the named version. Show: ensuring `export default Feature` exists, debugging with `import('./feature').then(m => console.log(m))`, and using `webpackChunkName` comments for named chunks.""",

"""**Debug Scenario:**
A WebSocket hook creates a new connection on every render in React Strict Mode:

```ts
function useWebSocket(url: string) {
  const [socket, setSocket] = useState(() => new WebSocket(url));

  useEffect(() => {
    return () => socket.close();
  }, [socket]);
}
```

`useState` initializer runs twice in Strict Mode — two WebSocket connections are created. Show: moving WebSocket creation into `useEffect` (not `useState`), using `useRef` to hold the WebSocket, and proper cleanup ordering.""",

"""**Debug Scenario:**
Passing `dispatch` deep through a tree causes unnecessary re-renders when unrelated state changes:

```tsx
<OrderForm dispatch={dispatch} total={state.total} />
<CartItems dispatch={dispatch} items={state.items} />
// total change re-renders CartItems; items change re-renders OrderForm
```

Each component receives more state than it needs. Show: selecting only needed state slices via `Context + useContext`, memoizing components with `React.memo` and verifying `items` and `dispatch` references don't change, and the `useContextSelector` pattern for granular context reads.""",

"""**Debug Scenario:**
`useEffect` fires twice in development, causing duplicate API calls that create duplicate records:

```tsx
useEffect(() => {
  api.createSession({ userId }).then(setSession);
}, [userId]);
```

React Strict Mode intentionally runs effects twice (mount → unmount → mount). Show: adding a cleanup function that cancels the first request (`AbortController`), making `createSession` idempotent server-side (same `userId` within a short window returns existing session), and understanding that Strict Mode double-invoke only happens in development.""",

"""**Debug Scenario:**
A tooltip rendered via `createPortal` into `document.body` is being clipped and doesn't appear above a modal:

```tsx
<Tooltip />  // z-index: 1000, portaled to document.body
<Modal />    // z-index: 2000, portaled to document.body
```

The tooltip is actually being rendered inside the modal's DOM subtree (not in `body`), and the modal's `overflow: hidden` clips it. Show: verifying portal destination with DevTools, always portaling tooltips directly to `document.body`, and using `<dialog>` elements (render in the top layer, always above everything including z-index stacks).""",

"""**Debug Scenario:**
A timed animation causes a "Can't perform a React state update on an unmounted component" warning:

```tsx
function CountdownTimer() {
  const [count, setCount] = useState(10);
  setTimeout(() => setCount(c => c - 1), 1000); // fires after unmount!
}
```

`setTimeout` fires after the component unmounts, calling `setCount` on a dead component. Show: using `useEffect` with `clearTimeout` cleanup, using `useRef` to hold the timer ID, and React 18's auto-cleanup improvement (the warning is suppressed in React 18 for class components but the timer is still a memory leak).""",

"""**Debug Scenario:**
A controlled `<input>` in React doesn't let the user type when the value comes from a Redux store:

```tsx
<input
  value={store.query}
  onChange={(e) => dispatch(setQuery(e.target.value))}
/>
```

The input appears frozen. Investigation: `dispatch(setQuery(...))` triggers a re-render, but the Redux reducer has a bug — it returns the previous state unchanged for the `setQuery` action. The controlled input always gets the old value. Show: verifying the reducer actually updates state (`return { ...state, query: action.payload }`), using Redux DevTools to inspect action/state pairs, and the React DevTools "highlight updates" to confirm re-renders.""",

"""**Debug Scenario:**
A `useRef`-based focus trap in a modal doesn't work — Tab still moves focus outside the modal:

```ts
function useFocusTrap(containerRef: RefObject<HTMLElement>) {
  useEffect(() => {
    const focusable = containerRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    // Missing: actual keydown listener to intercept Tab
  }, []);
}
```

Querying focusable elements doesn't trap focus unless there's a `keydown` listener intercepting `Tab`. Show: adding `document.addEventListener('keydown', handleTab)` where `handleTab` moves focus to the first focusable element when Tab is pressed on the last, the `focus-trap-react` library as a battle-tested solution, and the HTML `dialog` element's built-in focus-trap behavior.""",

"""**Debug Scenario:**
A `useContext` call inside a component returns the default context value instead of the provider's value:

```tsx
const ThemeContext = createContext('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <ChildThatUsesContext />
    </ThemeContext.Provider>
  );
}

function ChildThatUsesContext() {
  const theme = useContext(ThemeContext); // always 'light'!
}
```

Investigation reveals `ChildThatUsesContext` is imported in a file that has its OWN copy of `ThemeContext` (two different module instances due to circular imports or incorrect barrel exports). Show: ensuring both files import from the same `context.ts` file, checking the module's reference with `console.log(ThemeContext)` in both files, and using module bundler aliases to prevent duplicate module instances.""",

"""**Debug Scenario:**
A component that renders a `<canvas>` element shows a blurry rendering on high-DPI (Retina) displays:

```tsx
function Chart({ width, height }: { width: number; height: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const ctx = canvasRef.current!.getContext('2d')!;
    drawChart(ctx); // draws at logical pixel size — blurry on Retina
  }, []);

  return <canvas ref={canvasRef} width={width} height={height} />;
}
```

On a 2x display, the canvas draws at `width × height` logical pixels but the device expects 2x more physical pixels. Show: multiplying canvas dimensions by `devicePixelRatio` (`canvas.width = width * dpr`), scaling the context (`ctx.scale(dpr, dpr)`), setting CSS size to the logical dimensions (`style={{ width, height }}`), and updating on `devicePixelRatio` change (zoom).""",

]

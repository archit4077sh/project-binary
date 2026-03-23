"""
snippets/q_react.py — BATCH 4: 28 brand-new React questions
Zero overlap with batch1, batch2, or batch3 archives.
"""

Q_REACT = [

"""**Task (Code Generation):**
Implement a `usePreviousValue<T>` hook that returns both the previous and current value plus the delta for numeric types:

```ts
const { previous, current, delta } = usePreviousValue(score);
// previous: 85, current: 92, delta: +7
```

Show: the `useRef` pattern to capture the previous value synchronously during render (not in `useEffect`), the TypeScript overload that narrows `delta` to `number | null` only when `T extends number`, and a `<ScoreBadge>` component that flashes green/red based on whether `delta` is positive or negative using a CSS animation triggered by the sign change.""",

"""**Debug Scenario:**
A `<DragDropContext>` (react-beautiful-dnd) around a list of items throws:

```
Invariant failed: provided.innerRef must be used on the drop target element
```

Only in certain conditions — specifically when the `<Droppable>` contains a virtualized list (`react-window`). The inner `ref` from `provided.innerRef` never gets attached to the actual scroll container.

Show: react-beautiful-dnd's requirement that `provided.innerRef` targets the direct scroll container (not a wrapper div), the `outerRef` prop needed for `react-window` + `react-beautiful-dnd` integration, and the correct component structure for a virtualized droppable list.""",

"""**Task (Code Generation):**
Build a `<PermissionBoundary>` component that checks user permissions before rendering children, with role-based and attribute-based access:

```tsx
<PermissionBoundary
  require="documents:write"
  context={{ ownerId: doc.userId }}   // attribute-based: only owner can write
  fallback={<ReadOnlyView />}
  loading={<Spinner />}
>
  <DocumentEditor />
</PermissionBoundary>
```

Show: the permission engine (RBAC + ABAC hybrid), how to asynchronously resolve permissions from the server, the caching strategy so repeated `<PermissionBoundary>` checks for the same action don't make multiple requests, and the TypeScript type for the `require` prop (must be a valid permission string literal).""",

"""**Debug Scenario:**
A `useReducer` hook is initialized with a lazy initializer function, but the initializer runs on every render instead of only once:

```ts
const [state, dispatch] = useReducer(reducer, props.userId, (userId) => {
  return expensiveInit(userId); // runs every render!
});
```

React's lazy initializer (3rd argument) should only run once on mount. The developer mistakenly put `useReducer` inside a conditional. Show: the React Rules of Hooks violation (hooks in conditionals cause reconciliation issues), the symptom pattern, moving the hook to the top level, and an alternative using `useState` with lazy init `() => expensiveInit(userId)` for comparison.""",

"""**Task (Code Generation):**
Implement a `usePortal` hook that renders children into a DOM node outside the React tree:

```ts
const { Portal, portalNode } = usePortal({
  targetId: 'tooltip-root', // append to existing node
  // OR:
  createNewNode: true,       // create and append to body
  onMount: (node) => node.classList.add('portal-active'),
  onUnmount: (node) => node.classList.remove('portal-active'),
});

return <Portal><Tooltip position={coords}>{content}</Tooltip></Portal>;
```

Show: the `ReactDOM.createPortal` implementation inside the `Portal` component, `useLayoutEffect` for synchronous DOM operations, and why portals still propagate synthetic events through the React tree (not the DOM tree).""",

"""**Debug Scenario:**
An application wraps all pages in a `<ErrorBoundary>` that catches render errors and shows a fallback UI. After a successful error (fallback UI shown), the user clicks "Try Again" which calls `errorBoundary.reset()`. The component retries, encounters the same error, and the Error Boundary shows the fallback again — but this time without the "Try Again" button because the reset key didn't change.

Show: the `key` prop pattern for resetting Error Boundary state (changing `key` force-unmounts and remounts), why `componentDidCatch` + `setState({ hasError: false })` alone doesn't retry the render, and a `<RetryErrorBoundary>` that cycles through a limited number of retries before showing a permanent error.""",

"""**Task (Code Generation):**
Build a `useIntervalTree` hook for managing overlapping time ranges (e.g., scheduling calendar events):

```ts
const { add, remove, queryRange, conflicts } = useIntervalTree<CalendarEvent>();

add({ id: '1', start: 900, end: 1100, data: morningMeeting });
add({ id: '2', start: 1000, end: 1200, data: teamSync }); // overlaps

const overlap = queryRange(1000, 1100); // returns both events
const hasConflict = conflicts('3', { start: 1030, end: 1130 }); // true
```

Show: the interval tree data structure, React state management for the tree, and a `<ConflictHighlighter>` component that visually marks conflicting events.""",

"""**Debug Scenario:**
A developer uses React's `StrictMode` and notices their `useEffect` runs twice in development. They disable `StrictMode` to prevent this. Later in production, a bug appears where a subscription listener is attached twice.

The root cause: the developer's `useEffect` had a missing cleanup function — the subscription was added but never removed. `StrictMode` double-invoke was correctly revealing the bug. Show: why React's dev-mode double-invoke is a bug finder not a bug, the proper cleanup pattern for subscriptions, and the three-phase lifecycle (setup → cleanup → setup) that `StrictMode` simulates.""",

"""**Task (Code Generation):**
Implement a `useMultipleSelection` hook for complex list selection UX (similar to OS file managers):

```ts
const { selectedIds, select, deselect, toggle, selectRange, selectAll, clearAll } = useMultipleSelection(items);

// Single click: select
// Shift+click: selectRange from last selected to current
// Ctrl+click: toggle individual without clearing others
// Cmd+A: selectAll
```

Show: tracking the latest clicked item for range selection, the anchor-point pattern for `selectRange`, keyboard event integration, and a `getCheckboxProps(id)` helper that returns the correct `checked`/`onChange` props for each item.""",

"""**Debug Scenario:**
A `<Tooltip>` renders its content in a portal. The tooltip's `useLayoutEffect` measures the portal node's dimensions to position itself. In SSR (Next.js), `useLayoutEffect` fires a warning:

```
Warning: useLayoutEffect does nothing on the server because its effect cannot be encoded into the server renderer's output format.
```

Show: replacing `useLayoutEffect` with `useEffect` for non-blocking DOM measurements (tooltip position can update after first paint), creating a `useIsomorphicLayoutEffect` hook that is `useLayoutEffect` on client and `useEffect` on server, and when each is truly necessary vs just conventional.""",

"""**Task (Code Generation):**
Build a `createCompoundComponent` factory for compound component patterns (like Radix UI Primitives):

```tsx
const Accordion = createCompoundComponent({
  Root: AccordionRoot,
  Item: AccordionItem,
  Trigger: AccordionTrigger,
  Content: AccordionContent,
});

// Usage:
<Accordion.Root type="single">
  <Accordion.Item value="q1">
    <Accordion.Trigger>Question 1</Accordion.Trigger>
    <Accordion.Content>Answer 1</Accordion.Content>
  </Accordion.Item>
</Accordion.Root>
```

Show: the context threading between Root → Item → Trigger/Content, the TypeScript types that make `Accordion.Trigger` outside `Accordion.Item` a type error, and forwarded refs on each sub-component.""",

"""**Debug Scenario:**
A React app using `React.lazy` for code splitting shows a full-page spinner for 3 seconds when navigating to a new route, even on fast connections. The lazy component itself loads quickly, but the Suspense fallback renders for the full duration.

The issue: the lazy component has a `useEffect` that runs an async operation (fetching user data) and doesn't resolve until the data is ready. The component shows a spinner from its own `useEffect` — but since Suspense has already replaced it with the fallback, users see the fallback spinner, then the component mounts and shows another spinner.

Show: using React 18's `use()` hook with a cached Promise for data loading inside the component so Suspense catches it, and eliminating the double-spinner effect.""",

"""**Task (Code Generation):**
Implement a `usePageTransition` system for animating between pages in a React Router app:

```ts
const { navigate, isLeaving, isEntering } = usePageTransition();

// In component:
<div className={cn('page', isLeaving && 'page--exit', isEntering && 'page--enter')}>
  {children}
</div>
```

Show: tracking `isLeaving` (set on navigate START, cleared when exit animation ends) and `isEntering` (set when new route mounts), `useTransition` to keep the old route in the DOM during exit animation, and CSS `@keyframes` for `--exit` and `--enter` states that produce a seamless cross-fade.""",

"""**Debug Scenario:**
A component tree renders a list of notifications as `<NotificationItem>` components. Each `NotificationItem` has a "Dismiss" button. When the dismiss button is clicked, the item animates out and is removed from state. But the animation never plays — the item is immediately removed.

```ts
const dismiss = (id) => {
  setItems(prev => prev.filter(n => n.id !== id)); // removes immediately
};
```

The item is removed from state before the exit animation runs. Show: a two-phase dismiss pattern (1. mark as "dismissing" in state, 2. after animation completes, remove from state using `animationend` event), Framer Motion's `AnimatePresence` as the declarative alternative, and why React 18's View Transition API is the newest solution.""",

"""**Task (Code Generation):**
Build a `useFormStepper` hook for wizard-style multi-step forms:

```ts
const stepper = useFormStepper({
  steps: ['personal', 'address', 'payment', 'review'] as const,
  initialStep: 'personal',
  onComplete: async (allData) => submitOrder(allData),
});

stepper.next(personalData);  // validates current step data, advances
stepper.prev();               // goes back (keeps filled data)
stepper.jumpTo('payment');    // only if payment step was visited before

const { step, stepIndex, totalSteps, isFirst, isLast, data } = stepper;
```

Show: TypeScript literal union for `steps`, per-step data storage, back-navigation data restoration, and step validation with Zod.""",

"""**Debug Scenario:**
Two sibling components both read from a Zustand store, but one component updates a value that should also update the other. The second component renders stale data even though both use the same store.

```ts
// Component A:
const { user, setUser } = useStore();

// Component B:
const { user } = useStore(s => ({ user: s.user })); // creates new object each render
```

Component B's selector `s => ({ user: s.user })` returns a new object reference every call — Zustand uses `Object.is` by default, so it always detects a "change" and re-renders, but conversely the "old" component sees the new reference as different from `user`. Show: using primitive selectors (`s => s.user`) or passing `shallow` as the second argument to `useStore`.""",

"""**Task (Code Generation):**
Implement a `useGlobalHotkeys` system that manages keyboard shortcuts app-wide:

```ts
useGlobalHotkeys([
  { keys: ['meta+k', 'ctrl+k'], action: openCommandPalette, description: 'Open command palette' },
  { keys: ['?'],                 action: openHelpModal,      description: 'Show shortcuts', scope: 'global' },
  { keys: ['j', 'k'],           action: navigateList,        description: 'Navigate', scope: 'list-view' },
]);
```

Show: parsing key combos into modifier + key objects, binding to `keydown` on `window`, scope management (some shortcuts only active in certain contexts), a `useHotkeyScope` hook to push/pop active scopes, and a `<HotkeyCheatSheet>` component that reads all registered hotkeys and shows a modal.""",

"""**Debug Scenario:**
A `<SearchResults>` component uses `useDeferredValue` to show stale results while new results load. But users report seeing stale results for 5-10 seconds during slow API responses — the deferred value stays stale much longer than expected.

```ts
const deferredQuery = useDeferredValue(query);
const { data } = useQuery(['search', deferredQuery], () => search(deferredQuery));
```

`useDeferredValue` defers the value to avoid blocking urgent updates, but if there's no new render to interrupt, it provides no benefit. The query takes 5s to resolve — `useDeferredValue` only defers the UPDATE, not the fetch duration. Show: the correct use case for `useDeferredValue` (it's for rendering, not fetching), progressive disclosure with a loading indicator, and optimistic search results (show previous results with opacity 0.6 during new fetch).""",

"""**Task (Code Generation):**
Build a `<RecursiveRenderer>` component that renders a nested comment tree with collapse/expand:

```tsx
<RecursiveRenderer
  tree={commentTree}
  maxDepth={5}
  renderNode={(comment, { depth, isCollapsed, toggle }) => (
    <Comment
      comment={comment}
      depth={depth}
      isCollapsed={isCollapsed}
      onToggle={toggle}
    />
  )}
/>
```

Show: the recursive component (base case at `maxDepth`), managing collapsed state for thousands of nodes efficiently (use a `Set<id>` of collapsed IDs instead of per-node state), `React.memo` on the node renderer to prevent re-renders on parent collapse/expand, and the TypeScript `TreeNode<T>` generic type.""",

"""**Debug Scenario:**
A `useWebSocket` hook connects to a WS server on mount. During React 18 concurrent mode renders, the hook mounts, starts connecting, then receives a concurrent mode interrupt — React discards the in-progress render and restarts. The WebSocket connects twice, creating two simultaneous connections.

Show: React 18 Strict Mode's intentional double-mount simulation, why effects should be idempotent (connecting twice should clean up the first connection), the correct cleanup function that closes the WebSocket on re-mount, and how to use a `useRef` to hold the connection so the cleanup can reliably close it.""",

"""**Task (Code Generation):**
Implement a `<MarkdownEditor>` with live preview:

```tsx
<MarkdownEditor
  value={content}
  onChange={setContent}
  height={400}
  plugins={['tables', 'strikethrough', 'task-lists']}
  toolbar={['bold', 'italic', 'link', 'image', 'code', 'preview']}
/>
```

Show: a split-pane layout (editor left, preview right), `textarea` event handling for Tab key insertion and list continuation (pressing Enter on a `- list item` auto-starts `- `), markdown parsing using `marked` or `micromark`, syntax highlighting of code blocks in the preview, and real-time preview updates debounced at 150ms.""",

"""**Debug Scenario:**
A production React app logs `Warning: A future version of React will block javascript: URLs as a security precaution` for links rendered from user-generated content.

The warning is from React sanitizing a rendered `<a href="javascript:void(0)">` that was used as a click handler placeholder:

```tsx
<a href="javascript:void(0)" onClick={handleClick}>Click</a>
```

Show: why `javascript:` URLs are an XSS vector, the semantic HTML replacement (`<button>` for actions, `<a href>` for actual navigation), and a `dangerouslySetInnerHTML` content sanitizer using `DOMPurify` for user-generated HTML that allows `<a>` tags but strips `javascript:` href values.""",

"""**Task (Code Generation):**
Build a `useEventQueue` hook that buffers rapid events and processes them in batches:

```ts
const { enqueue, queue, flush, isProcessing } = useEventQueue<UserAction>({
  batchSize: 10,
  flushInterval: 2000,    // auto-flush every 2 seconds
  processor: async (batch) => {
    await api.logActions(batch); // send to analytics
  },
  onError: (err, failedBatch) => retryQueue.push(failedBatch),
});
```

Show: the queue state (array + useRef to avoid stale closure), the `setInterval` auto-flush that clears on unmount, the `flush()` function that processes remaining items before page unload (`beforeunload` event), concurrency control (only one batch processes at a time), and TypeScript generics for the event type.""",

"""**Debug Scenario:**
A server-rendered React app uses a custom cache library that stores fetch results in a `WeakMap`. In production, memory grows unboundedly. The `WeakMap` should garbage collect entries, but it doesn't.

The keys to the `WeakMap` are Response objects: `weakMap.set(response, parsedData)`. The `response` objects are kept alive in a separate `Map` used as a response cache:

```ts
const responseCache = new Map<string, Response>(); // keeps Response objects alive
const parsedCache = new WeakMap<Response, ParsedData>(); // can't GC: Response still in Map
```

Explain `WeakMap` GC semantics (key must have no other strong references), the solution: using the URL string as the key in a regular `Map` with TTL, and when `WeakMap` is actually the right tool (private component data keyed by DOM nodes).""",

"""**Task (Code Generation):**
Implement a `<SplitText>` component that animates each word/letter individually:

```tsx
<SplitText
  text="Hello World"
  mode="words"      // or "chars"
  animateIn={{ opacity: [0, 1], y: [20, 0] }}
  stagger={0.05}    // 50ms between each element
  trigger="inView"  // animate when component enters viewport
/>
```

Show: splitting the text into `<span>` elements (handling `mode="chars"` preserving word spacing), applying CSS custom properties `--delay` for stagger offset, `IntersectionObserver` for the `trigger="inView"` mode, `prefers-reduced-motion` fallback (no animation, immediate show), and the `aria-label` on the container to preserve screen reader experience.""",

"""**Debug Scenario:**
A React app stores authentication state in a global Zustand store. When the user's session expires mid-session, the app shows an expired session modal. But the modal renders behind the page overlay rather than above it.

The modal renders in a Portal appended to `<body>`. But the page has a fullscreen overlay with `z-index: 100`. The modal's portal renders in DOM order BEFORE the overlay, which was added by a third-party cookie consent library:

```
body
  ├── #app-root
  │   └── (portal) #modal-root → modal (z-index: 200)
  └── (cookie bar injects here, z-index: 999)
```

Show: why z-index alone doesn't fix cross-stacking-context issues, using a custom `#top-layer-portal` div that's always the LAST child of `body`, and the `<dialog>` element with `showModal()` as the standards-based solution that's guaranteed to appear above all other content.""",

"""**Task (Code Generation):**
Build a `useKeyboardNavigation` hook for custom listbox/grid keyboard navigation:

```ts
const { activeIndex, setActiveIndex, getItemProps } = useKeyboardNavigation({
  count: items.length,
  orientation: 'vertical', // or 'horizontal' or 'grid'
  columns: 3,              // for grid orientation
  loop: true,              // wrap at edges
  onSelect: (index) => selectItem(items[index]),
});

<ul role="listbox">
  {items.map((item, i) => (
    <li role="option" aria-selected={activeIndex === i} {...getItemProps(i)}>
      {item.label}
    </li>
  ))}
</ul>
```

Show: arrow key handling per orientation, Home/End key support, grid navigation (up/down changes row), the `getItemProps(i)` helper returning tabIndex and event handlers, and `aria-activedescendant` vs roving tabindex (explain when to use each).""",

"""**Debug Scenario:**
A React component receives a large array as `children` and passes it through to a virtualized list. React DevTools Profiler shows the component re-renders on every parent render even though `children` hasn't changed.

```tsx
function VirtualList({ children }) {
  const items = React.Children.toArray(children);
  return <FixedSizeList itemCount={items.length}>{...}</FixedSizeList>;
}
```

`React.Children.toArray(children)` always returns a new array with new stable keys — but the comparison is `items !== prevItems` (referential). Show: using `useMemo(() => React.Children.toArray(children), [children])` and then explaining why `children` prop comparison is shallow (array reference) making the `useMemo` irrelevant. The real fix: pass data as a typed prop instead of `children` for large virtualized lists.""",

]

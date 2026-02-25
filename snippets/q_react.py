"""
snippets/q_react.py - 28 React Internals questions
"""

Q_REACT = [

"""**Context:**
Our Next.js 14 SaaS dashboard has a single UserContext that holds the authenticated user, their RBAC permissions, and notification count. Nearly every interactive component reads from it via useContext().

**Observed Issue:**
The React DevTools Profiler shows 60+ components re-rendering on trivial interactions -- like toggling a checkbox in a form -- that have nothing to do with the user object or permissions. Everything is a UserContext consumer.

**Specific Ask:**
What's the systematic fix? Is context splitting (separate PermissionContext, NotificationContext, UserContext) the right architectural call, or should I adopt use-context-selector? What's the performance and maintenance tradeoff of each at a tree this large?""",

"""**Context:**
Our DataTable is wrapped in React.memo. It receives a columns config array defined outside the component (stable), a rows array (memoized via useMemo), and an onRowClick handler from the parent Dashboard component.

**Code:**
```tsx
function Dashboard() {
  const [filter, setFilter] = useState('');
  return (
    <DataTable
      columns={COLUMNS}
      rows={filteredRows}
      onRowClick={(id) => openModal(id)}  // new ref every render
    />
  );
}
```

**Observed Issue:**
DataTable re-renders on every parent render despite React.memo. columns and rows are stable. The culprit is the inline arrow for onRowClick -- new reference every render.

**Specific Ask:**
Beyond "wrap in useCallback" -- if this is a shared component library, consumers will almost always pass inline callbacks. Should the library use an internal callback ref pattern to absorb reference churn? Or is a custom memo comparison function the right layer to fix this?""",

"""**Context:**
We have a useDataFetcher custom hook that debounces a fetch call. It's used in the FilterBar of our dashboard. When the user types quickly, the debounced fetch fires with stale filter state.

**Code:**
```ts
const fetchDebounced = useCallback(
  debounce(() => {
    fetchRows(filter); // stale closure -- filter captured at creation time
  }, 300),
  [] // empty deps intentionally to avoid re-creating debounce
);
```

**Observed Issue:**
filter inside the debounced closure is always the initial value. Adding filter to the deps array re-creates the debounce on every keystroke, defeating the purpose.

**Specific Ask:**
What's the correct pattern for debounced functions that reference reactive state? Should I read filter from a ref inside the debounce? Is there a useLatest pattern that's idiomatic here and how does it interact with React's concurrent mode?""",

"""**Context:**
Our PermissionGate component uses useMemo to compute whether the current user can see a UI section. The memo returns a plain object with flags.

**Code:**
```ts
const access = useMemo(() => ({
  canEdit: userRoles.includes('editor'),
  canDelete: userRoles.includes('admin'),
}), [userRoles]);
```

**Observed Issue:**
Even when userRoles hasn't changed (same array contents), the component re-renders because userRoles is a new array reference every time it's read from context. The useMemo recalculates, returns a new object, and all consumers re-render.

**Specific Ask:**
How do you memoize correctly when the dependency itself has unstable reference but stable value? Should I serialize userRoles to a string as the dep? Use a deep equality custom hook? Or fix the reference stability upstream in the context?""",

"""**Context:**
We render a paginated list of ReportCard components. When a user navigates between pages, we want to reset each card's internal expanded state.

**Code:**
```tsx
{reports.map((report, index) => (
  <ReportCard key={index} report={report} />
))}
```

**Observed Issue:**
Using key={index} means React reuses existing component instances when items shift positions during pagination. The expanded state bleeds into different reports on page change.

**Specific Ask:**
We switched to key={report.id} and the state resets correctly. But now the enter/exit animation (Framer Motion) is jarring because items are unmounted/remounted rather than repositioned. How do you reconcile stable keys (for correct state) with smooth position animations? Is AnimatePresence + layoutId the right answer here?""",

"""**Context:**
Our useUserData hook fetches a user profile and sets local state. It's used in ~30 components across the dashboard.

**Code:**
```ts
useEffect(() => {
  fetchUser(userId).then(user => setUser(user));
}, [userId]);
```

**Observed Issue:**
When userId changes rapidly (navigating between user detail pages), a slow request from a previous userId can resolve after the current one, setting stale data. Classic race condition.

**Specific Ask:**
What's the idiomatic React pattern for canceling or ignoring stale async operations inside useEffect? For non-cancellable promises (third-party SDK calls), is the ignore-flag pattern sufficient? And how do you write a deterministic test for this in Jest since the bug is timing-dependent?""",

"""**Context:**
We have an ErrorBoundary wrapping a Suspense boundary around our DataTable. When the initial data fetch fails, ErrorBoundary shows a Retry button. On retry, the Suspense fallback (skeleton) should show again while data refetches.

**Observed Issue:**
After the user clicks Retry, the ErrorBoundary resets, but the Suspense boundary doesn't show its fallback -- the UI just goes blank for 2-3 seconds before data appears. The skeleton never renders on retry.

**Specific Ask:**
What's the correct mechanism to reset both a Suspense boundary AND an ErrorBoundary atomically on user retry? Does react-error-boundary's resetKeys interact correctly with Suspense, or is there a key-based reset trick needed at the Suspense level?""",

"""**Context:**
We're building a polymorphic Input component in our design system that needs to accept a ref, support generics for its value type, and be compatible with forwardRef.

**Code:**
```tsx
const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ value, onChange, ...rest }, ref) => (
    <input ref={ref} value={value} onChange={onChange} {...rest} />
  )
);
```

**Observed Issue:**
When we try to make this generic (value: T, onChange: (val: T) => void), TypeScript refuses to infer T through forwardRef. The workaround of casting with `as` loses all type safety.

**Specific Ask:**
What's the correct TypeScript pattern for a generic component wrapped in forwardRef? Is there a way to preserve generic inference without using `as unknown as`? How do major design system libraries (MUI, Radix) handle this?""",

"""**Context:**
We recently enabled React 18's StrictMode across our whole dashboard app. Some components that initialize third-party chart libraries (ECharts, Highcharts) on mount are now crashing.

**Observed Issue:**
StrictMode double-invokes effects in development, so the chart initializes twice on the same DOM node. The second init throws "container already has a chart instance." This doesn't happen in production.

**Specific Ask:**
What's the general pattern for making non-idempotent initializations (chart libs, WebGL contexts, third-party SDKs) StrictMode-safe? Is the solution a ref flag to guard double-init, or should cleanup in the effect return function destroy and re-create the instance? What's the performance implication of destroy+recreate on every dev re-mount?""",

"""**Context:**
After upgrading to React 18 createRoot, we're seeing state tearing -- different parts of the UI briefly show inconsistent data during a concurrent render. Specifically, the data table row count and the summary header count go out of sync for a frame.

**Observed Issue:**
Both components read from the same Zustand store, but during a transition the renders are interleaved across multiple frames, so one component renders with the old value and one with the new value.

**Specific Ask:**
Is useSyncExternalStore the canonical fix for preventing state tearing with external stores in React 18? Does Zustand v4+ already use it internally? If so, why would we still see tearing, and what's the next debugging step?""",

"""**Context:**
We have a charting component that measures its container's bounding rect in useLayoutEffect to size the SVG canvas correctly. In production we're occasionally seeing layout flash.

**Observed Issue:**
On some renders, the chart briefly renders at 0x0 before jumping to the correct size. This only happens on the first mount on slow connections. We suspect useLayoutEffect vs useEffect timing.

**Specific Ask:**
useLayoutEffect fires synchronously after DOM mutation but before paint -- so flash shouldn't be possible. Could this be an SSR issue where useLayoutEffect is suppressed on the server and the size is wrong on hydration? What's the correct pattern for DOM measurement that needs to survive SSR without flash?""",

"""**Context:**
We have a useWebSocket custom hook that connects to our real-time data feed. It's used in 5 different route-level components across the dashboard.

**Observed Issue:**
Each component that uses useWebSocket opens its own WebSocket connection to the same endpoint. We end up with 5 concurrent connections to the same server. We need to share a single connection across all consumers without lifting state.

**Specific Ask:**
What's the pattern for a singleton-style resource (WebSocket, EventSource) shared across multiple hook consumers without a global Provider? Is a module-level singleton with manual ref-counting for connect/disconnect the right approach, or should we use a Context? What's the risk of module-level state in SSR environments?""",

"""**Context:**
We're lazy-loading our AnalyticsPanel with React.lazy because it imports a heavy charting library. We have it inside a Suspense boundary in the dashboard layout.

**Code:**
```tsx
const AnalyticsPanel = lazy(() => import('./AnalyticsPanel'));

<Suspense fallback={<Skeleton />}>
  <AnalyticsPanel />
</Suspense>
```

**Observed Issue:**
The chunk loads fine on first visit. But on subsequent navigation to the dashboard (client-side), the Suspense fallback shows briefly again even though the module is already cached. It's as if React is suspending again on a cached lazy component.

**Specific Ask:**
Should a React.lazy component that has already been loaded ever re-trigger its Suspense boundary on re-render? What conditions would cause this -- could a change in the import() factory function identity cause it to reload? How do you debug which Suspense boundary is triggering?""",

"""**Context:**
Our old ErrorBoundary implementation is a class component (required pre-React 18). We're trying to add retry logic where the boundary resets when the user clicks Retry.

**Code:**
```tsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  reset = () => this.setState({ hasError: false });
  render() {
    if (this.state.hasError) return <button onClick={this.reset}>Retry</button>;
    return this.props.children;
  }
}
```

**Observed Issue:**
When the user clicks Retry, hasError resets to false, but the child that threw the error re-renders and throws again immediately if the underlying error condition hasn't changed.

**Specific Ask:**
What's the correct reset mechanism -- should resetting an ErrorBoundary also trigger the child to re-fetch/re-attempt, or are those decoupled concerns? Is the react-error-boundary library's resetKeys approach better, and can it coordinate with React Query's retry behavior?""",

"""**Context:**
We have a modal component that renders via a Portal (ReactDOM.createPortal) appended to document.body. The modal contains a form with event handlers.

**Observed Issue:**
When a user clicks inside the modal, the event bubbles up through the React tree (not the DOM tree), reaching an onClick handler on a parent component outside the portal. This parent handler closes the modal, so clicking inside the modal immediately closes it.

**Specific Ask:**
React portals bubble events through the React component tree, not the DOM tree. What's the correct pattern to stop portal events from triggering ancestor handlers? stopPropagation on the portal container? Or restructuring the component tree so the modal isn't a child of the closeable component?""",

"""**Context:**
We're refactoring a large form component in our dashboard from multiple useState calls to useReducer. The form has 15 fields with cross-field validation rules.

**Observed Issue:**
With useReducer, dispatching an action feels verbose for simple field updates. We're writing a SET_FIELD action for every individual field change. The reducer is growing to 200+ lines. Some cross-field logic (clearing field B when field A changes) is easy in the reducer but hard to test independently.

**Specific Ask:**
At what complexity threshold does useReducer become the right choice over useState for forms? And is there a pattern to keep the reducer manageable -- like sub-reducers per form section, or is that an anti-pattern in React? How do libraries like React Hook Form avoid this complexity entirely?""",

"""**Context:**
Our theme context provides a value object created inline in the provider render function.

**Code:**
```tsx
<ThemeContext.Provider value={{ theme, setTheme, resolvedColors }}>
```

**Observed Issue:**
Every time the ThemeProvider re-renders (e.g., from its parent), it creates a new value object reference even if theme and resolvedColors haven't changed. Every context consumer re-renders unnecessarily.

**Specific Ask:**
Is the fix as simple as wrapping the value in useMemo? What are the edge cases -- can useMemo ever return a stale object for theme? Is there a pattern where the context value object is structurally stable by design (e.g., splitting state from dispatch)?""",

"""**Context:**
We're on React 18 and noticed that setState calls inside setTimeout and native event handlers are now batched, which changed some behavior we depended on in our notification system.

**Code:**
```ts
setTimeout(() => {
  setLoading(false);  // React 17: triggers render
  setData(result);    // React 17: triggers second render
  // React 18: both batched into ONE render
}, 100);
```

**Observed Issue:**
A component that depended on two separate renders (loading=false fires a useEffect, then data update fires another useEffect) now only gets one render commit. The useEffect that depended on loading=false fires with data already set, breaking its assumptions.

**Specific Ask:**
With React 18 automatic batching, how do you force a re-render boundary between two setState calls when the order of effects matters? Is flushSync the appropriate tool, or should the component logic not depend on intermediate render states?""",

"""**Context:**
We have a heavy TaxCalculator component that runs CPU-intensive computations synchronously in render. User interactions elsewhere in the dashboard (typing in a search box) stutter while TaxCalculator is re-rendering.

**Observed Issue:**
User keystroke → parent state update → TaxCalculator re-renders synchronously → 120ms main thread block → keystrokes are dropped.

**Specific Ask:**
How does useTransition/startTransition help here? My understanding is it marks state updates as non-urgent, deferring re-renders of components like TaxCalculator. Does this mean the TaxCalculator render literally gets interrupted and resumed? What's the mental model difference between useTransition and Web Workers for this use case?""",

"""**Context:**
We pass a search query to a FilteredList component which runs an expensive filter over 50k items synchronously on every keystroke.

**Code:**
```tsx
function Dashboard() {
  const [query, setQuery] = useState('');
  const filtered = filterItems(items, query); // expensive
  return <FilteredList items={filtered} />;
}
```

**Observed Issue:**
Typing in the search box feels sluggish. We want the input to feel instant while the list updates lag behind.

**Specific Ask:**
Is useDeferredValue the right tool here? My concern is that filterItems is still called on every render -- it just renders two versions of the list. Does React actually skip the deferred render if a newer update comes in? How does this differ from debouncing the query state update?""",

"""**Context:**
We have a DataTable component that needs to expose an imperative scrollToRow(id) method so parent components can trigger scroll-to programmatically (e.g., after a search match).

**Observed Issue:**
Using a ref on the DataTable DOM element gives us the container div, not the virtualized list's scrolling API. We need to expose the underlying react-window List instance's scrollToItem method.

**Specific Ask:**
Is this the canonical use case for useImperativeHandle? What's the correct TypeScript type for the exposed handle? And architecturally, when does imperative escape hatching via refs become a code smell vs. a necessary pattern for genuinely imperative operations?""",

"""**Context:**
We're using the React Profiler API to measure render times in our production dashboard for performance monitoring.

**Code:**
```tsx
<Profiler id="DataTable" onRender={(id, phase, actualDuration) => {
  analytics.track('render', { id, phase, actualDuration });
}}>
  <DataTable />
</Profiler>
```

**Observed Issue:**
actualDuration spikes to 400ms on some renders but the DevTools profiler shows only 20ms. The discrepancy is confusing our monitoring dashboard.

**Specific Ask:**
What's the difference between the React Profiler's actualDuration and what DevTools shows? Does actualDuration include the time for React to diff the tree (reconciliation) plus render, while DevTools only shows commit time? When should you trust one over the other for perf regression alerting?""",

"""**Context:**
We render a dynamic list of form sections where sections can be added, removed, or reordered. Each section is a React.Fragment with a key.

**Code:**
```tsx
{sections.map(section => (
  <React.Fragment key={section.id}>
    <SectionHeader section={section} />
    <SectionBody section={section} />
  </React.Fragment>
))}
```

**Observed Issue:**
When a section is removed mid-list, the SectionBody below it briefly shows stale data before unmounting. We think React is reassigning keys or deferring unmount.

**Specific Ask:**
Can keyed Fragments cause reconciliation issues where child components momentarily receive wrong props before their parent Fragment unmounts? Or is this a different bug -- perhaps related to Zustand state not updating synchronously?""",

"""**Context:**
We have a legacy NumberInput component that was built as an uncontrolled component using defaultValue. We're migrating it to be controlled (value + onChange) as part of a form library integration.

**Observed Issue:**
During migration, some instances of NumberInput flicker between controlled and uncontrolled -- React throws "A component is changing an uncontrolled input to be controlled." This happens when the initial value prop is undefined and later becomes a number.

**Specific Ask:**
What's the correct migration strategy from uncontrolled to controlled without React's warning? Is always initializing with a defined value (even 0 or '') the only fix? And what are the scenarios where uncontrolled inputs are still the right choice even in a React Hook Form world?""",

"""**Context:**
We're building an accessible multi-select combobox in our design system. It has a listbox and each option needs a unique id for aria-activedescendant to work correctly with SSR.

**Code:**
```tsx
const id = `option-${Math.random()}`; // different every render + SSR mismatch
```

**Observed Issue:**
Using Math.random() causes hydration mismatch. Using an incrementing counter causes id collisions when multiple comboboxes are on the same page.

**Specific Ask:**
Is React 18's useId the correct solution here? How does useId guarantee uniqueness across concurrent renders and SSR? Does it work correctly with streaming SSR where components hydrate in a different order than they rendered on the server?""",

"""**Context:**
We noticed that after a fast refresh (HMR), some components that were previously memoized start re-rendering on every update. The behavior disappears after a full page reload.

**Observed Issue:**
We suspect the component function identity changes between hot module replacements, breaking React.memo's reference check. React.memo compares props but the component itself is a new function reference after HMR.

**Specific Ask:**
Does changing a component's function identity between renders (via HMR) affect React.memo's behavior? How does React identify component types -- by reference, by displayName, or something else? Is this a known HMR gotcha and is there a way to preserve memo across hot reloads?""",

"""**Context:**
We have a layout component that passes children to multiple slots using React.Children.map and cloneElement to inject props into children.

**Code:**
```tsx
React.Children.map(children, child =>
  React.cloneElement(child, { theme, onAction })
)
```

**Observed Issue:**
The pattern breaks when children are wrapped in Fragment or conditional expressions. Also, TypeScript loses the child's prop types after cloneElement.

**Specific Ask:**
Is React.Children + cloneElement considered an anti-pattern in 2024? What's the modern composition alternative -- render props, Context, compound components with explicit slots? We need the parent to inject theme and onAction without requiring children to explicitly accept those props.""",

"""**Context:**
Our ESLint react-hooks/exhaustive-deps rule is flagging a dependency we intentionally omit. We have a useEffect that should only run on mount, but it uses a function defined outside the component.

**Code:**
```ts
useEffect(() => {
  initializeSDK(config); // ESLint wants config in deps
}, []); // eslint-disable-line -- intentional, run once
```

**Observed Issue:**
config is a prop that changes on every render (object literal passed from parent). Adding it to deps causes initializeSDK to re-run on every render. Disabling the lint rule with a comment feels like a code smell.

**Specific Ask:**
What's the idiomatic way to initialize something once from a prop value without disabling exhaustive-deps? Should config be stabilized with a ref (useRef(config)) and read inside the effect? How does the community handle this pattern in libraries like analytics trackers or SDK initializers?""",

]

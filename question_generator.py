"""
question_generator.py — Generates realistic senior frontend engineering questions
using a rich template + snippet system. No LLM API required.
"""

import random
import textwrap
from config import PRODUCT_CONTEXT
from snippets.react import REACT_SNIPPETS
from snippets.nextjs import NEXTJS_SNIPPETS
from snippets.typescript import TYPESCRIPT_SNIPPETS

# ─── Helper ───────────────────────────────────────────────────────────────────

def _fmt_code(snippet: str) -> str:
    """Wrap a code snippet in markdown fences."""
    return f"```\n{textwrap.dedent(snippet).strip()}\n```"

def _rc(lst: list) -> str:
    """Return a random choice from a list."""
    return random.choice(lst)

_stack = PRODUCT_CONTEXT["stack"]
_features = PRODUCT_CONTEXT["features"]
_product = PRODUCT_CONTEXT["product"]

# ─── Template Banks ───────────────────────────────────────────────────────────

def _make_react_internals(subtopic: str) -> str:
    if subtopic == "re-render_debugging":
        snippet = _rc(REACT_SNIPPETS[:3])
        return f"""\
**Context:**
Working on our {_product}. We have a `PermissionGate` component that wraps almost every interactive element and checks the current user's RBAC roles. The React DevTools Profiler shows it rendering 40-60 times on a single keystroke in the filter bar — even though permissions never change during a session.

**Code:**
{_fmt_code(snippet)}

**Observed Issue:**
The profiler flame chart shows `PermissionGate` as the hottest component, but `React.memo` is already applied. Interestingly the re-renders only happen when the parent context has any state update — even unrelated state.

**Specific Ask:**
What's the idiomatic way to isolate context consumers so a context update in, say, `NotificationContext`, doesn't cascade into `PermissionGate`? Should I be splitting context into smaller atoms, using a selector pattern (like `useContextSelector`), or is there a better architectural solution here?"""

    elif subtopic == "memoization_misuse":
        snippet = _rc(REACT_SNIPPETS[1:4])
        return f"""\
**Context:**
In our {_product} we memoize a `columns` configuration array that gets passed to a virtualized `DataTable` component. Despite the `useMemo`, the table still triggers a full re-render on every parent update.

**Code:**
{_fmt_code(snippet)}

**Observed Issue:**
Even though `columns` is wrapped in `useMemo([])`, the DataTable re-renders. I added a `console.log("columns recomputed")` inside the memo — it does NOT fire. So `columns` reference is stable. But the table still re-renders fully according to the profiler.

**Specific Ask:**
If `columns` is provably stable (no recomputation) and `DataTable` is wrapped in `React.memo`, what other vectors could cause it to re-render on every parent tick? I suspect `onSort` callback or the `rows` prop, but what's the systematic debugging approach you'd use with React DevTools to pinpoint the exact offending prop without trial-and-error?"""

    elif subtopic == "reconciliation_key_issue":
        return f"""\
**Context:**
We have a dynamically filtered list in our {_product} dashboard sidebar. When the filter changes, items shift positions significantly. We're seeing some items flash or lose focus state unexpectedly.

**Code:**
```
// Items are keyed by index after filtering
{{ filteredItems.map((item, idx) => (
  <SidebarItem key={{idx}} item={{item}} />
)) }}
```

**Observed Issue:**
When the user types in the filter box, sidebar items with focus (expanded accordions, active dropdowns) jump to wrong items or collapse. Classic key-by-index problem. But the tricky part: each item has a stable `.id` field, yet keying by `.id` makes the transition animation look jarring because items are added/removed rather than shifted.

**Specific Ask:**
Is there a pattern to get both stable reconciliation (key by id) AND smooth positional animations during filter transitions? I'm thinking `layout` animations via Framer Motion, but I want to understand if there's a reconciliation-level solution before reaching for animation libraries. What does React's diffing algorithm actually do differently between keyed-by-id vs keyed-by-index in this scenario?"""

    elif subtopic == "suspense_edge_case":
        snippet = _rc(REACT_SNIPPETS[6:])
        return f"""\
**Context:**
We're migrating our data fetching in the {_product} to use Suspense-compatible data sources. The happy path works fine, but we're hitting a gnarly edge case with nested Suspense boundaries.

**Code:**
{_fmt_code(snippet)}

**Observed Issue:**
When the inner `DataTable` Suspense resolves but throws an error on a *second* fetch (re-query after a filter change), the `ErrorBoundary` catches it fine. But the `TableSkeleton` fallback never shows on the refetch — the component just goes blank. The Suspense boundary seems to not reset properly after the ErrorBoundary catches and the user hits "Retry".

**Specific Ask:**
What's the correct way to reset both an ErrorBoundary and a Suspense boundary together on user retry? I know react-error-boundary has `resetKeys`, but how does Suspense interact with that reset cycle? Is there a risk of a waterfall during the reset?"""

    elif subtopic == "strict_mode_double_invoke":
        return f"""\
**Context:**
We recently enabled React 18's StrictMode across our entire {_product} app. Now we're seeing some unexpected behavior in components that have side effects in the render phase — specifically a custom `useDataGridStore` hook that initializes some WebGL canvas on mount.

**Observed Issue:**
With StrictMode, the WebGL canvas is being initialized twice, and the second initialization errors with "WebGL context already exists on this canvas element". This doesn't happen in production (StrictMode is dev-only), but it's destroying our dev DX and hiding real bugs.

**Specific Ask:**
Beyond just "clean up in useEffect's return function", what are the patterns for handling truly non-idempotent initializations (WebGL, third-party chart libs, WebSockets) in a StrictMode-safe way? Is the pattern to track initialization with a ref? And how do you test that your cleanup is actually complete when StrictMode unmounts/remounts?"""

    else:  # concurrent_rendering_teardown
        return f"""\
**Context:**
We upgraded from React 17 to React 18 and opted into `createRoot`. Now we're seeing a race condition in our `useWebSocket` hook — the socket connects, receives a message, and tries to call `setState`, but the component has already been torn down by a concurrent render.

**Observed Issue:**
We get "Can't perform a React state update on an unmounted component" warnings (even though React 18 supposedly removed that warning). Digging deeper, the issue is the WebSocket `onmessage` handler holding a stale setState reference from before a concurrent render interruption.

**Specific Ask:**
In concurrent React, what's the safest pattern for external subscriptions (WebSockets, EventEmitter, BroadcastChannel) that fire asynchronously? Is `useSyncExternalStore` the right answer here, or is that overkill for a single-component subscription? What are the tradeoffs vs. a ref-based abort pattern?"""


def _make_performance(subtopic: str) -> str:
    if subtopic == "bundle_splitting_strategy":
        return f"""\
**Context:**
Our {_product} has grown to a {_rc(['2.1MB', '1.8MB', '2.4MB'])} initial JS bundle (gzipped: ~{_rc(['620KB', '580KB', '700KB'])}). The landing page is `/dashboard` and it currently imports everything eagerly — our heavy chart library ({_rc(['Recharts', 'Victory', 'Nivo'])}), the data grid, the permission engine, and the entire design system.

**Observed Issue:**
Lighthouse LCP is {_rc(['4.2s', '3.8s', '4.6s'])} on a mid-tier device on 4G. `next build` output shows the `/dashboard` route chunk at {_rc(['890KB', '760KB', '1.1MB'])} — clearly no splitting is happening even though we use `next/dynamic` in theory.

**Specific Ask:**
What's the systematic process to audit which `next/dynamic` calls are actually being respected vs. which imports are being hoisted into the parent chunk by the bundler? We use barrel files (`index.ts`) extensively — is that the culprit? And when splitting, what's the right heuristic for where to draw the chunk boundary in a dashboard that has lots of conditionally-shown panels?"""

    elif subtopic == "tree_shaking_failure":
        return f"""\
**Context:**
Our bundle analysis (via `@next/bundle-analyzer`) shows `lodash` is being included fully ({_rc(['530KB', '480KB', '510KB'])} unminified) even though we only use `debounce` and `groupBy`.

**Code:**
```typescript
// utils/data.ts
import {{ groupBy, debounce, sortBy }} from 'lodash';  // ← named imports, should tree-shake
```

**Observed Issue:**
Despite named imports, the full lodash bundle ships. We're on Webpack 5 (via Next.js 14) with `sideEffects: false` in our package.json. I expected this to be tree-shaken.

**Specific Ask:**
Why does Webpack 5 fail to tree-shake `lodash` even with named imports and `sideEffects: false`? Is it because `lodash` is CJS (not ESM)? What's the fix — `lodash-es`? A babel plugin? And more broadly, how do I reliably audit which packages in our dependency tree are CJS vs. ESM, since this will affect our entire tree-shaking strategy?"""

    elif subtopic == "react_profiler_bottleneck":
        return f"""\
**Context:**
Using the React DevTools profiler on our {_product} main table view. After a WebSocket update arrives with ~200 row changes, the profiler shows a {_rc(['180ms', '220ms', '240ms'])} render commit — enough to cause visible frame drops on 60fps displays.

**Observed Issue:**
The flame chart shows the top-level `<Dashboard>` re-renders, which cascades into `<DataTable>` and then all {_rc(['200', '150', '250'])} visible rows. Even rows that didn't change are re-rendering (shown in grey, not yellow, in the profiler, but still appearing in the commit).

**Specific Ask:**
If rows that "didn't change" still appear in the profiler commit tree, does that mean they actually re-ran their render function, or is this a profiler display artifact? And what's the most effective combination of `React.memo`, `useMemo`, and state normalization to make only the changed rows re-render after a bulk WebSocket update? I want to understand the algorithm, not just the fix."""

    elif subtopic == "memory_leak_listeners":
        return f"""\
**Context:**
Our {_product} runs as a long-lived SPA. Users keep the dashboard open for hours. After ~2 hours, memory usage in Chrome DevTools has grown from ~{_rc(['80MB', '100MB', '90MB'])} to ~{_rc(['400MB', '350MB', '450MB'])} and interaction latency spikes noticeably.

**Code:**
```typescript
function useRealtimeMetrics(metricId: string) {{
  useEffect(() => {{
    const handler = (event: MessageEvent) => {{
      updateMetric(metricId, event.data);
    }};
    window.addEventListener('message', handler);
    // cleanup is missing or wrong
  }}, [metricId]);
}}
```

**Observed Issue:**
Chrome Memory tab heap snapshot shows thousands of detached `MessageEvent` listener references growing over time. The component is mounted/unmounted often as users navigate between dashboard tabs.

**Specific Ask:**
Beyond just "add cleanup in useEffect", what's the correct pattern for managing event listeners that depend on changing values (`metricId`)? How does the dependency array interact with cleanup — does React call cleanup on EVERY `metricId` change, or only on unmount? And how would you set up a memory profiler baseline test so this class of bug is caught in CI before it ships?"""

    elif subtopic == "virtualized_list_overscan":
        return f"""\
**Context:**
Our {_product} data table uses `react-window` (`FixedSizeList`) to render {_rc(['10,000', '50,000', '20,000'])} rows. Performance is generally fine but we're seeing two issues: (1) fast scrolling causes a white flash before rows render, and (2) rows with expandable sub-rows break the fixed-height assumption.

**Observed Issue:**
Increasing `overscanCount` from 3 to 20 reduces flashing but makes the render commit heavier. The variable-height rows cause `FixedSizeList` to miscalculate item positions completely after an expansion.

**Specific Ask:**
For the variable-height case, is `VariableSizeList` with `itemSize` callback the right solution, or should we be managing a position cache ourselves? What's the correct way to invalidate the cache when a row expands? And for the overscan/flash tradeoff — is there a middle ground, like preloading rows off-screen without increasing the DOM node count?"""

    elif subtopic == "layout_thrashing":
        return f"""\
**Context:**
We have a custom sticky column implementation in our {_product} table — when the user scrolls horizontally, we programmatically set `left` offsets on sticky cells based on the measured widths of preceding columns.

**Code:**
```typescript
function updateStickyOffsets(tableRef: RefObject<HTMLElement>) {{
  const cells = tableRef.current!.querySelectorAll('[data-sticky]');
  let offset = 0;
  cells.forEach(cell => {{
    const width = cell.getBoundingClientRect().width; // READ
    (cell as HTMLElement).style.left = `${{offset}}px`;  // WRITE
    offset += width; // READ-THEN-WRITE interleaved
  }});
}}
```

**Observed Issue:**
Chrome DevTools Performance tab shows forced reflows on every scroll event. The sticky column calculation is clearly causing layout thrashing — read then write then read again inside the same loop.

**Specific Ask:**
What's the canonical pattern to batch DOM reads and writes to avoid interleaved reflows here? Should I be using `requestAnimationFrame`, a `ResizeObserver`, or reading widths once and caching them? And is CSS `position: sticky` with `left` achievable purely through CSS scroll-linked behavior to avoid JS altogether in modern browsers?"""


def _make_nextjs(subtopic: str) -> str:
    snippet = _rc(NEXTJS_SNIPPETS)
    if subtopic == "ssr_hydration_mismatch":
        return f"""\
**Context:**
Our {_product} has a `RelativeTime` component that renders timestamps like "3 minutes ago". We're using it in a Server Component context, and it hydrates on the client.

**Code:**
```tsx
// components/RelativeTime.tsx
export function RelativeTime({{ timestamp }}: {{ timestamp: string }}) {{
  const diff = Date.now() - new Date(timestamp).getTime();
  const label = formatDuration(diff);  // e.g. "3 minutes ago"
  return <span>{{label}}</span>;
}}
```

**Observed Issue:**
We're getting Next.js hydration mismatch warnings: "Text content did not match. Server: '4 minutes ago' Client: '4 minutes ago'" — identical string, but React still throws. This causes a full client re-render, tanking our LCP.

**Specific Ask:**
Why does React throw a hydration mismatch when the strings appear identical? Is this a millisecond-level timing difference between server render and client hydration? What's the canonical Next.js 14 solution — `suppressHydrationWarning`, `useEffect`-based deferred render, or converting to a Client Component? And how does each approach affect streaming and LCP?"""

    elif subtopic == "streaming_rsc":
        return f"""\
**Context:**
We adopted React Server Components + streaming in our {_product} rewrite. The dashboard page shells in ~{_rc(['200ms', '150ms', '180ms'])} and slow components stream in progressively. But our KPI summary section — the most important above-the-fold content — is streaming in LAST, after the less important table section.

**Code:**
{_fmt_code(snippet)}

**Observed Issue:**
Despite the KPI Suspense boundary appearing first in JSX, the table data resolves first because its query is faster. React streams in resolved components as they complete, not in JSX order.

**Specific Ask:**
Is there a way to hint to React's streaming scheduler that the KPI Suspense boundary has higher priority and should be streamed first, even if it resolves later? Or is the solution purely data-layer (make KPI query faster)? How does React determine stream order with multiple Suspense boundaries, and can we influence it?"""

    elif subtopic == "server_vs_client_components":
        return f"""\
**Context:**
We're doing the RSC migration for our {_product}. Trying to push as much as possible to Server Components, but hitting component boundary issues constantly. Our main pain point: the data table needs `useState` for row selection, but the row data should come from a Server Component fetch.

**Observed Issue:**
The moment we add `'use client'` to `DataTable`, all its children (including row components that could be pure RSC) become client components by inheritance. We end up shipping more JS than before the migration.

**Specific Ask:**
What's the correct compositional pattern to keep RSC-fetched data flowing into client interactive islands without converting everything to `'use client'`? I've seen the "pass server components as children/props to client components" pattern — is that the recommended approach here? What are the gotchas, and how do you handle the type safety when passing RSC output as a prop?"""

    elif subtopic == "caching_stale_data":
        return f"""\
**Context:**
Our {_product} route handler at `/api/rows` uses `revalidate = 30`. But after a user creates a new row via a POST, the GET still returns stale data for up to 30 seconds. We need near-instant consistency on mutations.

**Code:**
{_fmt_code(NEXTJS_SNIPPETS[1])}

**Observed Issue:**
We tried calling `revalidatePath('/dashboard')` in the Server Action after the POST, but the cached GET route data doesn't update — the route handler cache and the page cache seem independent.

**Specific Ask:**
What's the difference between `revalidatePath`, `revalidateTag`, and the fetch cache in Next.js 14? Which one controls the route handler's `revalidate` segment config specifically? And is there a way to do fine-grained tag-based revalidation for individual rows so we don't nuke the entire page cache on every mutation?"""

    else:
        return f"""\
**Context:**
We're using Next.js 14 Middleware to enforce RBAC on our {_product}. The middleware reads a JWT from cookies and checks permissions before allowing route access.

**Code:**
{_fmt_code(NEXTJS_SNIPPETS[2])}

**Observed Issue:**
The middleware works correctly for initial page loads. But when using `router.push()` for client-side navigation, the middleware doesn't run — it only runs on full-page loads and API calls. So a user can navigate to `/dashboard/admin` client-side even if their token lacks the `admin` permission.

**Specific Ask:**
Is Next.js Middleware guaranteed to run on `router.push()` client-side navigations in Next.js 14 App Router? If not, where should RBAC enforcement live for client-side transitions? Should we duplicate the permission check in a layout Server Component, or is there a middleware-based solution that intercepts client navigation RSC fetches?"""


def _make_typescript(subtopic: str) -> str:
    snippet = _rc(TYPESCRIPT_SNIPPETS)
    titles = {
        "complex_generic_inference": "generic inference failure",
        "mapped_type_pitfall": "mapped type issue",
        "discriminated_union_narrowing": "discriminated union narrowing",
        "deep_readonly_mutation": "deep readonly compatibility",
        "conditional_type_distribution": "conditional type distribution",
        "infer_keyword_usage": "infer keyword usage",
    }
    title = titles.get(subtopic, "TypeScript issue")
    return f"""\
**Context:**
On our {_product} codebase (TypeScript 5.4, strict mode, no `any`). I'm hitting a {title} that's blocking a clean abstraction for our data fetching layer.

**Code:**
{_fmt_code(snippet)}

**Observed Issue:**
TypeScript is incorrectly widening / narrowing / refusing to infer the type in the generic layer. The concrete usage compiles fine, but the generic wrapper breaks. The error makes sense mechanically but the workaround feels wrong.

**Specific Ask:**
What's the root cause of this inference failure? Is this a known TypeScript limitation, or am I structuring the types incorrectly? What's the idiomatic fix — a type assertion, a function overload, or a restructuring of the generic constraints? I want to understand the *why* before I reach for `as unknown as T`."""


def _make_architecture(subtopic: str) -> str:
    if subtopic == "monorepo_package_boundary":
        return f"""\
**Context:**
We're splitting our {_product} monorepo (Turborepo + pnpm workspaces) into packages: `@dash/ui`, `@dash/data`, `@dash/auth`, `@dash/permissions`. We're hitting circular dependency issues — `@dash/ui` imports types from `@dash/permissions` to show/hide elements, but `@dash/permissions` imports UI primitives from `@dash/ui` for its modal.

**Observed Issue:**
Turborepo warns of a cycle: `@dash/ui` → `@dash/permissions` → `@dash/ui`. TypeScript project references also refuse to compile with circular deps.

**Specific Ask:**
What's the standard approach to break this kind of UI ↔ logic circular dependency in a monorepo? Is the solution an `@dash/types` package that both depend on? Or should UI components accept permission props via render props / composition to avoid importing from `@dash/permissions` at all? How do companies at scale (Vercel, Linear) structure this boundary?"""

    elif subtopic == "microfrontend_state_sharing":
        return f"""\
**Context:**
We're experimenting with Module Federation on our {_product}. The host app and the `analytics-mfe` remote both use React Query. The problem: they each have their own `QueryClient` instance, so cache is not shared. A row update in the host invalidates its cache, but the analytics MFE still shows stale data.

**Observed Issue:**
Two `QueryClient` instances = two separate caches. We can't share a singleton because the host and remote are built independently with different React Query versions (host: v5, remote: v4).

**Specific Ask:**
What's the recommended pattern for state/cache synchronization across Module Federation remotes that have independent React instances? Is `BroadcastChannel` the right primitive for cross-MFE cache invalidation? Or should we push toward a shared event bus? And what's the long-term solution if we can't force version alignment between host and remote?"""

    elif subtopic == "feature_flag_architecture":
        return f"""\
**Context:**
Our {_product} has grown to ~{_rc(['40', '60', '80'])} feature flags managed in LaunchDarkly. They're consumed inconsistently — some via a custom `useFlag` hook (client-side), some fetched server-side in RSC, some hardcoded. We're about to add flag-dependent SSR rendering and the current approach won't scale.

**Observed Issue:**
Flag evaluation on the server and client can diverge, causing hydration mismatches. Also, our flag bootstrapping adds ~{_rc(['120ms', '80ms', '150ms'])} to TTFB because the RSC waits for LD to evaluate before rendering.

**Specific Ask:**
What's a production-grade feature flag architecture for a Next.js 14 RSC app? Specifically: how do you pass server-evaluated flags down to client components without prop-drilling or hydration issues? And how do you handle the bootstrapping latency — edge config, streaming, or something else?"""

    else:
        return f"""\
**Context:**
Our `@dash/ui` design system is consumed by 4 internal dashboards. We're on version `2.x` and need to do a breaking change in our `<Select>` component API (changing `value` from `string` to `{{ id: string; label: string }}`).

**Observed Issue:**
All 4 consumers are on different minor versions of `@dash/ui`. We can't do a big-bang upgrade. Some teams won't upgrade for months. We need to ship the new API while keeping the old one working.

**Specific Ask:**
What's the recommended versioning + migration strategy for a design system breaking change when consumers are on different release cadences? Is the answer deprecation warnings + a major version bump? Or maintain both API shapes via overloaded types and a compatibility shim? How do you structure the type definitions to allow both old and new usage simultaneously in TypeScript?"""


def _make_debugging(subtopic: str) -> str:
    if subtopic == "race_condition_in_hook":
        snippet = REACT_SNIPPETS[2]
        return f"""\
**Context:**
Our {_product} has a `useUserData` hook used across ~{_rc(['30', '20', '40'])} components. We're seeing intermittent data flashes in production — a user will briefly see another user's data before the correct data loads.

**Code:**
{_fmt_code(snippet)}

**Observed Issue:**
When `userId` changes rapidly (e.g., navigating between user profiles), the slow request sometimes resolves *after* a faster subsequent request. TypeScript and ESLint give no warning — this is a pure runtime race condition.

**Specific Ask:**
What's the idiomatic React pattern to cancel or ignore stale async requests in a `useEffect`? I know about AbortController for fetch — but how do you handle non-cancellable promises (e.g., a library that doesn't support AbortSignal)? And how would you write a test for this race condition — since it's timing-dependent, how do you make it deterministic in Jest?"""

    elif subtopic == "stale_closure_trap":
        snippet = REACT_SNIPPETS[0]
        return f"""\
**Context:**
Classic stale closure, but in a production context that makes it harder to spot. Our {_product} filter bar uses a debounced fetch triggered from a `useCallback` hook.

**Code:**
{_fmt_code(snippet)}

**Observed Issue:**
When the user types quickly, the debounced fetch fires with the filter value from when the callback was created (empty string or initial value), not the current value. The `filter` inside the debounced closure is always stale.

**Specific Ask:**
This is a well-known problem but I want to understand the best solution for this specific shape: debounced callbacks referencing reactive state. Should I use a ref for `filter` and read it inside the debounce, or restructure to use `useEffect` with the debounce timer internally? What are the tradeoffs? And does `useCallback` with a full dependency array defeat the purpose of debouncing?"""

    elif subtopic == "infinite_render_loop":
        return f"""\
**Context:**
After migrating a component in our {_product} from class-based to functional, we started hitting an infinite render loop. The component is a `ReportBuilder` that manages complex form state.

**Code:**
```typescript
function ReportBuilder() {{
  const {{ filters }} = useReportStore();
  const normalizedFilters = useMemo(
    () => normalizeFilters(filters),  // returns a new object every time
    [filters]
  );

  useEffect(() => {{
    setDerivedState(normalizedFilters);  // triggers re-render
  }}, [normalizedFilters]);  // but normalizedFilters is new each render → infinite loop
}}
```

**Observed Issue:**
`normalizeFilters` returns a structurally equal but referentially new object every call. So `useMemo` sees `filters` change on every render (because Zustand returns a new reference), memoization fails, and the effect re-fires infinitely.

**Specific Ask:**
How do you break this specific loop where (a) a selector returns a new reference even if contents are the same, (b) `useMemo` depends on it, and (c) an effect depends on the memoized value? Is the solution a deep-equality based `useMemo`? A custom `useDeepCompareMemo`? Or a structural change to how I consume Zustand state?"""

    else:
        return f"""\
**Context:**
In our {_product}, we have a global keyboard shortcut system (`useHotkeys`). After adding a new shortcut for the data table, we noticed existing shortcuts stop working after the table is unmounted (e.g., navigating away from the table route).

**Observed Issue:**
The `useHotkeys` hook attaches a `keydown` listener to `window`. When the table component unmounts, the listener is removed correctly (we verified with DevTools). But the other shortcuts also stop working on that same route transition.

**Specific Ask:**
If each `useHotkeys` call manages its own listener and cleanup, why would one component's unmount affect listeners registered by a completely different component? Could this be a React 18 concurrent scheduling issue where cleanup runs in a different order than expected? How would you debug listener interference without a global event bus?"""


def _make_state_management(subtopic: str) -> str:
    if subtopic == "zustand_vs_redux_tradeoff":
        return f"""\
**Context:**
Our {_product} currently uses Redux Toolkit for all client state. The team wants to migrate to Zustand for simplicity. We have ~{_rc(['25', '30', '20'])} slices, heavy use of `createAsyncThunk`, and middleware (logging, analytics, optimistic updates).

**Observed Issue:**
Zustand's simplicity is appealing, but we rely on RTK's DevTools integration, time-travel debugging, and the action log for production bug replay. Zustand's middleware ecosystem is thinner.

**Specific Ask:**
What's a realistic, honest tradeoff analysis between Zustand and Redux Toolkit at our scale? Specifically: does Zustand's `devtools` middleware give the same action-log-based debugging capability as RTK DevTools? How do you replicate `createAsyncThunk` loading/error states in Zustand without reinventing the wheel? And is there a migration path that lets us run both in parallel rather than a big-bang rewrite?"""

    elif subtopic == "react_query_cache_invalidation":
        return f"""\
**Context:**
Our {_product} uses React Query v5. After a user updates their profile (via `useMutation`), we call `queryClient.invalidateQueries({{ queryKey: ['user', userId] }})`. But the profile header component (which uses the same query key) doesn't refetch — it shows stale data.

**Code:**
```typescript
const {{ mutate }} = useMutation({{
  mutationFn: updateProfile,
  onSuccess: () => {{
    queryClient.invalidateQueries({{ queryKey: ['user', userId] }});
  }},
}});
```

**Observed Issue:**
Invalidation seems to have no effect. React Query DevTools shows the query as "stale" after invalidation, but it doesn't refetch. The component is mounted and visible.

**Specific Ask:**
What conditions must be true for `invalidateQueries` to trigger an active refetch vs. just marking as stale? Does window focus mode or `refetchType` option affect this? And what's the difference between `invalidateQueries` and `refetchQueries` — when would you use each?"""

    else:
        return f"""\
**Context:**
Our {_product} has an optimistic updates pattern for row deletion in the main table. We update the local React Query cache immediately, then fire the DELETE request.

**Code:**
```typescript
const {{ mutate: deleteRow }} = useMutation({{
  mutationFn: (id: string) => api.delete(`/rows/${{id}}`),
  onMutate: async (id) => {{
    await queryClient.cancelQueries({{ queryKey: ['rows'] }});
    const previous = queryClient.getQueryData(['rows']);
    queryClient.setQueryData(['rows'], (old: Row[]) => old.filter(r => r.id !== id));
    return {{ previous }};
  }},
  onError: (_, __, context) => {{
    queryClient.setQueryData(['rows'], context?.previous);
  }},
}});
```

**Observed Issue:**
The optimistic delete works, but when the server returns an error and we rollback, there's a visible flash where the row disappears and then reappears ~300ms later. Users find this confusing. Additionally, if two deletes fire in quick succession before either resolves, the rollback logic reverts to the wrong snapshot.

**Specific Ask:**
How do you handle the concurrent mutation case in optimistic updates — where snapshot A is taken, then mutation B fires and takes snapshot B (which already reflects mutation A's optimistic change), and then A fails and rolls back to its snapshot (which doesn't include B)? Is this a fundamental limitation of per-mutation snapshots?"""


def _make_css(subtopic: str) -> str:
    if subtopic == "layout_shift_cls":
        return f"""\
**Context:**
Our {_product} is failing Core Web Vitals for CLS (Cumulative Layout Shift) — score of {_rc(['0.18', '0.22', '0.15'])} vs. the "good" threshold of 0.1. The main culprits from the CLS debugger appear to be: (1) the data table shifting down when a sticky header renders, and (2) font loading causing text reflow.

**Observed Issue:**
Even with `font-display: swap`, our primary font (Inter) causes a layout shift on first load. And the table's sticky header is rendered client-side (it depends on scroll position) so there's a 1-frame delay before it's positioned correctly.

**Specific Ask:**
For the font CLS: is `font-display: optional` better than `swap` for CLS even though it may not load the font on slow connections? And for the table sticky header: since the height of a sticky element affects layout before it sticks, what's the technique to pre-reserve the space so Chrome's CLS scorer doesn't penalize it?"""

    elif subtopic == "css_in_js_runtime_perf":
        return f"""\
**Context:**
Our {_product} design system uses styled-components v6. In the Profiler, we see ~{_rc(['8ms', '12ms', '10ms'])} spent in styled-components' style injection on every render of our main `DataTable` (which has ~{_rc(['200', '150', '180'])} rows with styled `<Row>` and `<Cell>` components each).

**Observed Issue:**
Styled-components re-generates and injects styles even when no props change. This 8ms doesn't trigger a layout but shows up as scripting time in the Performance tab, adding up to visible jank during scroll.

**Specific Ask:**
Is the runtime CSS injection cost of styled-components inherently unacceptable for high-density list UIs? What's a pragmatic migration path: CSS Modules, Linaria (compile-time CSS-in-JS), or vanilla-extract? We can't rewrite 300 components overnight — is there a hybrid approach where we keep styled-components for layout/typography but use CSS Modules for the perf-critical table rows?"""

    else:
        return f"""\
**Context:**
We're adding a large side panel to our {_product} dashboard that slides in over content. When the panel opens, Chrome DevTools Performance tab shows multiple expensive "Recalculate Style" events taking ~{_rc(['15ms', '20ms', '12ms'])} each on a {_rc(['mid-tier', 'low-end'])} device.

**Code:**
```css
.side-panel {{
  transform: translateX(100%);
  transition: transform 300ms ease;
}}
.side-panel.open {{
  transform: translateX(0);
}}
/* Also: panel has 200+ descendant elements */
```

**Observed Issue:**
The `transform` animation should be on the compositor thread and off the main thread. But the style recalculation is happening on the main thread, causing jank at animation start.

**Specific Ask:**
Even with GPU-accelerated `transform` animations, why would "Recalculate Style" appear as a main-thread bottleneck during the animation? Is it because descendant selector invalidation is being triggered? Would adding `contain: layout style` or `will-change: transform` to the panel (or its descendants) isolate the style scope and prevent cascading recalculations?"""


def _make_testing(subtopic: str) -> str:
    if subtopic == "flaky_e2e_timing":
        return f"""\
**Context:**
Our {_product} CI (GitHub Actions) runs Playwright E2E tests. We have ~{_rc(['180', '200', '150'])} tests. About {_rc(['12', '8', '15'])}% of them fail non-deterministically on CI but always pass locally. The failures are almost always timeout-related: "Locator.click: Timeout 5000ms exceeded".

**Observed Issue:**
The element exists in the DOM when the timeout fires (we've confirmed via screenshots). The issue seems to be that the element is present but not yet interactive — it's behind a loading overlay or mid-animation.

**Specific Ask:**
What's the Playwright-idiomatic way to wait for an element to be both visible AND interactive (not covered by another element)? Is `locator.waitFor({{ state: 'visible' }})` sufficient, or do we need `actionability` checks? And for CI-specific flakiness (likely due to resource pressure), is there a Playwright config pattern (trace-on-retry, slow-mo thresholds, parallelism tuning) that reliably eliminates timing-dependent failures without slowing suite runtime by >20%?"""

    elif subtopic == "msw_vs_fetch_mock":
        return f"""\
**Context:**
Our {_product} Jest test suite has evolved over 2 years. Some older tests mock `fetch` directly via `jest.fn()`, others use MSW (Mock Service Worker) for integration-level tests, and some use both in the same file.

**Observed Issue:**
The mixed approach causes test pollution — MSW handlers bleed between tests if not properly reset, and `jest.fn()` mocks don't cover fetch calls made inside custom hooks that use `axios`. We spend ~{_rc(['2', '3'])} hours/week debugging test pollution issues.

**Specific Ask:**
What's the architectural decision for "MSW vs. direct mock" in a large Jest + RTL codebase? When is MSW the right tool vs. pure `jest.fn()`? And how do you enforce consistent mock cleanup (MSW handler reset, fetch mock restoration) across a large test suite without relying on every test author to remember to call `server.resetHandlers()` in `afterEach`?"""

    else:
        return f"""\
**Context:**
Our {_product} Jest test suite takes ~{_rc(['8', '12', '10'])} minutes to run on CI. We're on Jest 29, `ts-jest`, and ~{_rc(['1200', '900', '1500'])} test files. Build time is fine; it's the test execution itself that's slow.

**Observed Issue:**
`jest --verbose` shows many tests taking 2–4 seconds individually — even simple unit tests. `--showConfig` reveals `testEnvironment: 'jsdom'` globally. Some test files spin up full component trees unnecessarily.

**Specific Ask:**
What's the practical approach to profiling and optimizing a slow Jest suite at this scale? I know `--testEnvironment node` is faster for non-DOM tests — how do we efficiently audit which test files need jsdom vs. can run in node? And for the tests that do need jsdom, are there `jest-environment-jsdom` config options or mock strategies that reduce setup cost per file?"""


# ─── Main Entry Point ────────────────────────────────────────────────────────

_THEME_GENERATORS = {
    "react_internals":  _make_react_internals,
    "performance":      _make_performance,
    "nextjs_advanced":  _make_nextjs,
    "typescript":       _make_typescript,
    "architecture":     _make_architecture,
    "debugging":        _make_debugging,
    "state_management": _make_state_management,
    "css_rendering":    _make_css,
    "testing":          _make_testing,
}


def generate(theme: str, subtopic: str) -> str:
    """
    Generate a question for the given theme and subtopic.
    Returns a formatted string ready to be typed into a chat interface.
    """
    generator = _THEME_GENERATORS.get(theme)
    if not generator:
        raise ValueError(f"Unknown theme: {theme!r}")
    return generator(subtopic).strip()

"""
snippets/q_state.py - 28 State Management questions
"""

Q_STATE = [

"""**Context:**
We're migrating our dashboard from Redux Toolkit to Zustand. The primary motivation is reducing boilerplate. However, a senior engineer argues RTK's structured slice pattern prevents accidental global state sprawl.

**Observed Issue:**
Our Zustand prototype has 3 stores that have gradually merged concerns -- a userStore that now holds both user preferences and notification state. Pattern enforcement requires discipline, not tooling.

**Specific Ask:**
At what scale does Zustand's flexibility become a liability vs. an asset? What are the architectural conventions for keeping Zustand stores focused as a team grows to 15+ engineers? Does RTK's enforced structure (reducers, selectors in slices) provide enough value to justify the boilerplate at 200k DAU scale?""",

"""**Context:**
We're using Jotai for some isolated atomic state in our design system components. Each chart has per-chart state: zoom level, selected legend items, and active tooltip.

**Observed Issue:**
We have 20 charts on one dashboard view, each with 3 atoms = 60 atoms. The Jotai DevTools shows the atom graph is hard to navigate. Some derived atoms re-compute when they shouldn't.

**Specific Ask:**
When is Jotai atom granularity beneficial vs. when should atoms be grouped into a single atom family? How do atom families (atomFamily) differ from multiple independent atoms in Jotai? And how do you write derived atoms that only re-compute when specific upstream atoms change, not when the whole chart state object updates?""",

"""**Context:**
We use React Query for all server state. Our report list has a staleTime of 30 seconds. Users complain that after creating a new report, it doesn't appear in the list until they wait 30 seconds or refresh.

**Observed Issue:**
The mutation creates the report successfully, but the query cache thinks the list data is fresh (within staleTime). It doesn't refetch.

**Specific Ask:**
What's the correct React Query pattern to invalidate and refetch the report list immediately after a mutation succeeds? Does queryClient.invalidateQueries({ queryKey: ['reports'] }) refetch immediately regardless of staleTime? What's the difference between invalidateQueries (marks stale, fetches if component subscribed) vs. refetchQueries (forces refetch regardless)?""",

"""**Context:**
After calling queryClient.invalidateQueries({ queryKey: ['reports'] }) in a mutation's onSuccess, the report list still shows stale data in several components.

**Observed Issue:**
Different components use different query keys for the same report list: ['reports'], ['reports', filter], ['reports', 'recent']. The invalidateQueries call only matches the exact ['reports'] key, leaving the filtered variants stale.

**Specific Ask:**
How does React Query's queryKey matching work with invalidateQueries -- is it exact match only, or prefix-based? How do you design a queryKey hierarchy so that invalidating a parent key also invalidates all child variants? Is the correct approach ['reports', { filter }] with a partial invalidation call?""",

"""**Context:**
We implement optimistic updates for "mark report as favorite" actions. The mutation adds the report to the favorites list optimistically, then confirms with the server.

**Observed Issue:**
Two users rapidly toggle the same report as favorite/unfavorite. The second user's optimistic update is in-flight when the first user's result comes back. The rollback from user 1's failure overwrites user 2's successful optimistic state.

**Specific Ask:**
How do you handle concurrent optimistic updates to the same piece of state in React Query? Is there a pattern using mutation variables + context to track which mutation's rollback should win? Does React Query's built-in onMutate/onError/onSettled mechanism handle concurrent mutations correctly or do you need external coordination?""",

"""**Context:**
We're deciding which state to put in React Query (server state) vs. Zustand (client state). Currently, the active filter, selected rows, and column visibility are in Zustand. Report data is in React Query.

**Observed Issue:**
Some state is ambiguous: the currently expanded report panel (should this reset on page refresh?), the active workspace ID (affects all API calls), and dashboard layout preferences (user-specific, persisted to DB).

**Specific Ask:**
What's the mental model for deciding if a piece of state belongs to "server state" (React Query) vs. "ephemeral client state" (Zustand) vs. "synchronized client state" (localStorage/cookie backed)? For dashboard layout preferences that are user-specific and persisted to DB, which layer should be the source of truth?""",

"""**Context:**
Our dashboard allows filtering by up to 8 criteria. We want the URL to reflect the applied filters so users can share and bookmark filtered views.

**Observed Issue:**
Currently filters are in Zustand. Copying the URL and sharing it doesn't preserve the filters because they're not in the URL. We're debating between useSearchParams (URL state) and Zustand (local state) for filter management.

**Specific Ask:**
What's the architecture for bidirectional URL ↔ filter state synchronization in Next.js 14 App Router? Should the URL be the single source of truth (useSearchParams) with derived Zustand state, or should Zustand be primary with useEffect syncing to the URL? What are the tradeoffs for back/forward navigation behavior?""",

"""**Context:**
Our users have multiple dashboard tabs open simultaneously. When they mark a notification as read in one tab, the other tabs still show it as unread until they refresh.

**Observed Issue:**
Notification state lives in Zustand (in-memory). Changes don't propagate across browser tabs.

**Specific Ask:**
What's the correct mechanism for syncing client-side state across multiple browser tabs? Is BroadcastChannel API the right tool for cross-tab Zustand synchronization? How do you implement it as a Zustand middleware, and what's the behavior when one tab is in the background and receives an event -- does Zustand update and trigger re-renders in the background tab?""",

"""**Context:**
We want to add Redux DevTools support to our Zustand stores for better debugging. The stores are used across 30+ components and debugging state transitions is painful without time-travel.

**Observed Issue:**
Zustand has a devtools middleware but it shows all store mutations in a flat list without action labels. We can tell something changed but not what action caused the change.

**Specific Ask:**
How do you implement meaningful action names in Zustand DevTools? Is the correct pattern to name every setState call in devtools: set(state => ..., false, 'action/incrementCount')? And does Zustand's devtools middleware support time-travel debugging in the same way Redux DevTools does?""",

"""**Context:**
We use Reselect for memoized selectors in our Redux-based store. A selector that computes total unread notifications across all notification types is re-running on every dispatched action, even unrelated ones.

**Code:**
```ts
const selectUnreadCount = createSelector(
  [state => state.notifications],
  (notifications) => notifications.filter(n => !n.read).length
);
```

**Observed Issue:**
state.notifications is a new array reference on most dispatches (even unrelated ones) because the root reducer spreads state. The memoized selector recomputes on every action.

**Specific Ask:**
How do you ensure that state.notifications only produces a new reference when notification data actually changes? Should the notifications reducer use reference equality checks before returning a new array? Or is the fix a structural selector that passes individual notification IDs instead of the whole array?""",

"""**Context:**
Our Redux store has a notifications slice with a flat array of all notifications. Components need to access notifications by ID, filter by type, and count unread. We're also adding relationships (reports → notifications).

**Observed Issue:**
Filtering and finding by ID from a flat array is O(n) on every render. With 500+ notifications, this shows up in the React DevTools profiler. We're also duplicating notification data that's referenced from multiple places.

**Specific Ask:**
Is RTK's createEntityAdapter the correct solution for normalizing a flat array into a record keyed by ID? Walk through how selectById, selectAll, and selectIds from an EntityAdapter differ in their referential stability, and how this affects selector memoization downstream?""",

"""**Context:**
We have a ReportSummary component that derives formatted totals from raw line items in the Redux store. The derivation (format numbers, compute percentages) happens inside the component during render.

**Code:**
```tsx
function ReportSummary({ reportId }) {
  const lineItems = useSelector(state => state.reports[reportId].lineItems);
  const summary = computeSummary(lineItems); // expensive, runs every render
}
```

**Observed Issue:**
computeSummary runs on every render of ReportSummary even when lineItems hasn't changed -- because the selector returns a new array reference after unrelated store updates.

**Specific Ask:**
Should derived state (summary) be computed in a Reselect selector, a useMemo in the component, or stored in the Redux state itself? What's the difference between memoizing in a selector vs. useMemo for this case, and when does putting derived state in Redux become the right answer?""",

"""**Context:**
We migrated a large multi-step form from 15 useState calls to React Hook Form. Validation rules are complex: field B is required only if field A has a specific value.

**Observed Issue:**
Setting up cross-field validation in RHF using watch() causes the entire form to re-render when any watched field changes. We have 30 fields in the form and watching 10 of them for cross-field rules causes noticeable input lag.

**Specific Ask:**
What's the correct React Hook Form pattern for cross-field validation that doesn't cause full form re-renders? Should cross-field rules be in the resolver (Zod schema with .refine()) instead of using watch()? Does RHF's subscribe API or useFormContext with per-field subscriptions solve the performance issue?""",

"""**Context:**
We have a 5-step onboarding wizard in our dashboard. Each step has its own form. Navigation between steps should preserve entered data, and the complete form should submit atomically at the end.

**Observed Issue:**
Currently each step's form is independent. Data is lost when navigating back. We need a shared state for the wizard that persists across step navigation and handles validation per step vs. the whole form.

**Specific Ask:**
What's the architecture for a multi-step form where individual steps validate independently but the whole wizard submits as a single object? Should we use a single React Hook Form instance with step-based fieldset visibility, or multiple forms with a shared Zustand store? What's the tradeoff for data persistence ("go back and edit") and UX?""",

"""**Context:**
Our dashboard has a shopping cart feature for purchasing report credits. The cart needs to persist across browser sessions (localStorage), survive tab closes, and sync across multiple open tabs.

**Observed Issue:**
Zustand with localStorage middleware handles persistence and initial hydration. But tabs don't sync -- adding an item in Tab A doesn't appear in Tab B without a refresh.

**Specific Ask:**
What's the complete architecture for a Zustand store that: (1) hydrates from localStorage on mount, (2) persists all mutations to localStorage, and (3) syncs state changes cross-tab via BroadcastChannel? How do you handle the initial hydration race condition where two tabs start simultaneously and both read the same initial state?""",

"""**Context:**
We're adding undo/redo to our report builder. Users can add, remove, and reorder up to 50 report sections. We want Ctrl+Z / Ctrl+Y support.

**Observed Issue:**
The report state is in Zustand. We could push every state snapshot to a history array, but this is expensive for large reports. We're also concerned about undoing across async operations (e.g., undoing a section addition that triggered an auto-save).

**Specific Ask:**
What's the standard pattern for undo/redo with Zustand that avoids full snapshot copying? Is a command/action-based history (store the inverse operation for each action, not the snapshot) better than structural sharing (Immer + persistent data structures)? How do you handle the UX of "undo an auto-save" -- do operations that trigger side effects get special treatment in undo history?""",

"""**Context:**
Our dashboard has a collaborative editing feature where multiple users can view and annotate the same report. Annotations are synced via WebSocket.

**Observed Issue:**
User A and User B both annotate at the same point simultaneously. The server receives both operations, accepts A's annotation first, then B's. When the confirmed operations arrive at both clients, the local optimistic state conflicts with the server order.

**Specific Ask:**
What's the conflict resolution strategy for collaborative state where multiple users make concurrent mutations? Is Operational Transformation (OT) or CRDT the right model for a document annotation system? At a high level, how would you implement a CRDT-based annotation state in a React app where the local state is always immediately applied and then reconciled with the server?""",

"""**Context:**
We use optimistic updates for report status changes (Pending → Published). The UI immediately shows "Published" before the API confirms.

**Observed Issue:**
When the API call fails (e.g., permission error), React Query rolls back the optimistic state. But between the optimistic update and the rollback, the user may have performed another action based on the "Published" state -- navigating to a page only accessible to published reports.

**Specific Ask:**
How do you design optimistic updates for state transitions where the user can take dependent actions during the optimistic window? Is showing the optimistic state immediately always correct, or should certain high-risk transitions (permission-guarded state changes) use a "pending" visual state instead of assuming success?""",

"""**Context:**
Our dashboard report list supports infinite scroll, fetching 50 items per page. We use React Query's useInfiniteQuery. The query works but the UX has issues.

**Observed Issue:**
When a user scrolls to page 5, then navigates to a detail page and back, React Query refetches all 5 pages sequentially (5 network requests). The list shows a skeleton for several seconds.

**Specific Ask:**
How does React Query handle cache hydration for infinite queries when returning to a previously loaded page? Is there a way to restore the cached pages immediately while revalidating in the background? What's the correct initialPageParam and getNextPageParam pattern for cursor vs. offset-based pagination?""",

"""**Context:**
Our dashboard filter panel has 8 filter controls. The URL should reflect all active filters for shareability. We use useSearchParams in Next.js App Router.

**Observed Issue:**
Every filter change calls router.push() with updated search params, pushing a new History entry. After applying 8 filters, pressing Back 8 times to undo is terrible UX. Users expect Back to go to the previous page, not the previous filter state.

**Specific Ask:**
When should filter state use router.push() (new History entry) vs. router.replace() (replace current entry)? What's the correct UX pattern -- should each filter change replace history (so Back always goes to the previous page), or should there be a concept of "committed" vs. "tentative" filter state where only Applying pushes history?""",

"""**Context:**
We have a DataTable with selectable rows. Selection is stored in a React state as a Set<string> of selected row IDs.

**Observed Issue:**
Every time the user selects/deselects a row, the entire table re-renders because the Set reference changes. We use React.memo on rows but the set is passed as a prop, causing every row to re-render to check if it's selected.

**Specific Ask:**
What's the correct pattern for storing and accessing a "selected items" set in React that scales to 1,000+ rows without full table re-renders? Should selection state move to a Zustand store with per-row granular selectors? Or should each row subscribe to its own selection atom (Jotai) to avoid any cross-row coupling?""",

"""**Context:**
Our dashboard subscribes to a WebSocket feed that pushes entity updates (reports, users, projects). We need to merge incoming WebSocket events into our Zustand store without causing full-table re-renders.

**Observed Issue:**
Each WebSocket message calls zustand setState with a new entities object, triggering all entity-reading components to re-render even if their specific entity didn't change.

**Specific Ask:**
How do you implement a Zustand middleware that processes WebSocket events into normalized entity state while triggering only the affected entity's subscribers? Is the correct pattern entity-keyed selectors (state => state.entities[id]) + Zustand's automatic shallow equality, or do you need a custom subscription mechanism?""",

"""**Context:**
We're experiencing a stale cache issue where different browser tabs have conflicting views of the same data. Tab A sees a report as "Draft", Tab B sees the same report as "Published" because it cached the state from a previous session.

**Observed Issue:**
React Query's cache is in-memory per tab. There's no mechanism to invalidate the other tab's cache when a mutation happens in the current tab.

**Specific Ask:**
What's the architecture for cross-tab cache coherence with React Query? Should mutations broadcast via BroadcastChannel to trigger queryClient.invalidateQueries in other tabs? Is there a risk of invalidation storms (all tabs refetch simultaneously) when there are 10+ tabs open?""",

"""**Context:**
We're evaluating Preact Signals as an alternative to Zustand for fine-grained reactivity in our most performance-sensitive dashboard panels. Signals update only the DOM nodes that read them, bypassing React's virtual DOM diff.

**Observed Issue:**
In our prototype, signals work well for the trade-price ticker (pure value display). But we're unsure how signals interact with React's batching, error boundaries, Suspense, and the broader React ecosystem.

**Specific Ask:**
In a React 18 + Next.js 14 app, what's the practical scope for Preact Signals (@preact/signals-react) before you hit ecosystem compatibility issues? Do signals work inside React Server Components, and what are the SSR implications? Is this an all-or-nothing architectural choice or can signals and React state coexist per-component?""",

"""**Context:**
Our dashboard has a global notification counter shown in the nav. It's computed from multiple sources: unread messages, pending approvals, and system alerts. Each source has its own store.

**Observed Issue:**
The notification counter rerenders 3 times (once per store update) when all three stores update simultaneously after a WebSocket broadcast. This causes a brief counter flicker.

**Specific Ask:**
In Jotai, how do you create a derived atom that depends on atoms from multiple stores without triple-rendering? Does Jotai's batching API handle simultaneous atom updates from external events like WebSocket? Is the correct fix a single flushSync atom update per WebSocket message, or moving to a single normalized store?""",

"""**Context:**
Our dashboard has several confirmation dialogs (delete confirmation, discard changes, etc.) that need to be triggered imperatively from anywhere in the app.

**Observed Issue:**
Currently each dialog is co-located with its trigger. When we need to confirm a delete triggered from a Server Action's success callback, there's no clean way to pop a confirmation dialog from outside React's component tree.

**Specific Ask:**
What's the architecture for a global confirmation dialog that can be triggered imperatively from anywhere including async callbacks, Server Action handlers, or Zustand actions? Is a dialog-queue pattern (Zustand store holds a queue of pending confirmations, a single DialogRenderer at the root drains it) better than an event emitter approach?""",

"""**Context:**
Our dashboard has a toast notification system. Toasts can be triggered from anywhere: form submissions, WebSocket events, Server Action callbacks, and background sync events.

**Observed Issue:**
Our current Zustand toasts store handles deduplication and auto-dismiss. But when multiple events fire simultaneously (e.g., 5 WebSocket events arrive in 100ms), 5 toasts appear at once, overwhelming the user.

**Specific Ask:**
What's the correct UX pattern for high-frequency transient notifications -- batching multiple events into a single summary toast, grouping by type, or a notification center drawer? And at the implementation level, how do you debounce or coalesce Zustand toast additions that happen within a short time window?""",

"""**Context:**
We store user theme preference (light/dark/system) in localStorage and Zustand. On page load, there's a flash because Zustand initializes to 'light' before the localStorage hydration hook runs.

**Observed Issue:**
The component tree renders with the default 'light' theme, then switches to 'dark' after useEffect runs and reads localStorage. This causes a visible flash and a CLS hit.

**Specific Ask:**
How do you eliminate the theme flash on initial load for a localStorage-persisted preference? Is an inline script that reads localStorage and sets the theme class (before React hydrates) the only reliable fix? How does next-themes handle this in App Router, and does Zustand's persist middleware have a way to populate initial state synchronously on the server?""",

]

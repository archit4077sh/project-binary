"""
snippets/q_state.py — 28 FRESH State Management questions (mix of debugging + code generation)
Zero overlap with archived set.
"""

Q_STATE = [

"""**Task (Code Generation):**
Implement a `createSlice` helper (Redux Toolkit–style) for Zustand that reduces boilerplate:

```ts
const userSlice = createSlice({
  name: 'user',
  initialState: { data: null as User | null, loading: false },
  actions: {
    setUser: (state, user: User) => ({ ...state, data: user }),
    setLoading: (state, loading: boolean) => ({ ...state, loading }),
    reset: () => ({ data: null, loading: false }),
  },
});

const useUserStore = create(userSlice);
const { setUser, setLoading } = useUserStore.getState();
```

Show the `createSlice` implementation with TypeScript types that infer action parameters from the reducer functions.""",

"""**Debug Scenario:**
A Zustand store is initialized with data fetched from an API. When the component mounts, the store has the correct data. But when the user navigates away and returns, the store shows the initial empty state — the fetched data is gone.

Investigation shows the store is defined inside the component:
```ts
function Dashboard() {
  const useStore = create(() => ({ data: [] })); // Re-created every render!
}
```

Explain why defining a Zustand store inside a component body causes a new store instance on every render, and show the correct pattern for stores that need initialization data.""",

"""**Task (Code Generation):**
Build a `useSyncedState<T>` hook that keeps state synchronized across browser tabs using `BroadcastChannel`:

```ts
const [theme, setTheme] = useSyncedState<'light' | 'dark'>('theme-channel', 'light');
// When setTheme('dark') is called in Tab A, Tab B automatically updates
```

Requirements:
- Creates a `BroadcastChannel` with the given name
- Broadcasts on every state change
- Receives broadcasts from other tabs and updates local state
- Doesn't echo back its own messages (avoid infinite loops)
- Cleans up the channel on unmount

Show the full implementation.""",

"""**Debug Scenario:**
React Query v5 is used for server state. A mutation updates a user's profile and invalidates the `['user', userId]` query. The profile header component (which uses this query) re-fetches correctly. But a sidebar component that renders the same user data doesn't update.

```ts
// Sidebar uses:
const { data: user } = useQuery({ queryKey: ['user', userId], queryFn: getUser });

// Profile uses:
const { data: user } = useQuery({ queryKey: ['user', userId], queryFn: getProfile });
```

Diagnose: the sidebar uses `getUser` and the profile uses `getProfile` — different `queryFn` but same `queryKey`. Explain how React Query handles this case and whether two components with identical keys but different `queryFn` share cache.""",

"""**Task (Code Generation):**
Implement a `useStorageState<T>` hook that syncs to any storage backend (localStorage, IndexedDB, AsyncStorage for React Native):

```ts
// localStorage backend:
const [token, setToken] = useStorageState('auth-token', null, localStorageAdapter);

// IndexedDB backend:
const [offline-data, setData] = useStorageState('data', [], idbAdapter);
```

Show the `StorageAdapter` interface, a `localStorageAdapter` implementation, and the hook. The hook should handle async storage backends (where reads/writes return Promises) by showing an initial loading state.""",

"""**Debug Scenario:**
A Redux Toolkit store uses `createAsyncThunk` for data fetching. After a network error, the UI shows an error message. The user dismisses the error and retries — but the retry immediately shows the previous error without making a new network request.

```ts
// Slice:
extraReducers: builder => {
  builder.addCase(fetchData.rejected, (state, action) => {
    state.error = action.error.message;
    state.status = 'failed';
  });
}
// Retry:
dispatch(fetchData()); // status is still 'failed', so UI shows error immediately
```

The status is 'failed' before the retry resolves. Show the correct pattern: clearing error state on `fetchData.pending`, and the UX implication of the loading → error → loading transition.""",

"""**Task (Code Generation):**
Build a `useFormState` hook for complex multi-field forms with:
- Field-level validation (runs on blur, shows on submit)
- Cross-field validation (e.g., `endDate > startDate`)
- `isDirty`, `isValid`, `isSubmitting` flags
- Array fields (add/remove rows dynamically)
- `reset(values)` that resets to given values without triggering validation

```ts
const form = useFormState({
  fields: { name: '', tags: [] as string[], startDate: '', endDate: '' },
  validate: (values) => ({ endDate: values.endDate < values.startDate ? 'Must be after start' : null })
});
```""",

"""**Debug Scenario:**
A Jotai atom is derived from another atom using `atom(get => ...)`. When the base atom updates, the derived atom re-computes — but components subscribed to the derived atom don't re-render.

```ts
const baseAtom = atom<User | null>(null);
const nameAtom = atom((get) => get(baseAtom)?.name ?? '');

// In component:
const name = useAtomValue(nameAtom); // doesn't update when baseAtom changes!
```

Investigate: is this a Jotai version issue, a component wrapping issue (missing Provider), or an atom scope issue? Show the common causes of Jotai derived atoms not triggering subscribing components and how to debug with Jotai DevTools.""",

"""**Task (Code Generation):**
Implement an `operationQueue` for offline-first apps that queues mutations when offline and replays them when connectivity is restored:

```ts
const queue = useOperationQueue({
  onOnline: async (operations) => {
    for (const op of operations) await replayOperation(op);
  },
});

// Called even when offline:
queue.enqueue({ type: 'CREATE_NOTE', payload: { title, content } });
```

Show the queue implementation using IndexedDB for persistence (so queued ops survive browser refresh), the online/offline detection, and conflict resolution if the server already has a conflicting operation.""",

"""**Debug Scenario:**
An app uses React Context for cart state. The cart has 50 items. Updating the quantity of one item causes all 50 `<CartItem>` components to re-render, shown in the Profiler.

The items are correctly memoized with `React.memo`, and the `onQuantityChange` callback is wrapped in `useCallback`. The Profiler shows items re-render because the `cart` object reference changes on every update.

```ts
const [cart, setCart] = useState<CartItem[]>([]);
// Context value:
<CartContext.Provider value={{ cart, updateItem, removeItem }}>
```

Show the fix using separate contexts (data vs actions), or `useMemo` for the context value, and explain why separating reads from writes is the key insight.""",

"""**Task (Code Generation):**
Build a `useCommandHistory` hook for implementing undo/redo with the Command pattern:

```ts
interface Command<T> {
  execute: (state: T) => T;
  undo: (state: T) => T;
  description: string;
}

const { state, execute, undo, redo, history } = useCommandHistory<TextDocument>(initialDoc);

execute({
  description: 'Insert text at cursor',
  execute: (doc) => insertText(doc, cursor, text),
  undo: (doc) => deleteText(doc, cursor, text.length),
});
```

Show the implementation with max history depth, batch command support (multiple actions as one undo step), and a history panel component.""",

"""**Debug Scenario:**
Valtio (proxy-based state) is used for a real-time dashboard. Deeply nested state mutations work correctly in dev mode but in production, some components don't update after mutations to nested properties.

```ts
const state = proxy({ dashboard: { filters: { status: 'all' } } });
// In action:
state.dashboard.filters.status = 'active'; // works in dev, sometimes not in prod
```

Investigate: does Valtio require `structuredClone` or spread for nested updates, or does it track mutations via Proxy traps at all depths? Explain the difference between Valtio's proxy and MobX's observable for deeply nested state.""",

"""**Task (Code Generation):**
Implement `createContextStore<T>` — a factory that creates a React Context-based store with Zustand-like selector subscriptions:

```ts
const UserStore = createContextStore({ name: '', role: 'user' as 'user' | 'admin' });

// In component — only re-renders when 'role' changes:
const role = UserStore.useSelector(s => s.role);
const { setState } = UserStore.useStore();
```

The selector must use `Object.is` comparison to prevent re-renders for equal values. Show the implementation using `useRef` + `useSyncExternalStore`.""",

"""**Debug Scenario:**
An e-commerce app uses Redux for cart state. The `cartItems` selector is an expensive computation (applies discounts, calculates totals). The selector runs on every action dispatch — including unrelated actions like `SET_MODAL_OPEN`.

```ts
const cartTotal = useSelector(state => 
  state.cart.items.reduce((total, item) => total + calculatePrice(item), 0)
);
```

Show how `reselect` memoizes this selector with `createSelector`, why memoization depends on input selector reference equality, and the correct pattern when `calculatePrice` itself depends on state from another slice.""",

"""**Task (Code Generation):**
Build a `useWebSocketStore` that provides real-time state updates via WebSocket while maintaining optimistic updates for mutations:

```ts
const { data: reports, updateReport, isConnected } = useWebSocketStore('/ws/reports');

// Optimistic update:
updateReport(id, { status: 'closed' }); // instantly updates UI
// If WS server sends back conflicting data, reconcile:
// Server data wins; show conflict notification
```

Show the Zustand store setup, the WebSocket subscription logic, the optimistic update + rollback pattern, and the conflict detection.""",

"""**Debug Scenario:**
Using React Query's `useInfiniteQuery` for a paginated list, the `fetchNextPage` function is called but the new page data is appended to the top of the list instead of the bottom.

```ts
const { data, fetchNextPage } = useInfiniteQuery({
  queryKey: ['items'],
  queryFn: ({ pageParam = 0 }) => fetchPage(pageParam),
  getNextPageParam: (lastPage) => lastPage.nextCursor,
});

// Rendering:
data.pages.flatMap(page => page.items).reverse() // Bug: reversal here
```

Diagnose how the `reverse()` combined with `getNextPageParam` causes the visual ordering problem, and show the correct rendering order with correct cursor-based pagination configuration.""",

"""**Task (Code Generation):**
Implement a `useRealtimeQuery<T>` hook that combines initial data from React Query with real-time WebSocket updates:

```ts
const { data: orders } = useRealtimeQuery<Order[]>({
  queryKey: ['orders'],
  queryFn: fetchOrders,
  wsChannel: 'orders:updates',
  onMessage: (current, event) => {
    if (event.type === 'ORDER_CREATED') return [...current, event.order];
    if (event.type === 'ORDER_UPDATED') return current.map(o => o.id === event.order.id ? event.order : o);
    return current;
  },
});
```

Show the implementation, how it keeps the React Query cache in sync with WebSocket events, and how to handle the race condition between initial fetch and incoming events during load.""",

"""**Debug Scenario:**
A Zustand middleware called `persist` is used to save store state to localStorage. After the user logs out and a new user logs in, the previous user's data briefly appears because the persisted state loads before the login completes.

```ts
const useStore = create(
  persist(
    (set) => ({ user: null, preferences: {} }),
    { name: 'app-store', storage: createJSONStorage(() => localStorage) }
  )
);
```

Design a secure logout flow that: clears the persisted state, resets all Zustand stores, and prevents the stale state flash. Show how to handle Zustand's `persist` hydration timing relative to the auth check.""",

"""**Task (Code Generation):**
Build a `useModalState` hook that manages a stack of modals with:
- `push(modalId, props)` — opens a new modal on top of the stack
- `pop()` — closes the top modal
- `close(modalId)` — closes a specific modal anywhere in the stack
- Keyboard handler: `Escape` closes the top modal
- Prevents body scroll when any modal is open
- Supports animated exit (modal stays in DOM until animation completes)

Show the hook, the `ModalStack` provider, and a `<ModalRenderer>` that renders all active modals.""",

"""**Debug Scenario:**
A team uses Immer with Redux Toolkit's `createSlice`. A reducer that filters an array is accidentally mutating state instead of returning a new array, but Immer swallows the error silently.

```ts
reducers: {
  removeItem: (state, action) => {
    state.items = state.items.filter(item => item.id !== action.payload);
    // Should work — but combined with another line:
    return state; // Bug: returning draft state breaks Immer
  }
}
```

Explain Immer's two modes (mutate draft vs return new value) and why returning the draft causes subtle bugs. Show the correct Immer reducer patterns and how to detect this bug with Immer's `current()` helper.""",

"""**Task (Code Generation):**
Implement a `useAutoSave` hook that automatically saves form data to the server after a period of inactivity:

```ts
const { isSaving, lastSaved, error } = useAutoSave({
  data: formValues,
  saveFn: async (data) => api.patch('/drafts/1', data),
  debounce: 2000, // save 2s after last change
  onConflict: (localData, serverData) => resolveConflict(localData, serverData),
});
```

Features:
- Debounced save on data change
- Shows "Saving..." and "Last saved at HH:MM" in UI
- Detects server conflicts (server version != local version)
- Retries on network failure (exponential backoff)""",

"""**Debug Scenario:**
An RTK Query endpoint has `providesTags: [{ type: 'User', id: 'LIST' }]`. A mutation has `invalidatesTags: [{ type: 'User', id: 'LIST' }]`. After the mutation fires, the user list doesn't refresh.

```ts
// Mutation:
invalidatesTags: (result) => result ? [{ type: 'User', id: 'LIST' }] : []
```

The `invalidatesTags` function returns an empty array when `result` is falsy — and the mutation's `result` is undefined on success (the endpoint returns 204 No Content). Fix the tag invalidation and explain RTK Query's tag system including list vs entity tags.""",

"""**Task (Code Generation):**
Implement a finite state machine using XState v5 for a multi-step file upload flow:

```
idle → selecting → uploading → processing → success
                ↘ cancelled        ↘ failed → retrying → uploading
```

Show:
1. The XState machine definition with guards and actions  
2. A `useUpload` hook wrapping the machine
3. A `<UploadProgress>` component driven by the machine state
4. How to cancel an in-progress upload and clean up resources""",

"""**Debug Scenario:**
React Query is set up with `staleTime: Infinity` for configuration data that rarely changes. After a backend deployment updates the config, users don't see the new values until they hard refresh.

The team adds `staleTime: 5 * 60 * 1000` (5 minutes) to fix this. But now every component instance that mounts re-fetches the config if 5 minutes have passed, causing 10 simultaneous identical API calls.

Explain React Query's deduplication of concurrent fetches for the same query key, why in-flight deduplication works but stale query deduplication doesn't save all component mounts, and the correct `staleTime` + `gcTime` combination for shared config data.""",

"""**Task (Code Generation):**
Build a `useOptimisticList<T>` hook for managing lists with optimistic CRUD operations:

```ts
const { items, addItem, updateItem, removeItem, pendingIds } = useOptimisticList<Product>({
  queryKey: ['products'],
  mutations: {
    add: createProduct,
    update: updateProduct,
    remove: deleteProduct,
  },
});
```

- `addItem` shows the item immediately with a temp ID, replaces with server ID on success
- `updateItem` shows changes immediately, reverts on failure
- `removeItem` hides the item immediately, restores on failure
- `pendingIds` tracks which items have in-flight mutations (for loading indicators)""",

"""**Debug Scenario:**
A server-side Redux store is created per-request in a Next.js API route. But some production users see state from other users' requests — a state leakage bug.

```ts
// lib/store.ts
export const store = configureStore({ reducer }); // Module-level singleton!
```

This is the same bug as the earlier Next.js server component example but in Redux. If multiple concurrent requests share the same store, dispatching actions for User A's request mutates state that User B's request then reads. Show the correct per-request store pattern and explain how Next.js's module bundling makes server-side singletons dangerous.""",

"""**Task (Code Generation):**
Build a `usePageLeaveGuard` hook that prevents the user from accidentally navigating away from a form with unsaved changes:

```ts
const { isDirty, setDirty } = usePageLeaveGuard({
  message: 'You have unsaved changes. Leave anyway?',
  enabled: formIsDirty,
});
```

Requirements:
- Intercepts browser `beforeunload` event (for tab close / refresh)
- Intercepts Next.js client-side navigation via `router.events` (App Router)
- Shows a confirmation dialog before allowing navigation
- Automatically disables when the form is saved (`enabled: false`)
- TypeScript-compatible with `useFormState` or react-hook-form's `isDirty`""",

"""**Debug Scenario:**
A `useShoppingCart` hook uses `useReducer` internally. The `ADD_ITEM` action is dispatched from a `<ProductCard>` component deep in the tree. After adding items rapidly by clicking multiple cards, some additions are lost — the cart shows fewer items than expected.

```ts
onClick={() => dispatch({ type: 'ADD_ITEM', payload: product })}
// Multiple rapid clicks: only 1 of 3 items added
```

The bug occurs because `React.StrictMode` double-invokes reducers in development — but the symptom appears in production too. Diagnose: is this a reducer purity issue (side effects inside reducer), an event handler closure issue, or a batching timing issue? Show a reproducible example and the fix.""",

]

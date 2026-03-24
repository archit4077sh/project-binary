"""
snippets/q_state.py — BATCH 6: 55 brand-new State Management questions
Zero overlap with batches 1-5 archives.
"""

Q_STATE = [

"""**Task (Code Generation):**
Implement a `createAtomFamily<T>` for Jotai-style atom families with automatic cleanup:

```ts
const productAtomFamily = createAtomFamily<string, ProductState>({
  initializeAtom: (id) => atom({ id, loading: true, data: null, error: null }),
  areEqual: (a, b) => a === b,
  ttl: 10 * 60 * 1000,  // remove atom from registry after 10 min of no subscribers
});

// In component:
const [product, setProduct] = useAtom(productAtomFamily(productId));

// Cleanup:
productAtomFamily.remove(productId); // manual removal
productAtomFamily.get(productId);    // get or create atom for id
```

Show: the `Map<Key, Atom<T>>` registry, TTL cleanup using `WeakRef` + `FinalizationRegistry`, the `useEffect` cleanup path when the last subscriber unmounts, and TypeScript generic type inference for the atom value.""",

"""**Task (Code Generation):**
Build a `createOptimisticQueue` for managing multiple concurrent optimistic updates with undo:

```ts
const { apply, confirm, reject, undo } = createOptimisticQueue<CartState>();

// User adds item:
const opId = apply(state => addItemToCart(state, item));
// UI shows item immediately (optimistic)

// Server confirms:
await api.addToCart(item);
confirm(opId);   // finalizes the optimistic update

// Server rejects:
reject(opId);    // rolls back only this update, keeps others
undo(opId);      // user-initiated undo (moves op to reject pile)
```

Show: the queue of pending operations (each with a `before` snapshot for rollback), applying operations in order on the base state, rolling back a single operation (re-applying all others on top of the base), and TypeScript typing for `apply`'s callback return type.""",

"""**Task (Code Generation):**
Implement a `useSharedWorkerState<T>` hook for state synchronized across browser tabs via SharedWorker:

```ts
// In every tab:
const [cart, setCart, isLeader] = useSharedWorkerState<CartState>('cart', {
  initialState: { items: [], total: 0 },
  workerUrl: '/workers/state-worker.js',
  onConflict: 'last-write-wins',
});

setCart(state => addItem(state, product));
// The update is broadcast to all open tabs via SharedWorker
```

Show: the `SharedWorker` message protocol (subscribe/update/unsubscribe messages), state broadcast to all connected ports on update, the leader election mechanism (`isLeader` — the first tab to connect is the leader), and fallback to `localStorage` events when `SharedWorker` is unavailable.""",

"""**Task (Code Generation):**
Build a `createHydratableStore<T>` that initializes from server-side props and dehydrates back:

```ts
// Server (Next.js getServerSideProps):
const store = createHydratableStore<AppState>();
const state = await buildInitialServerState(req);
const dehydrated = store.dehydrate(state);
// Pass to page: { props: { dehydratedState: dehydrated } }

// Client:
const store = createHydratableStore<AppState>();
store.hydrate(dehydratedState); // restore server state without network requests
```

Show: the `dehydrate` function serializing state to a plain JSON-serializable object, `hydrate` restoring it, handling circular references in state (use `superjson`), the React 18 `hydrateRoot` integration, and version field in dehydrated state to handle schema migrations.""",

"""**Task (Code Generation):**
Implement a `createMutationPipeline<Input, Output>` for chained data transformations with rollback:

```ts
const saveProfile = createMutationPipeline<ProfileInput, Profile>([
  { name: 'validate',  fn: validateProfileData },
  { name: 'upload',    fn: uploadProfilePhoto,  rollback: deleteUploadedPhoto },
  { name: 'save',      fn: saveToDatabase,      rollback: deleteFromDatabase },
  { name: 'notify',    fn: sendWelcomeEmail,     rollback: null }, // no rollback needed
]);

const result = await saveProfile.execute(profileData);
if (!result.success) {
  // All steps with rollback functions have been called in reverse order
  console.log('Failed at step:', result.failedStep, result.error);
}
```

Show: sequential step execution with context passing, rollback in reverse order on failure, TypeScript's pipeline type propagation (each step's output feeds into the next), and `result.steps` for debugging (which steps completed before failure).""",

"""**Task (Code Generation):**
Build a `useCollaborativeState<T>` hook for real-time collaborative editing using CRDT:

```ts
const { state, update, peers } = useCollaborativeState<DocumentState>(roomId, {
  initialState: document,
  crdt: 'yjs',            // Uses Yjs CRDT library under the hood
  transport: 'websocket',
  awareness: {
    username: currentUser.name,
    cursor: null,
  },
});

// Conflict-free update (merged automatically with other users' changes):
update(doc => {
  doc.title = 'New Title'; // Yjs handles concurrent edits
});
```

Show: Yjs `Y.Doc` and `Y.Text`/`Y.Map`/`Y.Array` shared types, WebSocket provider (`y-websocket`), awareness protocol for cursor positions, and undo manager (`new Y.UndoManager(yType)`) for collaborative undo (only undoes local changes).""",

"""**Task (Code Generation):**
Implement a `createZustandPersist<T>` with multiple storage adapters and migration:

```ts
const useStore = create(
  persist<AppState>(
    (set) => ({
      user: null,
      preferences: defaultPreferences,
      setUser: (user) => set({ user }),
    }),
    {
      name: 'app-store',
      storage: createJSONStorage(() => window.matchMedia?.('(storage-type: indexeddb)').matches
        ? indexedDBStorage    // large state
        : localStorage        // small state
      ),
      version: 3,
      migrate: (persistedState, version) => {
        if (version === 1) return migrateV1toV2(persistedState);
        if (version === 2) return migrateV2toV3(persistedState);
        return persistedState;
      },
      partialize: (state) => ({ preferences: state.preferences }), // only persist preferences
    }
  )
);
```

Show: the Zustand `persist` middleware, `partialize` for selective persistence, the `migrate` function called when the stored version doesn't match current, and `onRehydrateStorage` for post-hydration initialization.""",

"""**Task (Code Generation):**
Build a `createQueryCache<T>` with React concurrent mode compatibility:

```ts
const queryCache = createQueryCache<{ [url: string]: unknown }>({
  maxSize: 100,
  strategy: 'lru',
  suspense: true,
});

function ProductList() {
  // Suspense: throws Promise on cache miss, resolves when loaded:
  const products = queryCache.read('/api/products');
  return products.map(p => <Product key={p.id} product={p} />);
}

// Pre-populate cache:
await queryCache.preload('/api/products', () => fetch('/api/products').then(r => r.json()));
```

Show: the Suspense protocol (throw a Promise, React catches it and shows Suspense fallback), `read()` returning cached value synchronously OR throwing the in-flight Promise, LRU eviction, and `useSyncExternalStore` for safe concurrent reads.""",

"""**Task (Code Generation):**
Implement a `createReduxToolkitAdapter` for migrating a legacy Redux store to a modern RTK pattern:

```ts
// Legacy:
const ADD_TODO = 'ADD_TODO';
const addTodo = (text: string) => ({ type: ADD_TODO, payload: text });
const todoReducer = (state = [], action) => { ... };

// Migration adapter — creates RTK slice with same action types:
const todoSlice = createReduxToolkitAdapter({
  name: 'todos',
  legacyActions: { ADD_TODO: addTodo, REMOVE_TODO: removeTodo },
  legacyReducer: todoReducer,
  migrate: {
    ADD_TODO: { toRTK: (payload) => ({ text: payload }), fromRTK: (p) => p.text },
  },
});
```

Show: the RTK `createSlice` equivalent, backward-compatible action creators (legacy code can still dispatch `{ type: 'ADD_TODO', payload }` and the store handles it), and the migration path for slowly transitioning action creators to RTK style.""",

"""**Task (Code Generation):**
Build a `useGraphQLSubscription` hook that handles WebSocket-based GraphQL subscriptions:

```ts
const { data, error, loading } = useGraphQLSubscription<NewMessageData>({
  query: `
    subscription OnNewMessage($channelId: ID!) {
      newMessage(channelId: $channelId) { id content author { name avatar } sentAt }
    }
  `,
  variables: { channelId },
  onData: (msg) => scrollToBottom(),
  reconnectOnError: true,
  onComplete: () => setShowReconnecting(true),
});
```

Show: the GraphQL over WebSocket protocol (`graphql-ws`), subscription lifecycle (`subscribe` → receive data → `complete` → `unsubscribe`), reconnection with exponential backoff, and integrating with Apollo Client's `useSubscription` vs custom implementation comparison.""",

"""**Task (Code Generation):**
Implement a `createFormOrchestrator` for multi-step forms with shared state and validation:

```ts
const { FormStep, useFormData, navigate, submit } = createFormOrchestrator({
  steps: ['personal', 'payment', 'review'],
  schema: {
    personal: PersonalInfoSchema,
    payment:  PaymentInfoSchema,
  },
  onSubmit: async (allData) => api.checkout(allData),
  persistence: 'sessionStorage',
});

// In Step1:
function PersonalStep() {
  const { data, update, errors } = useFormData('personal');
  return <PersonalForm data={data} onChange={update} errors={errors} />;
}
```

Show: the step data isolated in separate Zustand slices, cross-step data access (`useFormData('all')`), validation on navigate-next (block progression if invalid), resuming from `sessionStorage` on page refresh, and the progress indicator state.""",

"""**Task (Code Generation):**
Build a `createImmutableStateProxy<T>` that prevents accidental mutations of shared state:

```ts
const state = createImmutableProxy({
  user: { name: 'Alice', preferences: { theme: 'dark' } },
  cart: { items: [], total: 0 },
});

state.user.name = 'Bob'; // TypeError: Cannot assign to read only property
state.cart.items.push({ id: '1' }); // TypeError: Cannot add property 0 — read only

// Only allowed via the update function:
const nextState = state.$update(draft => {
  draft.user.name = 'Bob'; // Immer-style
  draft.cart.items.push({ id: '1' });
});
// nextState: new immutable proxy with updated values
// state: unchanged
```

Show: `Object.freeze` for full deep freezing (runtime only), ES6 `Proxy` handler intercepting `set` and `deleteProperty`, integration with `immer`'s `produce` for the `$update` method, and TypeScript's `DeepReadonly<T>` for compile-time protection.""",

"""**Task (Code Generation):**
Implement a `createOfflineQueue` for queueing operations while offline and syncing when reconnected:

```ts
const offlineQueue = createOfflineQueue({
  storage: indexedDB,
  syncEndpoint: '/api/sync',
  conflictResolution: 'server-wins',
  onSync: (syncedOps) => store.dispatch(applySyncedOps(syncedOps)),
});

// User adds items while offline:
offlineQueue.enqueue({ op: 'CREATE', entity: 'todo', data: { text: 'Buy groceries' } });

// When back online:
navigator.onLine → offlineQueue.flush(); // sends queued ops to server in order
```

Show: `navigator.onLine` + `window.addEventListener('online', ...)`, serializing operations to IndexedDB, the sync protocol (send batch of ops, server returns conflict resolution result), and `offlineQueue.retry()` for failed syncs.""",

"""**Task (Code Generation):**
Build a `createContextSelector<T>` to prevent over-rendering when using React Context:

```ts
const StoreContext = createContextSelector<AppState>({
  Provider: ({ children }) => {
    const store = useReducer(rootReducer, initialState);
    return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>;
  },
});

// Subscribes only to the user slice:
const user = StoreContext.useSelector(state => state.user);
// Only re-renders when state.user changes (not on unrelated state changes)
```

Show: the `use-context-selector` library approach, implementing with `useMemo` + `useRef` + `useReducer` to compare selected slices, the performance comparison vs naive Context (no selector: rerenders all consumers), and `shallowEqual` for array/object selectors.""",

"""**Task (Code Generation):**
Implement a `createReactiveComputed<T>` for derived state that auto-tracks dependencies:

```ts
const store = createReactiveStore({ count: 0, multiplier: 2, name: 'Alice' });

// Auto-tracks: reads store.count and store.multiplier inside
const doubled = createComputed(() => store.count * store.multiplier);
// doubled.value: auto-recomputes only when count OR multiplier changes

const greeting = createComputed(() => `Hello, ${store.name}!`);
// greeting.value: auto-recomputes only when name changes

// Computed depending on computed:
const formattedDoubled = createComputed(() => `${doubled.value}x`);

store.count = 5; // doubled and formattedDoubled auto-update, greeting does NOT
```

Show: the MobX-style observable tracking using a global `currentComputed` stack, `Proxy` on the store to detect property reads during computation, dependency deregistration when deps change, and `reaction(() => greeting.value, (val) => console.log(val))` for side effects.""",

# ── Debugging ─────────────────────────────────────────────────────────────────

"""**Debug Scenario:**
A Redux store's selector causes infinite re-renders because it returns a new array every time:

```ts
const selectVisibleTodos = (state: RootState) =>
  state.todos.filter(todo => !todo.completed);

// In component:
const todos = useSelector(selectVisibleTodos);
// Re-renders on every dispatch — filter() always returns a new array!
```

`useSelector` uses reference equality by default — a new array reference on every call triggers a re-render. Show: using `createSelector` from `reselect` to memoize the filtered result (only recomputes when `state.todos` reference changes), the `shallowEqual` second argument to `useSelector` for arrays, and the performance impact of over-rendering.""",

"""**Debug Scenario:**
Zustand's `useStore` hook re-renders a component even though the selected slice hasn't changed:

```ts
const useStore = create<AppState>((set) => ({
  user: { name: 'Alice', role: 'admin' },
  cart: { items: [], total: 0 },
}));

// Component only needs user.role:
function RoleDisplay() {
  const user = useStore(state => state.user); // Rerenders when cart changes!
  return <span>{user.role}</span>;
}
```

Selecting the entire `user` object causes re-renders when any part of `user` or other state changes, because the selector might return the same object (not a problem) — but if `user` is replaced entirely when something else changes, it re-renders. Show: using a more specific selector (`state => state.user.role`), `useShallow` from Zustand for object selectors, and why Zustand's equality check (`Object.is` by default) matters.""",

"""**Debug Scenario:**
React Query's `useQuery` shows stale data after a mutation even though `invalidateQueries` is called:

```ts
const mutation = useMutation({
  mutationFn: updateUser,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['user'] });
  },
});

// But the component still shows the old data!
const { data: user } = useQuery({
  queryKey: ['users', userId], // Different key than invalidated!
  queryFn: () => fetchUser(userId),
});
```

`invalidateQueries({ queryKey: ['user'] })` matches queries where the key starts with `'user'`, but the actual key is `['users', userId]` (plural). Show: changing `invalidateQueries` key to match (`['users']`), using `queryClient.invalidateQueries({ queryKey: ['users', userId], exact: true })` for exact matching, and setting up React Query Devtools to inspect the current query cache and keys.""",

"""**Debug Scenario:**
Jotai atoms cause unexpected behavior when the atom is defined inside a React component:

```tsx
function Counter() {
  const countAtom = atom(0); // New atom instance on every render!
  const [count, setCount] = useAtom(countAtom);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

A new `atom(0)` is created on every render — each render has a different atom, so the count always shows 0. Show: defining atoms at module level (outside components), using `atomFamily` for instance-specific atoms keyed by ID, and `atomWithReset` if the atom should reset to initial value on demand.""",

"""**Debug Scenario:**
A Vuex (or similar centralized store) has a getter that depends on an expensive computation and re-runs too often:

```ts
// Vuex getter:
const getters = {
  filteredProducts: (state) => {
    return state.products
      .filter(p => p.category === state.activeCategory) // Runs on any state change!
      .sort((a, b) => a.price - b.price);
  },
};
```

Vuex getters are memoized by default (cached until reactive dependencies change) — but `state.products` and `state.activeCategory` change frequently. Show: splitting into two getters (one for filter, one for sort) so the sort only re-runs when filtered results change, using `reselect` with Vuex as an alternative, and logging getter recalculation counts to identify hot spots.""",

"""**Debug Scenario:**
An Redux Toolkit `createAsyncThunk` shows loading state even after the request completes:

```ts
const fetchUser = createAsyncThunk('user/fetch', async (userId: string) => {
  const response = await api.getUser(userId);
  return response.data;
});

// Reducer:
builder.addCase(fetchUser.fulfilled, (state, action) => {
  state.user = action.payload;
  // BUG: forgot to set loading back to false!
});
builder.addCase(fetchUser.pending, (state) => {
  state.loading = true;
});
```

Show: adding `state.loading = false` in both `fulfilled` and `rejected` cases, using RTK's `createSlice.extraReducers` pattern, and the `createAsyncThunk` lifecycle — `pending` → `fulfilled`/`rejected`, both of which should reset the loading state.""",

"""**Debug Scenario:**
A React app uses Context API and all consumers re-render whenever any value in the context changes, even if they only use a small part:

```tsx
const AppContext = createContext({ user: null, theme: 'dark', notifications: [] });

function Header() {
  const { theme } = useContext(AppContext); // Re-renders when notifications changes!
  return <nav className={theme}>...</nav>;
}
```

Context re-renders ALL consumers on every value change. Show: splitting into multiple contexts (`UserContext`, `ThemeContext`, `NotificationContext`) so each consumer only subscribes to relevant changes, using `use-context-selector` for selector-based context consumption, and Zustand/Jotai as alternatives that don't have this problem.""",

"""**Debug Scenario:**
A developer uses `useReducer` but the dispatch function causes a stale closure inside a callback:

```ts
const [state, dispatch] = useReducer(reducer, initial);

const handleSave = useCallback(async () => {
  await api.save(state.draft); // state is stale! captured at callback creation
  dispatch({ type: 'SAVE_SUCCESS' });
}, []); // empty deps — state is always the initial value
```

`state` is captured at `useCallback` creation time with empty deps. Show: adding `state` to deps (but then `handleSave` changes on every render), using `useRef` to hold a mutable reference to the latest state (`stateRef.current = state`), or passing `state.draft` as a parameter to avoid the closure.""",

"""**Debug Scenario:**
An `immer`-based slice mutates state in a way that causes TypeScript to lose type safety:

```ts
const todosSlice = createSlice({
  name: 'todos',
  initialState: [] as Todo[],
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      state.push({ id: Date.now(), text: action.payload, done: false });
      // state is a Proxy (Draft<Todo[]>) — TypeScript treats it as Todo[]
      // But what if we accidentally do:
      return [...state, { id: '1', text: 'test', done: false }];
      // MIXED! Both return AND mutation — the return value is ignored!
    },
  },
});
```

In Immer, if you both mutate AND return a value, the return value is used and mutations are discarded (or vice versa depending on Immer version). Show: using EITHER mutation OR explicit return (never both), TypeScript warning about returning from a function that mutates, and ESLint's `immer/no-return-and-mutation` rule.""",

"""**Debug Scenario:**
A XState machine shows an error "Cannot send event to stopped machine" after component unmount:

```tsx
function TrafficLight() {
  const [state, send] = useMachine(trafficLightMachine);

  useEffect(() => {
    const timer = setInterval(() => send('TIMER'), 1000); // After unmount!
    return () => clearInterval(timer); // Cleanup! But still errors in React 18 strict mode
  }, [send]);
}
```

In React 18 Strict Mode, effects run twice (mount → unmount → remount). The `send` function might be associated with a stopped machine service. Show: checking if the service is stopped before sending (`service.getSnapshot().done`), using XState's v5 `actor.subscribe` pattern for lifecycle management, and the `@xstate/react` hook's built-in handling of this edge case.""",

"""**Debug Scenario:**
A developer's Zustand `set` with a function updater doesn't update state when called multiple times synchronously:

```ts
const { increment } = useStore.getState();

// In a click handler:
increment(); // +1
increment(); // +1
increment(); // +1
// Expected count: 3, Actual count: 1!
```

```ts
const useStore = create(set => ({
  count: 0,
  increment: () => set(state => ({ count: state.count + 1 })),
}));
```

Actually, Zustand's functional updater (`set(state => ...)`) DOES read the latest state — the example above should work. Show the REAL problem: when `increment` IS called correctly but uses the OBJECT form instead:

```ts
increment: () => set({ count: useStore.getState().count + 1 }), // Stale count!
```

Three synchronous calls all read the same `count` before any update is applied. Show: using the functional form `set(state => ({ count: state.count + 1 }))` instead of object form.""",

"""**Debug Scenario:**
React Query's `prefetchQuery` doesn't pre-populate the cache before navigation, causing a loading state on mount:

```ts
// On hover over link (try to prefetch):
await queryClient.prefetchQuery({
  queryKey: ['product', id],
  queryFn: () => fetchProduct(id),
});

// On product page mount:
const { data, isLoading } = useQuery({
  queryKey: ['products', id], // Typo: 'products' vs 'product' in prefetch!
  queryFn: () => fetchProduct(id),
});
// isLoading: true — cache miss!
```

The query key in `prefetchQuery` doesn't match the query key in `useQuery`. Show: using shared query key constants or factory functions (`productKeys.detail(id)` → `['product', 'detail', id]`), the `getQueryData` check to verify the cache was populated, and React Query DevTools to inspect cache state.""",

"""**Debug Scenario:**
A developer's MobX `computed` value runs more often than expected, degrading performance:

```ts
class ProductStore {
  @observable products: Product[] = [];
  @observable activeCategory: string = 'all';
  @observable searchQuery: string = '';

  @computed get filteredProducts() {
    // Runs on ANY store change because accessing multiple observables:
    return this.products
      .filter(p => p.category === this.activeCategory)
      .filter(p => p.name.includes(this.searchQuery));
  }
}
```

Show: MobX's fine-grained dependency tracking (only re-runs when `products`, `activeCategory`, or `searchQuery` change — actually MobX IS efficient here). Demonstrate a case where it breaks: accessing a volatile observable inside computed (`Date.now()` makes it run every render cycle). Solution: move volatile computations outside `@computed` or use a `reaction`.""",

"""**Debug Scenario:**
A Redux store's middleware runs in the wrong order causing side effects before state is updated:

```ts
const store = configureStore({
  reducer: rootReducer,
  middleware: [analyticsMiddleware, thunkMiddleware, loggingMiddleware],
  // Order matters! Thunk must come BEFORE custom middleware
});

// analyticsMiddleware runs first — state isn't updated yet for analytics tracking!
```

Middleware runs in left-to-right order, wrapping from outside-in. `analyticsMiddleware` runs before `thunk` processes async actions. Show: the correct middleware order (thunk first, then custom middlewares that should react to the final action), using `getDefaultMiddleware()` to get the correct base order, and `listenerMiddleware` from RTK as a better pattern for side effects.""",

"""**Debug Scenario:**
A developer's React state update inside a `setTimeout` doesn't batch with other updates in React 17 (but does in React 18):

```ts
// React 17:
setTimeout(() => {
  setCount(c => c + 1); // Triggers re-render 1
  setUser(u => ({ ...u, online: true })); // Triggers re-render 2
  // Two re-renders!
}, 1000);

// React 18:
// The same code only triggers ONE re-render (automatic batching)
```

Show: React 17's behavior (no batching outside React event handlers), using `unstable_batchedUpdates` in React 17 to manually batch, React 18's automatic batching (everything is batched by default), and `flushSync` in React 18 to opt-out of batching when synchronous updates are needed.""",

"""**Debug Scenario:**
A developer's `useReducer` state with an object is causing unnecessary re-renders because the dispatch always returns a new state object even when nothing changed:

```ts
function reducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload }; // New object even if payload === state.loading!
    default:
      return state;
  }
}
```

If `SET_LOADING` is dispatched with the same value as current `loading`, a new state object is returned — `useReducer` bails out only if the reducer returns the `===` same reference. Show: adding an early return check (`if (action.payload === state.loading) return state`), and how `useReducer`'s bail-out only applies to the `===` same object comparison.""",

"""**Debug Scenario:**
A developer's Tanstack Query (React Query) v5 mutation cache is not being updated after a successful mutation:

```ts
const mutation = useMutation({
  mutationFn: (id: string) => api.deleteProduct(id),
  onSuccess: (_, deletedId) => {
    queryClient.setQueryData(['products'], (old: Product[]) =>
      old.filter(p => p.id !== deletedId)  // ✓ Correct filter
    );
    // But ProductDetail cache for the deleted product is still in cache!
    // queryClient.removeQueries(['products', deletedId]); // Forgot this!
  },
});
```

Show: removing the specific deleted item's cache with `queryClient.removeQueries({ queryKey: ['products', deletedId] })`, `invalidateQueries` as a simpler (but forces refetch) alternative, and using RTK Query's `onQueryStarted` to optimistically update the cache (RTK approach).""",

"""**Debug Scenario:**
A developer's global event bus pattern causes memory leaks because component subscribers are never removed:

```ts
const eventBus = new EventEmitter();

function NotificationComponent() {
  eventBus.on('notification', (msg) => {
    setMessages(prev => [...prev, msg]);
    // Bug: listener is never cleaned up when component unmounts!
  });

  return <div>...</div>;
}
```

Each mount of `NotificationComponent` adds a new listener. After navigating away and back 10 times, there are 10 listeners all running. Show: using `useEffect` with cleanup (`const handler = (msg) => ...; eventBus.on('notification', handler); return () => eventBus.off('notification', handler)`), and preferring React Context + Zustand/Jotai over a global event bus for React apps.""",

"""**Debug Scenario:**
A developer's Recoil atom family creates too many atoms and causes performance issues:

```ts
const productAtom = atomFamily<Product | null, string>({
  key: 'product',
  default: null,
});

// All 50,000 products get atoms created eagerly:
products.forEach(product => {
  useRecoilValue(productAtom(product.id)); // Creates atom for every product!
});
```

Each `atomFamily(id)` creates a new atom instance registered in Recoil's atom registry. 50,000 atoms consume significant memory. Show: creating atoms lazily (only call `productAtom(id)` when that product's component mounts), using `selectorFamily` to derive product data from a single `allProductsAtom` (one atom, not 50,000), and `useRecoilCallback` for imperative atom reads without creating subscriptions.""",

"""**Debug Scenario:**
A developer's SWR `mutate` call doesn't update the UI even though the API call succeeded:

```ts
const { data, mutate } = useSWR('/api/profile', fetcher);

async function updateProfile(newData) {
  await api.updateProfile(newData);
  mutate(); // Should revalidate!
  // But data still shows old value for 5 seconds
}
```

The key-based `mutate()` from `useSWR` triggers revalidation — but if a custom `fetcher` has an internal cache that returns stale data, SWR sees the same (stale) response. Show: using optimistic mutation (`mutate(optimisticData, false)` — update cache locally without revalidation), using `mutate('/api/profile', newData, false)` for instant UI update, and verifying the `fetcher` doesn't have its own cache layer masking the stale data problem.""",

"""**Debug Scenario:**
A developer's Redux middleware accidentally blocks async actions by calling `next` twice:

```ts
const apiMiddleware: Middleware = store => next => action => {
  if (action.type === 'API_CALL') {
    fetch(action.url)
      .then(r => r.json())
      .then(data => store.dispatch({ type: action.successType, payload: data }));
    return next(action); // Passes action through to reducer!
    // Action goes through reducer with just the request (no data yet)
    // Then success dispatch later — two reducer calls
  }
  return next(action);
};
```

Show: NOT calling `next(action)` for API actions that should be handled entirely by the middleware (swallowing the original action), or dispatching a `REQUEST_STARTED` action via `next` to signal loading state, and the Redux Thunk approach (avoids this duplication by having separate action creators for request/success/failure).""",

"""**Debug Scenario:**
A developer's state management causes "flashing" of stale data when switching between two resources that share a query key:

```ts
// Product A selected:
const { data } = useQuery(['product', id], fetchProduct);
// data: Product A's data

// User clicks to Product B:
// During the refetch for Product B, data still shows Product A!
```

React Query keeps the previous data visible while refetching by default (`keepPreviousData`). Show: using `placeholderData: keepPreviousData` intentionally when you WANT this (pagination), setting `placeholderData: undefined` for cases where old data should not show for a new resource (different entity), and showing a loading skeleton overlay on top of previous data while the new data loads.""",

]

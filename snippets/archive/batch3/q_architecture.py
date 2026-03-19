"""
snippets/q_architecture.py — BATCH 3: 28 brand-new Architecture questions
Zero overlap with batch1 or batch2 archives.
"""

Q_ARCHITECTURE = [

"""**Task (Code Generation):**
Implement a `CircuitBreaker` class for wrapping API calls that prevents cascading failures:

```ts
const cb = new CircuitBreaker({
  threshold: 5,     // open after 5 consecutive failures
  timeout: 30_000,  // try half-open after 30s
  onStateChange: (from, to) => logger.warn(`Circuit ${from} → ${to}`),
});

const data = await cb.execute(() => fetch('/api/orders').then(r => r.json()));
// Throws CircuitOpenError if circuit is open
```

Show: the three states (closed/open/half-open), transition logic, the execution wrapper, and integration with React Query as a custom `queryFn` middleware that maps circuit errors to user-visible messages.""",

"""**Debug Scenario:**
A React app's bundle is analyzed and shows the entire `@sentry/browser` SDK (45KB) is loaded synchronously on page load, even for users who will never trigger an error. The SDK is initialized in `_app.tsx`:

```ts
import * as Sentry from '@sentry/browser';
Sentry.init({ dsn: process.env.SENTRY_DSN });
```

Design an error monitoring architecture that:
1. Loads Sentry SDK lazily only after the first error occurs
2. Queues errors that happen before Sentry loads
3. Sends queued errors after SDK loads
4. Falls back to `console.error` if Sentry fails to load

Show the lazy loading strategy and the error queue implementation.""",

"""**Task (Code Generation):**
Build a declarative `<QueryBuilder>` component for constructing complex API filter queries:

```tsx
<QueryBuilder
  schema={productSchema}
  onChange={setFilters}
  initialQuery={{
    operator: 'AND',
    rules: [
      { field: 'price', operator: 'gt', value: 100 },
      { field: 'category', operator: 'in', value: ['electronics'] },
    ],
  }}
/>
```

Show: the recursive query node type (`Group | Rule`), the JSON schema to derive available operators per field type, the rule builder UI component, and how to convert the JSON query to a URL query string and a SQL WHERE clause.""",

"""**Debug Scenario:**
A company's frontend microservice architecture has four React apps sharing a `@shared/design-system` package. After a `Button` component API-breaking change (renaming `onClick` to `onPress`), only 2 of 4 apps updated, breaking the other 2 in production.

Design a breaking change detection system:
1. Export a machine-readable API contract from the design system (`api.json`)
2. CI step that compares the package's `api.json` with the previous version
3. Semantic versioning enforcement: major bump required for prop renames
4. Automated codemod generation that renames `onClick` → `onPress` in consumer apps

Show the API contract format and the detection script.""",

"""**Task (Code Generation):**
Implement a request deduplication middleware for a shared API layer:

```ts
const client = createApiClient({
  deduplicate: true, // identical in-flight requests share one Promise
  deduplicateWindow: 50, // ms: requests within 50ms are considered duplicates
});

// Two simultaneous calls → one network request:
const [userA, userB] = await Promise.all([
  client.get('/api/user/1'),
  client.get('/api/user/1'),
]);
```

Show the pending request Map keyed by URL+method+body hash, Promise sharing, cache expiry after `deduplicateWindow`, and TypeScript generics for the response type.""",

"""**Debug Scenario:**
A Next.js monorepo has a `@company/auth` package shared across 3 apps. The package exports both server-side utilities (uses `next/headers`, `cookies()`) and client-side utilities (uses `useState`, context). When the `@company/auth` package is imported in a Server Component, it works fine. In a Client Component, it crashes because the package doesn't mark itself as server-only or client-only.

Design the correct package architecture:
1. `@company/auth/server` — server-only exports with `server-only` package guard
2. `@company/auth/client` — client-only exports with `client-only` package guard
3. `@company/auth` — shared types and constants only

Show the `package.json` exports field configuration for each subpath.""",

"""**Task (Code Generation):**
Build a `DataPipeline<Input, Output>` for ETL operations with error isolation per record:

```ts
const pipeline = new DataPipeline<RawProduct, ProcessedProduct>()
  .step('validate', (p) => validateProduct(p))         // throws → skips record
  .step('enrich', async (p) => fetchCategory(p))       // async step
  .step('transform', (p) => normalizeProduct(p))        // sync transform
  .step('deduplicate', (p, context) => {               // stateful step
    if (context.seen.has(p.id)) throw new SkipError();
    context.seen.add(p.id);
    return p;
  });

const { results, errors, skipped } = await pipeline.process(rawProducts);
```

Show the step composition types, error isolation (one record failure doesn't stop others), and the stateful context pattern.""",

"""**Debug Scenario:**
A Single Page Application stores user auth tokens in `localStorage`. A security audit flags this as vulnerable to XSS: any script injected into the page can steal the token.

Design a secure token storage architecture:
1. Access token in memory (`useRef` in a top-level component, not accessible from other scripts)
2. Refresh token in `HttpOnly` cookie (not readable by JavaScript)
3. Silent refresh: a background timer calls `/api/auth/refresh` using the HttpOnly cookie
4. Security tradeoff: why memory storage loses auth on page refresh and how to handle it

Show the React provider implementation for in-memory token management.""",

"""**Task (Code Generation):**
Implement a `createRepository` factory for clean data access layer abstraction:

```ts
const userRepo = createRepository<User>({
  tableName: 'users',
  primaryKey: 'id',
  db: prismaClient,
});

// Provides standard CRUD with TypeScript types:
const user = await userRepo.findById('1');         // User | null
const users = await userRepo.findMany({ where: { active: true } }); // User[]
const created = await userRepo.create({ name: 'Alice', email: 'a@b.c' }); // User
const updated = await userRepo.update('1', { name: 'Bob' }); // User
await userRepo.delete('1'); // void
```

Show the TypeScript generic factory, Prisma integration, and a cacheable version using React Query.""",

"""**Debug Scenario:**
A team builds a real-time collaborative editor where multiple users edit a JSON document simultaneously. When two users edit the same field at the same time, last-write-wins causes data loss.

Design an Operational Transformation (OT) lite system for concurrent edits:
1. Assign a vector clock to each operation
2. On conflict (same field, different values), use a deterministic merge rule (longer value wins, or alphabetically)
3. Show how operations are rebased when the server receives out-of-order updates
4. React integration: optimistic local updates + server-authoritative merge

Show the operation type, the transform function, and the client-side merge logic.""",

"""**Task (Code Generation):**
Design a feature rollout system with automatic rollback for a Next.js deployment:

```ts
const rollout = createRolloutConfig({
  feature: 'new-checkout',
  percentage: 20, // 20% of users
  metrics: {
    errorRateThreshold: 0.05, // rollback if error rate > 5%
    latencyThreshold: 2000,   // rollback if p95 > 2s
    checkInterval: 60_000,    // check every minute
  },
  onRollback: () => notifySlack('new-checkout rolled back!'),
});
```

Show: the consistent hashing for user assignment (same user always in/out of rollout), the metrics collection endpoint, the automated rollback trigger, and the Next.js Edge Config integration to change rollout percentage without redeployment.""",

"""**Debug Scenario:**
A large React application has a `<GlobalSearchBar>` that's mounted at the root layout level. When the route changes, the search bar briefly unmounts and remounts (losing focus and input state) because the route-level Suspense boundary wraps the layout.

Explain: why Suspense boundaries above a component cause it to unmount during navigation fallback, show the fix using `startTransition` for navigation (prevents showing loading fallback for fast navigations), and the layout-level Suspense positioning that avoids unmounting persistent UI elements like navigation bars and search.""",

"""**Task (Code Generation):**
Build a `SchemaRegistry` for runtime type validation with versioning support:

```ts
const registry = new SchemaRegistry();
registry.register('UserCreated', { version: 1, schema: UserCreatedV1Schema });
registry.register('UserCreated', { version: 2, schema: UserCreatedV2Schema });

// Validates incoming events and migrates old versions:
const event = registry.validate('UserCreated', payload, { version: payload.schemaVersion });
// event is typed as the latest version
```

Show: Zod schema versioning, automatic migration from v1 → v2 using a `migrate` function, the registry's TypeScript types for versioned schemas, and integration with a message queue consumer that processes events.""",

"""**Debug Scenario:**
A company uses a Webpack Module Federation setup where the host app and remote apps run different React versions (host: 18.2, remote: 18.3). The remote app's components crash with:

```
Error: Invalid hook call. Hooks can only be called inside a function component.
```

This happens because two React instances are loaded (one per app), violating React's singleton requirement. Explain the correct `shared` configuration that forces both apps to use a single React instance, the `singleton: true` flag, and `strictVersion: false` — when to use each and the tradeoffs for minor version mismatches.""",

"""**Task (Code Generation):**
Implement a `DocumentWorkflow<States>` state machine for document approval processes:

```ts
const workflow = createDocumentWorkflow({
  states: ['draft', 'review', 'approved', 'rejected', 'archived'],
  transitions: {
    draft: ['review'],
    review: ['approved', 'rejected'],
    approved: ['archived'],
    rejected: ['draft'],
    archived: [],
  },
  guards: {
    'draft→review': (doc, user) => doc.wordCount > 100 && user.role !== 'viewer',
    'review→approved': (doc, user) => user.role === 'manager',
  },
  hooks: {
    onEnter: { approved: async (doc) => await sendApprovalEmail(doc.authorId) },
  },
});
```

Show the TypeScript type inference for valid transition strings and the guard evaluation.""",

"""**Debug Scenario:**
An analytics pipeline processes 50,000 events per minute. The frontend sends events to a `/api/events` Route Handler which writes directly to PostgreSQL. At peak load, the database connection pool is exhausted and events are lost.

Design a buffered write architecture:
1. Frontend → in-memory queue (browser) → batch POST every 5 seconds (max 100 events)
2. Route Handler → Redis list (append, non-blocking) → return 202 immediately
3. Background worker → reads from Redis list → batches to PostgreSQL every 10 seconds
4. Dead letter queue for failed writes

Show the frontend batching hook and the Route Handler implementation.""",

"""**Task (Code Generation):**
Build a unified error handling architecture across a Next.js + Node.js API backend:

```ts
// Shared error types:
class AppError extends Error {
  constructor(
    public code: ErrorCode,
    message: string,
    public statusCode: number,
    public context?: Record<string, unknown>
  ) { super(message); }
}
```

Show:
1. `ErrorCode` enum covering validation, auth, network, not-found errors
2. Next.js Route Handler error middleware that maps `AppError` to HTTP responses
3. React Error Boundary that categorizes errors and shows appropriate UI
4. Sentry integration that adds `context` to error reports
5. Client-side error normalization for fetch errors""",

"""**Debug Scenario:**
A design system's tokens are defined in a `tokens.json` file consulted by both the CSS generation pipeline and the TypeScript type system. After adding new tokens, some components still reference old token names that were renamed — TypeScript doesn't catch this because the components use string literals:

```ts
// Old:
const color = token('brand-primary'); // string, not type-checked
// New token name: 'color-brand-primary'
```

Design a type-safe token access system where `token('brand-primary')` is a TypeScript error (the string isn't a valid token name), using generated types from `tokens.json`.""",

"""**Task (Code Generation):**
Implement a `useReconnectingWebSocket` hook for mission-critical real-time connections:

```ts
const { send, readyState, lastMessage } = useReconnectingWebSocket('wss://api.example.com/ws', {
  reconnectInterval: 1000,
  maxReconnectAttempts: 10,
  exponentialBackoff: true,
  onReconnect: (attempt) => console.log(`Reconnecting (attempt ${attempt})`),
  protocols: ['v1.protocol.example'],
});
```

Show: exponential backoff calculation, heartbeat ping/pong to detect dead connections, queue of messages sent while disconnected (replay on reconnect), React state for `readyState` (Connecting/Open/Closing/Closed), and cleanup on unmount.""",

"""**Debug Scenario:**
A team adopts Turborepo for their monorepo but finds the build cache hit rate is only 20% despite no changes to most packages. Investigation reveals that all packages list `../../.env` in their inputs hash:

```json
{
  "pipeline": {
    "build": {
      "inputs": ["$TURBO_DEFAULT$"],
      "env": ["DATABASE_URL", "API_URL"]
    }
  }
}
```

The `.env` file changes every build (it includes a `BUILD_TIMESTAMP` variable), poisoning all cache entries. Show how to fix `turbo.json`: explicitly list only the env vars that affect the build output, use `globalEnv` for shared vars, and `passThroughEnv` for vars that should be available but not affect cache hash.""",

"""**Task (Code Generation):**
Build a `useUndoableReducer` that wraps `useReducer` with built-in undo/redo:

```ts
const [state, dispatch, { undo, redo, canUndo, canRedo }] = useUndoableReducer(
  reducer,
  initialState,
  { maxHistory: 50 }
);

dispatch({ type: 'ADD_ITEM', payload: item }); // recorded in history
undo(); // reverts to previous state
redo(); // reapplies the action
```

Requirements:
- Marks specific actions as `skipHistory: true` for non-undoable side-effects (like analytics)
- `undo()` dispatches a reverse action (not just restores a snapshot) for conflict resolution in collaborative contexts
- Time-travel debugging: `jumpToState(index)` jumps to specific history entry

Show the full implementation.""",

"""**Debug Scenario:**
A large Next.js app has 60 API routes. Every route handler re-implements the same pattern: parse body, validate with Zod, check auth, run handler, catch errors. A new developer adds a route without the auth check and this reaches production.

Design a typed Route Handler factory that enforces the required middleware:

```ts
export const GET = createHandler({
  auth: 'required',              // ← TypeScript error if omitted and route is authenticated
  schema: { query: QuerySchema },
  handler: async ({ query, user }) => { ... },
});
```

Show the factory implementation, how TypeScript enforces `auth` is specified, and how the inferred `user` type changes based on `auth: 'required' | 'optional' | 'none'`.""",

"""**Task (Code Generation):**
Implement a client-side caching layer with Cache-Control semantics:

```ts
const cache = new ResponseCache({
  defaultMaxAge: 60_000,         // 1 minute
  staleWhileRevalidate: 30_000,  // serve stale for 30s while revalidating
  maxEntries: 200,
  storage: 'memory',             // or 'sessionStorage' | 'indexeddb'
});

const user = await cache.fetch('/api/user/1', async () => {
  const res = await fetch('/api/user/1');
  return res.json();
}, { maxAge: 300_000 }); // 5 min for this specific key
```

Show the entry lifecycle (fresh → stale → expired), stale-while-revalidate logic (background refresh), LRU eviction, and TypeScript generics for response type inference.""",

"""**Debug Scenario:**
A React Native + Next.js monorepo shares business logic in a `@shared/core` package. After adding a React-specific hook to `@shared/core`, the Node.js backend (which imports from the same package) crashes at startup:

```
TypeError: (0 , react__WEBPACK_IMPORTED_MODULE_0__.useState) is not a function
```

The backend imported `@shared/core` which now transitively imports React. Design the monorepo package boundaries: `@shared/core-pure` (no framework deps, pure TypeScript), `@shared/core-react` (React hooks), `@shared/core-react-native` (RN-specific). Show how `package.json` exports and `peerDependencies` enforce these boundaries.""",

"""**Task (Code Generation):**
Build a `TokenBucket` rate limiter for client-side API call throttling:

```ts
const limiter = new TokenBucket({
  capacity: 10,        // max 10 requests burst
  refillRate: 2,       // add 2 tokens per second
  refillInterval: 500, // check every 500ms
});

async function apiCall(url: string) {
  await limiter.acquire(); // waits if no tokens available
  return fetch(url);
}
```

Show: the token refill algorithm, `acquire()` that returns a Promise that resolves when a token is available (queuing requests), `tryAcquire()` that returns false immediately if no tokens (for non-blocking usage), and a React `useRateLimiter` hook wrapper.""",

"""**Debug Scenario:**
A company's monorepo has 15 packages. Running `tsc --build` takes 45 seconds. The TypeScript project references graph is:

```
app → shared → utils → base
app → ui-components → base
```

After changing only `utils`, the build still recompiles `base`, `shared`, `ui-components` (which doesn't depend on `utils`), and `app`.

Explain TypeScript's project references incremental build algorithm, why `ui-components` shouldn't be rebuilt (it doesn't depend on `utils`), and diagnose whether the issue is incorrect `tsconfig.json` references, missing composite mode, or incorrect `outDir` configuration. Show the correct tsconfig setup.""",

"""**Task (Code Generation):**
Design a `useFeatureAnnouncement` hook that shows one-time tooltips introducing new features to existing users:

```ts
const { shouldShow, dismiss } = useFeatureAnnouncement('new-export-button', {
  showAfterDays: 1,  // don't show on day-of-release, wait 1 day
  maxShows: 3,       // show at most 3 times before auto-dismissing
  userSegment: 'power-users', // only show to users with >50 exports
});

if (shouldShow) {
  return <FeatureTooltip onDismiss={dismiss}>New: Export to PDF!</FeatureTooltip>;
}
```

Show: localStorage-based persistence for show count and first-seen date, the user segment evaluation (checked against user profile from context), and the `useEffect` that resets announcements when a new feature key is provided.""",

"""**Debug Scenario:**
A company uses Webpack's Module Federation for micro-frontends. After upgrading the shell app's React from 18.2 to 18.3, the remote apps (still on 18.2) start showing hooks errors when rendered inside the shell.

Both the shell and remotes declare React as `shared` in their Webpack configs, but the `requiredVersion` is set to `^18.0.0` (too broad) in the remote, allowing the shell to load React 18.3 which then mismatches with the remote's built-in hooks expectations.

Show: the correct `requiredVersion: '18.2.x'` pinning, the `strictVersion: true` flag that throws rather than silently using a mismatched version, and how to use `singleton: true` with version checking to guarantee only one React instance while still detecting version mismatches at startup.""",

]

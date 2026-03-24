"""
snippets/q_architecture.py — BATCH 5: 28 brand-new Architecture questions
Zero overlap with batch1, batch2, batch3, or batch4 archives.
"""

Q_ARCHITECTURE = [

"""**Task (Code Generation):**
Implement a `createBFFClient<Schema>` (Backend for Frontend) that provides a typed data layer:

```ts
const bff = createBFFClient({
  baseUrl: '/api/bff',
  schema: {
    'dashboard.overview':  { input: { userId: z.string() }, output: DashboardOverviewSchema },
    'products.search':     { input: SearchFiltersSchema, output: z.array(ProductSchema) },
    'orders.create':       { input: CreateOrderSchema, output: OrderConfirmationSchema },
  },
});

// Fully typed:
const overview = await bff.call('dashboard.overview', { userId: '123' });
// overview: DashboardOverview
```

Show: the BFF server-side aggregation layer (single endpoint that orchestrates multiple microservice calls in parallel), the typed client that validates input/output with Zod, request deduplication (two concurrent `dashboard.overview` calls with same args → one HTTP request), and the `trpc`-style end-to-end type inference.""",

"""**Debug Scenario:**
A React app using React Query has a memory leak in production. Heap snapshots show `QueryObserver` objects accumulating over time — hundreds of thousands of instances.

Investigation shows a custom hook creates a new query key on every render:

```ts
function useProductData(id: string) {
  const timestamp = Date.now(); // new key each render!
  return useQuery({
    queryKey: ['product', id, timestamp], // changes every render
    queryFn: () => api.getProduct(id),
  });
}
```

React Query creates a new `QueryObserver` for each unique `queryKey`. With a changing timestamp, each render registers a new observer. Show: removing `timestamp` from the query key, using `staleTime` for cache freshness control instead, and React Query devtools for visualizing the live observer count.""",

"""**Task (Code Generation):**
Build a `createSagaRunner` for managing complex multi-step business workflows (without redux-saga dependency):

```ts
const checkoutSaga = createSagaRunner({
  name: 'checkout',
  steps: {
    validateCart:   async (ctx) => { await validateInventory(ctx.cart); return ctx; },
    applyDiscount:  async (ctx) => ({ ...ctx, total: applyDiscounts(ctx.cart, ctx.user) }),
    charge:         async (ctx) => ({ ...ctx, paymentId: await chargeCard(ctx.total) }),
    fulfillOrder:   async (ctx) => ({ ...ctx, orderId: await createOrder(ctx) }),
  },
  compensations: {
    charge:         async (ctx) => await refundPayment(ctx.paymentId!),
    validateCart:   async (ctx) => await releaseInventoryHold(ctx.cart),
  },
  onStepStart:    (step) => logger.info(`Starting ${step}`),
  onStepComplete: (step) => metrics.increment(`saga.${step}.success`),
  onCompensate:   (step) => logger.warn(`Compensating ${step}`),
});

const result = await checkoutSaga.run({ cart, user });
```

Show: sequential step execution with accumulated context, automatic compensation (rollback) in reverse order on failure, TypeScript context type accumulation through steps, and retry logic per step.""",

"""**Debug Scenario:**
A monorepo with 5 packages builds correctly but end-to-end tests fail with mismatched API types — the frontend uses a stale type definition for a request that the backend changed 3 days ago.

The frontend package has `@my-org/api-types` as a devDependency pinned to `^1.2.0`. The backend updated `api-types` to `1.3.0` (added required `correlationId` field) but the frontend wasn't updated.

Show: pinning internal workspace packages to `workspace:*` (always uses the local workspace version), adding a CI step that runs `npm ls @my-org/api-types` and fails if versions differ between packages, using a `changesets` bot that requires all consumers to update when the API types package is changed, and a TypeScript project reference to the api-types package (forces recompilation when types change).""",

"""**Task (Code Generation):**
Implement a `createCircuitBreaker<T>` for protecting services from cascade failures:

```ts
const paymentBreaker = createCircuitBreaker({
  call: processPayment,
  thresholds: {
    failureRate: 0.5,      // open after 50% failure rate
    sampleWindow: 20,      // over last 20 calls
    successToClose: 3,     // require 3 successes to close (half-open)
  },
  timeout: 5000,           // calls fail-fast after 5s when open
  onStateChange: (from, to) => metrics.record('circuit_breaker_state', { from, to }),
  fallback: async () => ({ status: 'queued', message: 'Payment will be processed shortly' }),
});

try {
  const result = await paymentBreaker.call(paymentData);
} catch (e) {
  // Circuit is open: e.message = 'Circuit breaker OPEN'
}
```

Show: the state machine (closed → open → half-open → closed), the rolling failure rate window, and the `fallback` function that's called when the circuit is open.""",

"""**Debug Scenario:**
A developer deploys a breaking API change (removed a required field) to production without versioning the API. Existing mobile app users on version 1.x get errors because their app sends requests with the removed field and expects it in the response.

Show: implementing URL versioning (`/api/v1/users`, `/api/v2/users`), or header versioning (`Accept: application/vnd.api.v2+json`), maintaining the v1 endpoint for backward compatibility with a deprecation warning header (`Deprecation: true`, `Sunset: 2025-06-01`), and a compatibility layer in v2 that accepts v1 request shapes and transforms them.""",

"""**Task (Code Generation):**
Build a `createSchemaEvolution<V>` system for migrating data between schema versions:

```ts
const userEvolution = createSchemaEvolution({
  v1: z.object({ name: z.string(), email: z.string() }),
  v2: z.object({ firstName: z.string(), lastName: z.string(), email: z.string() }),
  v3: z.object({ firstName: z.string(), lastName: z.string(), email: z.string(), role: z.enum(['user', 'admin']) }),
  migrations: {
    'v1->v2': (v1) => ({
      firstName: v1.name.split(' ')[0],
      lastName: v1.name.split(' ').slice(1).join(' ') || '',
      email: v1.email,
    }),
    'v2->v3': (v2) => ({ ...v2, role: 'user' as const }),
  },
});

// Auto-migrates v1 data to v3:
const v3User = userEvolution.migrate(v1Data, { from: 'v1', to: 'v3' });
```

Show: chaining migrations (`v1→v2→v3`), schema version detection from data shape, and backward compatibility checks.""",

"""**Debug Scenario:**
A Next.js app has multiple teams deploying different parts of the monorepo. After Team B deploys a shared `<Button>` component update, Team A's pages (not yet deployed) show broken layouts because the shared component's API changed:

```ts
// Old Button API:
<Button type="primary">Click</Button>

// New Button API (breaking change):
<Button variant="primary">Click</Button>  // 'type' prop removed
```

Show: semantic versioning for the shared component library with `changesets`, flagging breaking changes in PRs using the `changeset` bot, adding a `type` prop alias that maps to `variant` for backward compatibility during the transition period, and a Storybook visual regression test that catches UI changes before deployment.""",

"""**Task (Code Generation):**
Implement a `createQueryPlanner` for optimizing batched data fetching (DataLoader pattern):

```ts
const userLoader = createQueryPlanner<string, User>({
  batchFetch: async (ids) => {
    const users = await db.users.findMany({ where: { id: { in: ids } } });
    return ids.map(id => users.find(u => u.id === id) ?? null);
  },
  batchDelay: 5,         // collect IDs for 5ms before firing
  maxBatchSize: 100,     // max IDs per batch request
  cacheKey: (id) => `user:${id}`,
  cacheTTL: 60_000,
});

// 50 simultaneous calls → 1 batched DB query:
const [alice, bob, charlie] = await Promise.all([
  userLoader.load('u1'),
  userLoader.load('u2'),
  userLoader.load('u3'),
]);
```

Show: the tick-based batching (collect IDs within the current microtask queue, then batch), deduplication of duplicate IDs, the in-flight request cache (concurrent loads of the same ID share one Promise), and error per-item (one failed ID doesn't fail the entire batch).""",

"""**Debug Scenario:**
A React app's global error boundary catches React rendering errors but user reports show some errors appear only in safari private mode and are never caught:

```
TypeError: Cannot read properties of undefined (reading 'analytics')
  at window.analytics.track (...)
```

This error occurs OUTSIDE of React's rendering tree (in an event listener, not during render). Error boundaries only catch errors thrown during rendering, in lifecycle methods, and in constructors. Show: `window.addEventListener('error', handler)` for uncaught synchronous errors, `window.addEventListener('unhandledrejection', handler)` for unhandled async errors, forwarding these to Sentry, and the `ErrorBoundary.getDerivedStateFromError` vs `componentDidCatch` API.""",

"""**Task (Code Generation):**
Build a `createDomainEventStore` for event-sourced state management:

```ts
const orderStore = createDomainEventStore<Order, OrderEvent>({
  eventHandlers: {
    'order.created':    (state, e) => ({ ...initialOrder, id: e.payload.orderId }),
    'item.added':      (state, e) => ({ ...state, items: [...state.items, e.payload.item] }),
    'discount.applied': (state, e) => ({ ...state, discount: e.payload.discount }),
    'order.shipped':   (state, e) => ({ ...state, status: 'shipped', trackingId: e.payload.trackingId }),
  },
  initialState: null as Order | null,
});

// Build current state by replaying events:
const currentOrder = orderStore.buildFrom(eventStream);

// Project to a specific point in time:
const orderAtTime = orderStore.buildFrom(eventStream, { upTo: new Date('2024-01-15') });
```

Show: the event replay engine, temporal queries, event store schema (event type, payload, timestamp, aggregate ID), and a React hook `useOrderState(orderId)` that subscribes to new events via WebSocket.""",

"""**Debug Scenario:**
A GraphQL API with subscriptions has a memory leak — `console.log('active subscriptions:', pubsub.subscriptionCount())` shows subscriptions growing from 100 to 50,000 over 24 hours, never decreasing.

Investigation shows the subscription cleanup function (returned from the resolver) is never called when clients disconnect unexpectedly (browser tab closed without a clean WebSocket close):

```ts
Subscription: {
  orderUpdated: {
    subscribe: (_, { orderId }) => pubsub.asyncIterator(`order:${orderId}`),
    // Missing: cleanup when client disconnects
  }
}
```

Show: implementing `withFilter` from `graphql-subscriptions` that calls cleanup on disconnect, the WebSocket `close` event handler in `graphql-ws` server config that triggers garbage collection for the client's subscriptions, and `asyncIterator.return()` to clean up the async iterator.""",

"""**Task (Code Generation):**
Implement a `createMicroFrontendLoader` for dynamically loading micro-frontends:

```ts
const loader = createMicroFrontendLoader({
  registry: {
    'checkout':    { url: 'https://checkout.example.com/remoteEntry.js', scope: 'checkout', module: './App' },
    'product-feed': { url: 'https://catalog.example.com/remoteEntry.js', scope: 'catalog', module: './Feed' },
  },
  sharedModules: { react: { singleton: true, requiredVersion: '^18.0.0' } },
  onLoadError: (mfe, error) => fallbackRegistry.render(mfe),
});

// Usage:
const CheckoutApp = await loader.load('checkout');
<Suspense fallback={<LoadingSpinner />}>
  <CheckoutApp cartId={cartId} onComplete={handleCheckoutComplete} />
</Suspense>
```

Show: dynamic `<script>` injection for the remote entry, Webpack Module Federation `__webpack_init_sharing__` and `__webpack_share_scopes__` global API calls, error boundaries per MFE, and version negotiation for shared modules.""",

"""**Debug Scenario:**
A monorepo's ESLint configuration has a `@typescript-eslint/no-floating-promises` rule that's disabled in 80% of files with `// eslint-disable-next-line`. The rule was intended to prevent unhandled Promise rejections but proved too noisy.

Show: configuring `no-floating-promises` to allow `void expression` pattern (`void somePromise()` to explicitly mark intentionally unhandled Promises), the `ignoreVoid: true` option, and using an ESLint custom rule plugin that checks for `void` usage context (ensures the developer consciously chose to ignore the Promise rather than forgetting to await it).""",

"""**Task (Code Generation):**
Build a `createObservabilityMiddleware` for Express that provides distributed tracing:

```ts
app.use(createObservabilityMiddleware({
  tracer: opentelemetry.trace.getTracer('api-server'),
  propagator: new W3CTraceContextPropagator(),
  excludePaths: ['/health', '/metrics'],
  enrichSpan: (span, req) => {
    span.setAttribute('user.id', req.user?.id ?? 'anonymous');
    span.setAttribute('tenant.id', req.headers['x-tenant-id']);
  },
  metricsExporter: prometheusExporter,
}));
```

Show: extracting trace context from incoming `traceparent` header (W3C Trace Context), creating a child span for each request, recording `http.method`, `http.status_code`, and `http.route` span attributes per OpenTelemetry semantic conventions, Prometheus counter/histogram for request duration, and forwarding the trace context to outgoing `fetch` calls within the request handler.""",

"""**Debug Scenario:**
A team uses GitHub Actions to deploy to production on every merge to `main`. A typo in a recently merged PR broke the login flow in production for 40 minutes before it was noticed.

Design a safer deployment pipeline:
1. Static analysis gate (TypeScript + ESLint run on PR, block merge on failure)
2. Preview deployments for every PR (Vercel/Netlify preview URLs)
3. Smoke test that runs against preview before merging
4. Canary deployment to main (5% of traffic → 25% → 100%, with automatic rollback on error spike)

Show the GitHub Actions workflow YAML for the smoke test gate step and the canary traffic routing configuration.""",

"""**Task (Code Generation):**
Implement a `createAuthorizationEngine<Permissions>` with RBAC and ABAC:

```ts
const auth = createAuthorizationEngine({
  roles: {
    admin:    ['users:*', 'products:*', 'orders:*'],
    manager:  ['products:read', 'products:write', 'orders:read'],
    customer: ['products:read', 'orders:own:*'],
  },
  attributes: {
    'orders:own:read': (user, resource) => user.id === resource.ownerId,
    'orders:own:write': (user, resource) => user.id === resource.ownerId && resource.status === 'draft',
  },
});

const can = await auth.check(user, 'orders:own:read', order);
// can.allowed: true/false
// can.reason: 'attribute-check:orders:own:read' | 'role:customer' | 'denied'
```

Show: the permission inheritance (wildcard matching `users:*`), attribute-based checks for ownership, permission caching, and Express middleware integration.""",

"""**Debug Scenario:**
A Prisma-based API has N+1 query problems. Fetching 10 blog posts each with their author triggers 11 database queries instead of 2:

```ts
const posts = await prisma.post.findMany({ take: 10 });
// renders each post's author:
for (const post of posts) {
  const author = await prisma.user.findUnique({ where: { id: post.authorId } }); // 10 queries!
}
```

Show: the `include` option in Prisma to join authors in a single query (`findMany({ include: { author: true } })`), Prisma's query log to count actual DB queries, `select` to limit returned fields (avoid over-fetching), and the DataLoader pattern for GraphQL resolvers that can't use Prisma joins.""",

"""**Task (Code Generation):**
Build a `createCRDTDocument<T>` for conflict-free collaborative editing:

```ts
const doc = createCRDTDocument<Document>({
  initialState: { title: '', content: '', tags: [] },
  mergeFn: {
    title: 'last-write-wins',     // LWW with Lamport timestamp
    content: 'operational-transform', // OT for text editing
    tags: 'set-union',            // merge as sets (no duplicates)
  },
  clientId: generateClientId(),
});

// Local update:
doc.update('title', 'New Title');

// Remote update from another client:
doc.merge(remoteOperation);

// Both clients eventually converge to the same state
const finalState = doc.state();
```

Show: Lamport timestamps for LWW, vector clocks for causality tracking, the text OT algorithm (insert/delete operations that transform around concurrent edits), and React integration for collaborative editing.""",

"""**Debug Scenario:**
A developer uses `try/catch` in an async function but the catch block never executes after a thrown error inside a `forEach` callback:

```ts
async function processAll(items: Item[]) {
  try {
    items.forEach(async (item) => {
      await processItem(item); // throws!
    });
  } catch (e) {
    console.log('caught!'); // never runs
  }
}
```

`forEach` doesn't await the async callbacks — it fires them all synchronously (returning Promises that float). The `try/catch` wraps synchronous `forEach`, not the async operations inside. Show: replacing `forEach` with `for...of` loop (properly awaits each), `Promise.all(items.map(async item => processItem(item)))` for concurrent processing with a single catchable rejection, and `Promise.allSettled` for processing all items even if some fail.""",

"""**Task (Code Generation):**
Implement a `createDatabaseMigrationRunner` with rollback support:

```ts
const runner = createDatabaseMigrationRunner({
  migrations: [
    {
      id: '001_create_users',
      up:   async (db) => { await db.query(`CREATE TABLE users (...)`); },
      down: async (db) => { await db.query(`DROP TABLE users`); },
    },
    {
      id: '002_add_roles',
      up:   async (db) => { await db.query(`ALTER TABLE users ADD COLUMN role VARCHAR(50)`); },
      down: async (db) => { await db.query(`ALTER TABLE users DROP COLUMN role`); },
    },
  ],
  stateTable: '_migrations',    // tracks applied migrations
});

await runner.up();         // apply all pending
await runner.down(1);      // rollback last 1
await runner.status();     // list applied/pending
```

Show: the `_migrations` tracking table schema, transactional migration (rollback DB transaction if migration fails), checksum validation (detect if a migration file was modified after being applied), and dry-run mode that shows SQL without executing.""",

"""**Debug Scenario:**
A large express app has 200+ API routes. Adding authentication middleware to each route manually is error-prone — 12 routes are missing auth middleware and are publicly accessible.

Show: a default-secure approach using a global middleware that applies auth to ALL routes, then an explicit `publicRoute` decorator or `auth: false` flag for routes that should be public:

```ts
app.use(authMiddleware); // secure everything by default

// Explicit opt-out:
app.get('/api/public/health', markAsPublic, healthHandler);
app.post('/api/public/login', markAsPublic, loginHandler);
```

And an integration test that crawls all registered routes and asserts each either has `markAsPublic` or returns 401 without auth headers.""",

"""**Task (Code Generation):**
Build a `createMultiRegionClient` that routes requests to the nearest region:

```ts
const client = createMultiRegionClient({
  regions: {
    'us-east': { url: 'https://us-east.api.example.com', latency: Infinity },
    'eu-west': { url: 'https://eu-west.api.example.com', latency: Infinity },
    'ap-south':{ url: 'https://ap-south.api.example.com', latency: Infinity },
  },
  discoveryEndpoint: 'https://global.api.example.com/nearest-region',
  fallbackStrategy: 'next-fastest',   // on error, try next region
  healthCheckInterval: 30_000,
});

const data = await client.get('/api/data'); // automatically routes to nearest region
```

Show: latency measurement via `HEAD` requests to each region endpoint, the region selection algorithm, request retries with regional failover, and `navigator.connection.effectiveType` for adjusting the health check frequency on slow connections.""",

"""**Debug Scenario:**
A cloud-hosted app stores user sessions in a single Redis instance. When Redis has a maintenance window, ALL users are logged out simultaneously (sticky session problem).

Show: a multi-tier session storage strategy — primary Redis, secondary Redis replica (read only, fallback), and a degraded mode that falls back to encrypted JWT cookies (stateless, no Redis needed at all) for the duration of the outage. The JWT fallback has a short 15-minute expiry and the server automatically switches back to Redis sessions when it recovers, with a `x-session-degraded: true` header that the client can use to show a "reduced functionality" notice.""",

"""**Task (Code Generation):**
Implement a `createWebhookDispatcher` that delivers events with guaranteed at-least-once delivery:

```ts
const dispatcher = createWebhookDispatcher({
  storage: postgresQueue,    // persistent queue
  workers: 5,                // concurrent delivery workers
  delivery: {
    timeout: 10_000,
    retries: 5,
    backoff: 'exponential',  // 1s, 2s, 4s, 8s, 16s
  },
  signing: { algorithm: 'HMAC-SHA256', headerName: 'X-Webhook-Signature' },
  onDeliverySuccess: (event, attempt) => metrics.record('webhook_delivered'),
  onDeadLetter: (event) => alertOps('webhook permanently failed', event),
});

await dispatcher.dispatch({
  eventType: 'payment.completed',
  payload: { orderId: 'ord_1', amount: 99.99 },
  subscribers: ['https://partner-a.com/hooks', 'https://partner-b.com/hooks'],
});
```

Show: the persistent queue schema, worker pool processing, retry scheduling with exponential backoff, HMAC signing of payload, and the dead-letter queue after max retries.""",

"""**Debug Scenario:**
A developer builds a real-time collaborative feature using WebSockets, but load testing shows the WebSocket server becomes a bottleneck at 5,000 concurrent connections. The server is a single Node.js process.

Show: horizontal scaling with multiple Node.js WebSocket server processes, using Redis Pub/Sub as the message bus between processes (when user A sends a message, process 1 publishes to Redis, process 2 has user B subscribed and forwards the message), sticky session configuration in the load balancer (same client always routes to same WebSocket server to maintain connection state), and `socket.io`'s built-in Redis adapter that handles this pattern.""",

"""**Task (Code Generation):**
Build a `createEventualConsistencyChecker` for detecting stale reads after writes in distributed systems:

```ts
const checker = createEventualConsistencyChecker({
  primaryRead:  (id) => primaryDb.users.find(id),
  replicaRead:  (id) => replicaDb.users.find(id),
  equalityFn:   (a, b) => a.version === b.version,
  maxWait:      5000,   // wait up to 5s for replica to catch up
  pollInterval: 100,    // check every 100ms
});

// After a write:
await primaryDb.users.update(userId, { name: 'Alice' });
const { converged, latency } = await checker.waitForConvergence(userId);
// converged: true (replica caught up in 240ms)
// latency:   240ms (replication lag)
```

Show: the polling loop that stops when primary and replica return equal results, timeout handling, using this in integration tests to verify replication lag SLAs, and a monitoring dashboard endpoint that reports current replication lag.""",

"""**Debug Scenario:**
A GraphQL API built with Apollo Server 4 returns `null` for a field that should never be null, causing the entire query to return `null` at the parent level due to error propagation:

```graphql
type User {
  id: ID!
  profile: Profile!  # Non-null — if this resolver throws, parent becomes null!
}
```

In Apollo, if a non-null field resolver throws, the error propagates up to the nearest nullable parent. If `profile` is `!` (non-null) and it throws, `user` becomes `null`. Show: making the field nullable in the schema (`profile: Profile`) for resilience, using `@catch` directive (Apollo Gateway), wrapping the resolver in `try/catch` and returning a default profile, and the difference between Apollo's error masking (`formatError`) and `includeStacktraceInErrorResponses: false`.""",

]

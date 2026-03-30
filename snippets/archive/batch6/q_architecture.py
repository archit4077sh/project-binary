"""
snippets/q_architecture.py — BATCH 6: 55 brand-new Architecture questions
Zero overlap with batches 1-5 archives.
"""

Q_ARCHITECTURE = [

"""**Task (Code Generation):**
Implement a `createEventSourcingStore<State, Event>` for event-sourced state management:

```ts
const store = createEventSourcingStore<CartState, CartEvent>({
  initialState: { items: [], total: 0 },
  reducer: (state, event) => {
    switch (event.type) {
      case 'ITEM_ADDED': return addItem(state, event.item);
      case 'ITEM_REMOVED': return removeItem(state, event.itemId);
    }
  },
  persist: {
    adapter: new PostgresEventAdapter(db),
    snapshotEvery: 100,   // snapshot after 100 events to avoid replay from start
  },
});

store.dispatch({ type: 'ITEM_ADDED', item: product });
const currentState = store.getState();
const history = await store.replayFrom(timestamp);
```

Show: the event log append-only pattern, snapshot creation and restoration, replaying events from a snapshot, and event versioning (migrating old event shapes).""",

"""**Task (Code Generation):**
Build a `createCircuitBreaker<T>` for resilient external service calls:

```ts
const externalAPI = createCircuitBreaker({
  call: (url: string) => fetch(url).then(r => r.json()),
  failureThreshold: 5,      // open after 5 failures
  recoveryTimeout: 30_000,  // try again after 30s (half-open)
  successThreshold: 2,      // close after 2 consecutive successes
  onStateChange: (from, to) => metrics.record('circuit_state', { from, to }),
});

const data = await externalAPI.execute('/api/products');
// If circuit is OPEN: throws CircuitOpenError immediately (no network call)
// If circuit is HALF_OPEN: makes one test call
// If circuit is CLOSED: makes the call normally
```

Show: the three states (CLOSED/OPEN/HALF_OPEN), the state machine transitions, `CircuitOpenError` fast-fail, and a `getStatus()` method for health checks.""",

"""**Task (Code Generation):**
Implement a `createCQRS` (Command Query Responsibility Segregation) pattern for a feature:

```ts
// Command side (writes):
const commandBus = createCommandBus({
  handlers: {
    CreateOrder:   createOrderHandler(orderRepo, inventoryService),
    CancelOrder:   cancelOrderHandler(orderRepo, emailService),
    ShipOrder:     shipOrderHandler(orderRepo, shippingAPI),
  },
  middlewares: [authMiddleware, validationMiddleware, loggingMiddleware],
});

// Query side (reads — optimized for reading, separate data model):
const queryBus = createQueryBus({
  handlers: {
    GetOrderById:   getOrderByIdHandler(readDb),
    ListUserOrders: listUserOrdersHandler(readDb, cache),
  },
});

await commandBus.dispatch({ type: 'CreateOrder', userId, items });
const order = await queryBus.query({ type: 'GetOrderById', orderId });
```

Show: the command/query type separation (commands mutate, queries read), middleware pipeline for commands, and how to sync the read model from command side events.""",

"""**Task (Code Generation):**
Build a `createPluginSystem<PluginAPI>` framework for extensible applications:

```ts
const pluginAPI = createPluginSystem<PluginAPI>({
  hooks: ['beforeRender', 'afterSave', 'onError'],
  api: { db, cache, logger },
});

// Third-party plugins:
pluginAPI.register({
  name: 'analytics-plugin',
  version: '1.0.0',
  onMount: (api) => {
    api.hooks.afterSave.tap('analytics', (event) => {
      api.db.analytics.record(event);
    });
  },
});

// Core:
await pluginAPI.hooks.afterSave.call({ entityType: 'product', id: productId });
```

Show: the tapable hook system (like webpack's), plugin lifecycle (`onMount`, `onUnmount`), dependency resolution between plugins (plugin A requires plugin B), version compatibility checking, and isolating plugin errors (one failing plugin doesn't crash the app).""",

"""**Task (Code Generation):**
Implement a `createMicroFrontendOrchestrator` for module federation:

```ts
const orchestrator = createMicroFrontendOrchestrator({
  remotes: {
    checkout: { url: 'https://checkout.internal/remoteEntry.js', scope: 'checkout' },
    catalog:  { url: 'https://catalog.internal/remoteEntry.js',  scope: 'catalog' },
    profile:  { url: 'https://profile.internal/remoteEntry.js',  scope: 'profile' },
  },
  shared: {
    react:        { singleton: true, requiredVersion: '^18.0.0' },
    'react-dom':  { singleton: true, requiredVersion: '^18.0.0' },
    'design-system': { singleton: true },
  },
  fallback: (remoteName) => import(`./fallbacks/${remoteName}`),
});

const CheckoutApp = await orchestrator.load('checkout', './App');
```

Show: the Webpack Module Federation config for each remote, dynamic remote loading (`__webpack_init_sharing__`, `__webpack_share_scopes__`), version negotiation for shared modules, fallback loading when a remote fails, and cross-remote communication via a shared event bus.""",

"""**Task (Code Generation):**
Build a `createSagaOrchestrator` for long-running distributed transactions:

```ts
const checkoutSaga = createSaga('checkout', {
  steps: [
    { name: 'reserveInventory',  action: inventoryService.reserve,  compensate: inventoryService.release },
    { name: 'chargePayment',     action: paymentService.charge,     compensate: paymentService.refund },
    { name: 'createShipment',    action: shippingService.create,    compensate: shippingService.cancel },
    { name: 'sendConfirmation',  action: emailService.sendConfirm,  compensate: null }, // no compensation needed
  ],
  onComplete: (ctx) => db.orders.update(ctx.orderId, { status: 'confirmed' }),
  onFail:     (ctx, failedStep, error) => db.orders.update(ctx.orderId, { status: 'failed', reason: error.message }),
});

await checkoutSaga.execute({ orderId, userId, items });
```

Show: the step-by-step execution with rollback on failure (reverse compensation for all completed steps), persisting saga state to survive crashes, idempotency keys per step (retry-safe), and the saga log in the database for audit trails.""",

"""**Task (Code Generation):**
Implement a `createRepositoryPattern<Entity>` with caching and query builder:

```ts
const UserRepo = createRepository<User>({
  table: 'users',
  db,
  cache: redis,
  cacheTTL: 300,
  cacheKey: (id) => `user:${id}`,
});

// Typed query builder:
const admins = await UserRepo.findMany({
  where: { role: 'admin', active: true },
  orderBy: { createdAt: 'desc' },
  take: 10,
  include: { posts: true, permissions: true },
});

// Cache-first read:
const user = await UserRepo.findById('u1'); // checks cache first, falls through to DB
await UserRepo.invalidate('u1');            // clears cache entry
```

Show: the cache-aside pattern (read-through + write-through), the typed `where` clause using `Partial<Entity>` or Prisma-style filters, and `UserRepo.findMany` with pagination.""",

"""**Task (Code Generation):**
Build a `createFeatureToggle` system with percentage rollout and user targeting:

```ts
const flags = createFeatureToggle({
  source: {
    type: 'remote',
    url: 'https://flags.example.com/api',
    pollInterval: 60_000,
  },
  defaults: {
    newCheckoutFlow:   { enabled: false },
    aiRecommendations: { enabled: false, rolloutPercentage: 10 },
    darkMode:          { enabled: true },
  },
});

const user = { id: 'u1', plan: 'pro', country: 'US' };

flags.isEnabled('aiRecommendations', user);
// true for 10% of users, consistent hashing by user.id

flags.isEnabled('newCheckoutFlow', user);
// false (disabled globally)
```

Show: consistent user bucketing using `hash(flagName + userId) % 100 < rolloutPercentage`, targeting rules (`{ criteria: { plan: 'pro' } }` — enable for pro users), SSR support (flags resolved server-side and hydrated to client), and the `useFeatureFlag` React hook.""",

"""**Task (Code Generation):**
Implement a `createStreamProcessor<Input, Output>` for backpressure-aware stream processing:

```ts
const processor = createStreamProcessor<LogEntry, ProcessedLog>({
  transform: (entry) => ({
    ...entry,
    level: entry.severity > 5 ? 'high' : 'normal',
    parsed: parseLogMessage(entry.raw),
  }),
  batchSize: 100,
  flushInterval: 5000,         // flush every 5s even if batch not full
  backpressure: {
    highWaterMark: 1000,       // pause input when buffer > 1000
    lowWaterMark: 200,         // resume input when buffer < 200
  },
  errorStrategy: 'skip',       // skip malformed entries
  onFlush: (batch) => elasticsearchClient.bulk(batch),
});

const readable = getLogStream();
readable.pipe(processor.writable);
processor.readable.pipe(esWriter);
```

Show: implementing as a Node.js `Transform` stream, `push(null)` when done, backpressure via `highWaterMark`, batching with `setTimeout` for time-based flushing, and `objectMode: true` for object streams.""",

"""**Task (Code Generation):**
Build a `createCDNPurgeStrategy` for intelligent cache invalidation across CDN nodes:

```ts
const cdnPurge = createCDNPurgeStrategy({
  provider: 'cloudflare',
  zoneId:   process.env.CF_ZONE_ID!,
  apiToken: process.env.CF_API_TOKEN!,
  strategies: {
    content: 'tag',   // purge by cache tag (most efficient)
    pricing: 'path',  // purge specific URL patterns
    images:  'prefix', // purge all /images/* URLs
  },
});

// After a content update:
await cdnPurge.purge({ type: 'content', tags: ['product-123', 'category-electronics'] });
await cdnPurge.purge({ type: 'pricing', path: '/api/prices/product-123' });
```

Show: Cloudflare's Cache Tag purge API, surrogate key headers (`Cache-Tag: product-123`) set by the origin, bulk purge batching (Cloudflare: max 30 tags per request), and a circuit breaker around CDN API calls.""",

"""**Task (Code Generation):**
Implement a `createObservabilityMiddleware` for Express/Node.js with OpenTelemetry:

```ts
app.use(createObservabilityMiddleware({
  serviceName: 'api-gateway',
  tracing: {
    exporter: new OTLPTraceExporter({ url: process.env.OTEL_EXPORTER_URL }),
    autoInstrument: ['http', 'pg', 'redis'],
  },
  metrics: {
    exporter: new PrometheusExporter({ port: 9464 }),
    collect: ['http_requests_total', 'http_request_duration_seconds', 'active_connections'],
  },
  logging: {
    format: 'json',
    includeTraceId: true,   // correlate logs with traces
  },
}));
```

Show: `opentelemetry-api` span creation and propagation, `@opentelemetry/auto-instrumentations-node` for automatic instrumentation, Prometheus metric types (Counter, Histogram, Gauge), correlating logs with trace ID, and health check endpoint `/metrics` for Prometheus scraping.""",

"""**Task (Code Generation):**
Build a `createTestDoubles` factory for deterministic testing of external dependencies:

```ts
const doubles = createTestDoubles({
  db: mockDatabase({
    users: [{ id: 'u1', email: 'alice@test.com', role: 'admin' }],
    posts: [],
  }),
  email: spyEmailService(),       // records calls, doesn't send
  payment: stubPaymentService({   // always returns success
    charge: () => ({ transactionId: 'txn_test_123', status: 'succeeded' }),
  }),
  time: frozenClock(new Date('2024-01-15T10:00:00Z')),
});

// Usage in tests:
const result = await createOrder(doubles.db, doubles.payment, { userId: 'u1' });
expect(doubles.email.calls).toHaveLength(1);
expect(doubles.email.calls[0].to).toBe('alice@test.com');
```

Show: the `mockDatabase` implementing the repository interface in memory, `spyEmailService` recording calls in an array, `stubPaymentService` returning preset responses, and `frozenClock` overriding `Date.now()` and `setTimeout`.""",

"""**Task (Code Generation):**
Implement a `createSecretsManager` that fetches and caches secrets from AWS Secrets Manager:

```ts
const secrets = createSecretsManager({
  region: 'us-east-1',
  cacheTTL: 3600_000,         // re-fetch after 1 hour
  refreshBefore: 300_000,     // refresh 5 minutes before expiry
  onRefreshError: (err, key) => logger.error('Failed to refresh secret', { key, err }),
});

const dbPassword = await secrets.get('prod/database/password');
const apiKey     = await secrets.get('prod/stripe/api-key');
// Subsequent calls within TTL: cached, no AWS API call
```

Show: AWS SDK `GetSecretValueCommand`, caching with timestamps, proactive refresh before expiry using `setInterval`, error handling (return stale cached value on refresh failure), and TypeScript generics for structured secrets (`secrets.getJSON<DBConfig>('prod/database')`).""",

"""**Task (Code Generation):**
Build a `createAuditTrail` system that logs all data mutations with rollback capability:

```ts
const auditTrail = createAuditTrail({
  storage: new PostgresAuditStorage(db),
  captureFields: ['createdBy', 'updatedBy', 'timestamp'],
  exclude: ['password', 'accessToken'],
  retentionDays: 365,
});

// Wraps any entity repository:
const auditedUserRepo = auditTrail.wrap(UserRepository);

await auditedUserRepo.update('u1', { role: 'admin' });
// Logs: { entityType:'user', entityId:'u1', action:'UPDATE', before:{role:'user'}, after:{role:'admin'}, actor:'admin@example.com', at: Date }

// Rollback:
await auditTrail.rollback({ entityType: 'user', entityId: 'u1', toTimestamp: oneDayAgo });
```

Show: the before/after snapshot storage (using PostgreSQL JSONB), field exclusion for sensitive data, the `rollback` function replaying inverse operations, and querying the audit log by entity or actor.""",

"""**Task (Code Generation):**
Implement a `createHealthCheck` endpoint with dependency checks and circuit integration:

```ts
const health = createHealthCheck({
  checks: {
    database: async () => {
      await db.raw('SELECT 1');
      return { status: 'up', latency: lastDbLatency };
    },
    redis: async () => {
      const pong = await redis.ping();
      return { status: pong === 'PONG' ? 'up' : 'down' };
    },
    externalAPI: circuitBreaker.getStatus, // uses circuit state
  },
  timeouts: { database: 2000, redis: 1000, externalAPI: 500 },
  criticalChecks: ['database'],   // If database is down, overall status = down
  degradedChecks: ['externalAPI'], // If externalAPI is down, overall status = degraded
});

app.get('/health', health.handler);
// { status: 'up' | 'degraded' | 'down', checks: {...}, version: '1.2.3', uptime: 3600 }
```

Show: parallel check execution with individual timeouts, overall status aggregation logic, the Kubernetes readiness vs liveness probes distinction, and caching health check results for 5 seconds to prevent health-check-induced load.""",

# ── Debugging ─────────────────────────────────────────────────────────────────

"""**Debug Scenario:**
A microservices architecture has "thundering herd" problems — when a cache node restarts, all 100 services immediately query the database simultaneously, bringing it down:

```ts
async function getData(key: string) {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);
  // All 100 services hit DB simultaneously when cache is empty!
  const data = await db.query('SELECT * FROM data WHERE key = $1', [key]);
  await redis.set(key, JSON.stringify(data), 'EX', 3600);
  return data;
}
```

Show: implementing a distributed lock (Redis SETNX "mutex key" with expiry) so only ONE service queries the DB while others wait, probabilistic early expiration (refresh cache when TTL < 5% remaining, not at expiry), and jittered cache TTLs (add ± 10% randomness to prevent mass expiry at the same time).""",

"""**Debug Scenario:**
A GraphQL subscription is sending duplicate events to subscribers — every update triggers the subscription 3x:

```ts
schema.subscriptionType?.addFields({
  postUpdated: {
    subscribe: () => pubsub.asyncIterator(['POST_UPDATED']),
    resolve: (payload) => payload,
  },
});

// On post update — publishing 3 times instead of 1:
await pubsub.publish('POST_UPDATED', { post });
await pubsub.publish('POST_UPDATED', { post }); // BUG: copied by mistake
await pubsub.publish('POST_UPDATED', { post }); // BUG
```

Show: auditing all publish call sites for the subscription topic, using a unique event ID (`eventId: uuid()`) and filtering duplicate IDs at the subscriber, and the Apollo Subscription server's built-in deduplication with `filter` function.""",

"""**Debug Scenario:**
A Redis-based session store causes "ECONNRESET" errors under high load, causing users to be logged out:

```ts
app.use(session({
  store: new RedisStore({ client: redis }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
}));
```

Under high load, Redis connections are exhausted. `ECONNRESET` means the connection was dropped. Show: configuring `ioredis` with a connection pool (`maxRetriesPerRequest: 3`, `retryStrategy`), using `connect-redis` with retry options, monitoring Redis connection count (`redis.info('clients')`), and horizontal Redis scaling with Cluster mode or Redis Sentinel for high availability.""",

"""**Debug Scenario:**
A gRPC microservice has a memory leak — each unary RPC call creates a new `grpc.Client` instance that is never destroyed:

```ts
async function callInventoryService(productId: string) {
  const client = new InventoryServiceClient(url, credentials); // new client per request!
  const response = await promisify(client.getStock.bind(client))({ productId });
  // client never closed!
  return response;
}
```

gRPC clients maintain a connection pool internally. Creating a new client per request creates a new pool, which is never closed. Show: creating the client once at module level (singleton), calling `client.close()` on graceful shutdown, using `@grpc/grpc-js`'s built-in keepalive options, and a client pool pattern for services that require parallel connections.""",

"""**Debug Scenario:**
A message queue consumer sometimes processes the same message twice, creating duplicate database records:

```ts
consumer.on('message', async (msg) => {
  const order = JSON.parse(msg.content.toString());
  await db.orders.create({ data: order }); // May run twice!
  channel.ack(msg);                        // Ack AFTER processing
});
```

If the service crashes between `create` and `ack`, RabbitMQ redelivers the message. Show: implementing idempotency by storing `message.properties.messageId` in a `processed_messages` table, checking before processing (`if (await alreadyProcessed(msgId)) return channel.ack(msg)`), using PostgreSQL's `ON CONFLICT DO NOTHING` for the idempotency record and the order creation in a single transaction, and `msg.fields.redelivered` flag for early detection.""",

"""**Debug Scenario:**
A multi-region deployment has diverging data — writes to region A aren't appearing in region B:

```ts
// Database: CockroachDB with multi-region config
// Primary region: us-east-1
// Secondary region: eu-west-1

// User in EU writes data, reads it back immediately → shows old data!
const result = await db.users.update({ where: { id }, data: { name } });
const freshUser = await db.users.findUnique({ where: { id } }); // stale!
```

Read-after-write consistency is not guaranteed across regions — the read may route to a secondary region replica that hasn't caught up. Show: using `Durable` reads in CockroachDB (`SET locality_optimized_search TO OFF`), read-your-writes sessions (`BEGIN; ... COMMIT` keeps reads on the same node), routing reads to the region that just accepted the write, and eventual consistency acceptance with optimistic UI updates.""",

"""**Debug Scenario:**
A Kubernetes deployment of a Node.js app shows "502 Bad Gateway" errors during deploys — a few seconds of downtime during each rolling update:

```yaml
spec:
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

During rolling update, the old pod receives `SIGTERM` and stops accepting new connections immediately, but the Load Balancer hasn't removed it from rotation yet — requests during this window get 502. Show: adding a `preStop` hook with `sleep 5` to give the LB time to deregister (`lifecycle.preStop.exec.command: ['sleep', '5']`), graceful shutdown in Node.js (`server.close(() => process.exit(0))`), and `terminationGracePeriodSeconds: 30` to allow in-flight requests to complete.""",

"""**Debug Scenario:**
A distributed lock using Redis `SETNX` has a race condition — two processes both acquire the lock simultaneously:

```ts
async function acquireLock(key: string, ttl: number) {
  const acquired = await redis.setnx(key, 'locked');
  if (acquired) {
    await redis.expire(key, ttl); // NOT ATOMIC with setnx!
    return true;
  }
  return false;
}
```

Between `setnx` and `expire`, the process might crash — the lock is never released (deadlock). Two processes could both see `setnx=0` if the lock expired between their checks. Show: using `SET key value EX ttl NX` (atomic single command), Redlock algorithm for distributed locking across multiple Redis nodes, and the unique lock token value for safe release (`SET key uuid EX ttl NX; ...if GET key === uuid: DEL key`).""",

"""**Debug Scenario:**
An event-driven system using Kafka shows messages processing out of order — newer messages are sometimes processed before older ones for the same entity:

```ts
// Multiple consumers in a consumer group, each processing messages concurrently
consumer.on('message', async (msg) => {
  await processOrder(msg.value.orderId, msg.value); // concurrent!
});
```

Kafka guarantees ordering within a partition but not across partitions. Multiple consumers mean messages for the same order can be on different partitions. Show: using the `orderId` as the Kafka partition key (`{ key: order.id, value: JSON.stringify(event) }`) to ensure all events for an order go to the same partition, sequential processing within a partition (one consumer per partition, no concurrency within the handler), and the consumer group partition assignment strategy.""",

"""**Debug Scenario:**
An API Gateway's rate limiter allows burst requests that exceed the intended rate:

```ts
// Token bucket rate limiter: 100 requests/minute
const limiter = new TokenBucket({ capacity: 100, refillRate: 100 / 60 });

// A client sends 100 requests in 1 second → all allowed!
// Then 0 requests for 59 seconds → bucket refills to 100
// Then 100 requests in 1 second again → all allowed!
// In 2 seconds: 200 requests processed — double the intended rate!
```

Token bucket allows burst equal to bucket capacity at any time. Show: the sliding window log algorithm (stores timestamps of each request, counts requests in the past 60 seconds — no burst possible), the sliding window counter (compromise: tracks current and previous window counts, interpolates), and `@upstash/ratelimit`'s implementation of each strategy.""",

"""**Debug Scenario:**
A Next.js API route that calls a database connection pool is hitting "too many connections" in production:

```ts
// lib/db.ts — runs on every import!
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,
});
```

In Next.js API routes (Serverless Functions), each function invocation may import `db.ts` fresh, creating a NEW pool with 10 connections. With 100 concurrent requests, that's 1000 connections. Show: using `globalThis` to reuse the pool across invocations (`globalThis.__pgPool ??= new Pool(...)`), PgBouncer for connection pooling at the infrastructure level (thousands of app connections share a fixed pool), and Neon's serverless driver which uses HTTP/WebSocket for connection-less queries.""",

"""**Debug Scenario:**
A webhook receiver service sometimes misses webhook events because the HTTP response times out before the event is fully processed:

```ts
app.post('/webhooks', async (req, res) => {
  const event = req.body;
  await processWebhookEvent(event); // Takes 5-10 seconds!
  res.json({ received: true });     // Sender times out after 3 seconds!
});
```

Webhook senders expect a fast `200 OK` response (typically < 5 seconds). If they don't get it, they retry, causing duplicate processing. Show: responding immediately with `200 OK`, then processing asynchronously (`res.json({ received: true }); processInBackground(event)`), persisting to a queue (Redis, BullMQ) and processing separately, and using the webhook event `id` for idempotency (track processed IDs to skip retries).""",

"""**Debug Scenario:**
A service-to-service authentication using short-lived JWTs is failing frequently because the token issuance service and the consuming service have clock skew:

```ts
// Token issuer: generates JWT with 60-second expiry
const token = jwt.sign({ sub: serviceId }, secret, { expiresIn: 60 });

// Consumer: validates with current time
jwt.verify(token, secret); // Fails! Consumer clock is 90s ahead of issuer!
```

60-second JWT verified by a service whose clock is 90 seconds ahead → token is already expired. Show: adding clock skew tolerance to `jwt.verify` (`{ clockTolerance: 120 }` — allow ±2 minutes), increasing token expiry to 5-15 minutes for service tokens, using NTP synchronization across all services, and the `iat` (issued at) vs `exp` (expires at) claims.""",

"""**Debug Scenario:**
A background job that processes images is using 100% CPU on a single core and taking 30 minutes per batch, blocking all other work in the process:

```ts
// Image processing worker (single-threaded):
for (const image of images) {
  await sharp(image.buffer).resize(800).toFile(image.output); // CPU-bound!
}
```

`sharp` is CPU-intensive. Running sequentially in Node.js's event loop blocks other work. Show: distributing work across `worker_threads` (`os.cpus().length` workers), using a `WorkerPool` to fan out images to workers, `sharp`'s built-in thread pool (`sharp.concurrency(N)`) as a simpler alternative, and `Promise.allSettled` for parallel processing with error collection.""",

"""**Debug Scenario:**
An Elasticsearch index has degraded write performance and frequent GC pauses after 6 months. The index has 500M documents and was never optimized:

```ts
// Every save creates a new Lucene segment:
await es.index({ index: 'events', document: event });
// After 6 months: thousands of tiny segments → slow search + high GC
```

Elasticsearch auto-merges segments, but aggressive writes outpace merging. Show: scheduling `forcemerge` during low-traffic windows (`POST /events/_forcemerge?max_num_segments=1`), enabling `index.merge.policy.segments_per_tier: 5` for faster auto-merging, configuring `refresh_interval: 30s` for high-throughput indexes (fewer segments), time-based index rotation (daily/weekly indices with ILM for large event streams), and shard size optimization (target 10-50GB per shard).""",

"""**Debug Scenario:**
A REST API designed with resource-oriented URLs breaks down when implementing a complex workflow that spans multiple resources:

```ts
// Simple CRUD — fine with REST:
POST   /orders
GET    /orders/:id
PATCH  /orders/:id
DELETE /orders/:id

// But a "checkout" workflow needs to:
// 1. Reserve inventory
// 2. Create payment intent
// 3. Create order
// 4. Send confirmation email
// All atomically — how to model this in REST?
PATCH /orders/:id { action: 'checkout' } // RPC disguised as REST — bad design
```

Show: modeling as a resource (`POST /checkout-sessions`), the command pattern endpoint (`POST /orders/:id/actions/checkout`), using a CQRS command bus (`POST /commands/CheckoutOrder`), and when to abandon REST for GraphQL mutations or RPC (gRPC) for complex workflows.""",

"""**Debug Scenario:**
A React frontend's API calls are failing with CORS errors after a backend deployment switched from a single API server to multiple services behind a gateway:

```
Access-Control-Allow-Origin header missing from https://api.example.com/v2/products
```

The new API Gateway handles routing but doesn't forward the CORS `OPTIONS` preflight to the origin services — it returns `403` for the preflight. Show: handling CORS at the gateway level (not in each service), configuring Kong/AWS API Gateway/nginx CORS for `OPTIONS` preflight responses, the correct CORS response headers (`Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`), and why `*` doesn't work with `credentials: 'include'`.""",

"""**Debug Scenario:**
A multi-tenant SaaS app has a data isolation bug — querying a tenant's data sometimes returns another tenant's records:

```ts
// Row-level security via app-level filter:
const data = await db.records.findMany({
  where: {
    tenantId: req.tenant.id, // Correct filter
    ...userProvidedFilters,  // BUG: userProvidedFilters can override tenantId!
  },
});
```

If `userProvidedFilters` contains `{ tenantId: 'other-tenant' }`, the where clause uses the user's provided `tenantId` instead of the session's tenant. Show: enforcing `tenantId` with `AND` semantics rather than merged `where` (`db.records.findMany({ where: { AND: [{ tenantId: reqTenantId }, userFilters] } })`), using PostgreSQL Row-Level Security (RLS) as a defense-in-depth measure, and audit logging for cross-tenant data access attempts.""",

"""**Debug Scenario:**
A Next.js server that handles file uploads crashes with "out of memory" when users upload large files:

```ts
export const config = { api: { bodyParser: { sizeLimit: '50mb' } } };

export default async function handler(req, res) {
  const buffer = req.body; // 50MB loaded into memory!
  await processAndUploadToS3(buffer);
}
```

Loading the entire 50MB into memory per request is unsustainable under concurrent load. Show: using `busboy` or `formidable` for streaming multipart parsing, piping the Node.js request stream directly to S3 (`s3.upload({ Body: req }).promise()`), using presigned URLs for direct browser-to-S3 upload (bypassing the server entirely), and `Content-Length` validation before reading the body.""",

"""**Debug Scenario:**
A Prisma ORM query causes N+1 issues that aren't detected in development (small dataset) but crash production (millions of rows):

```ts
const users = await prisma.user.findMany({ take: 100 });
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { authorId: user.id } }); // N+1!
  process(user, posts);
}
```

100 users → 101 database queries. Show: using Prisma's `include: { posts: true }` to join in one query, `select` for specific field projection, the `prisma.$extends` logging extension to detect N+1 at development time, and `prisma.$metrics` for tracking query counts in production.""",

]

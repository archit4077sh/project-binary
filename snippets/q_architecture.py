"""
snippets/q_architecture.py — BATCH 7: 55 brand-new Architecture questions
Zero overlap with batches 1-6 archives.
"""

Q_ARCHITECTURE = [

'''**Task (Code Generation):**
Implement a `createOutboxPattern` for reliable message publishing with at-least-once delivery:

```ts
// Write the order AND the outbox message in one transaction — no dual-write problem:
await db.transaction(async (txn) => {
  const order = await txn.orders.create({ data: orderData });
  await txn.outbox.create({
    data: {
      aggregateId: order.id,
      aggregateType: 'Order',
      eventType: 'OrderCreated',
      payload: JSON.stringify(order),
      status: 'PENDING',
    }
  });
  return order;
});

// Separate outbox relay process polls and publishes:
const outboxRelay = createOutboxRelay({
  db,
  messageQueue: rabbitMQ,
  pollInterval: 1000,
  batchSize: 100,
  onPublished: async (id) => db.outbox.update({ where: { id }, data: { status: 'PUBLISHED' } }),
});
```

Show: the transactional outbox pattern (write message and business data in same DB transaction), the polling relay process, idempotent consumers (process by outbox ID), and the `Change Data Capture` (CDC) alternative using Debezium instead of polling.''',

'''**Task (Code Generation):**
Build a `createAggregateRoot<State, Event>` for Domain-Driven Design event sourcing:

```ts
const OrderAggregate = createAggregateRoot<OrderState, OrderEvent>({
  initialState: { id: '', status: 'draft', items: [], total: 0 },
  handlers: {
    OrderCreated:  (state, event) => ({ ...state, id: event.orderId, status: 'pending' }),
    ItemAdded:     (state, event) => ({ ...state, items: [...state.items, event.item] }),
    OrderConfirmed:(state, event) => ({ ...state, status: 'confirmed', confirmedAt: event.at }),
    OrderCancelled:(state, event) => ({ ...state, status: 'cancelled', reason: event.reason }),
  },
});

const order = new OrderAggregate();
order.apply({ type: 'OrderCreated', orderId: 'o1' });
order.apply({ type: 'ItemAdded', item: { id: 'p1', price: 99 } });

// Rebuild from event stream:
const rebuilt = OrderAggregate.rehydrate(eventStream);
```

Show: the `apply` method dispatching to the correct handler, `rehydrate` reducing over historical events, uncommitted events buffer for persistence, optimistic concurrency (`expectedVersion` for writes), and the aggregate version for conflict detection.''',

'''**Task (Code Generation):**
Implement a `createBulkheadPattern<T>` for isolating services using thread/concurrency pools:

```ts
const apiCallBulkhead = createBulkhead<UserData>({
  maxConcurrent: 10,    // max 10 in-flight calls
  maxQueue: 50,         // max 50 queued
  timeout: 5000,        // 5s timeout per request
  name: 'external-api',
  onReject: (reason) => metrics.increment('bulkhead.rejection', { name: 'external-api', reason }),
});

// All calls to this external API go through the bulkhead:
const user = await apiCallBulkhead.execute(() => externalAPI.getUser(userId));
// If 10 are already in-flight and queue is full:
// Throws BulkheadRejectionError immediately (fail-fast — don't make caller wait)
```

Show: using a semaphore (`Semaphore` class with `acquire/release`) for the concurrency limit, a priority queue for the waiting pool, timeout via `Promise.race([work, setTimeout(reject, timeout)])`, metrics for monitoring rejection rates, and combining with `createCircuitBreaker` for full resilience.''',

'''**Task (Code Generation):**
Build a `createSpecificationPattern<T>` for composable business rule validation:

```ts
const isPremiumUser    = new Specification<User>((user) => user.plan === 'premium');
const isVerifiedEmail  = new Specification<User>((user) => user.emailVerified);
const isAdultUser      = new Specification<User>((user) => user.age >= 18);
const hasActiveAccount = new Specification<User>((user) => user.status === 'active');

// Compose:
const canAccessPremiumContent = isPremiumUser
  .and(isVerifiedEmail)
  .and(isAdultUser.or(hasActiveAccount))
  .not(isBannedUser);

// Use:
if (!canAccessPremiumContent.isSatisfiedBy(currentUser)) {
  throw new AccessDeniedError(canAccessPremiumContent.whyNotSatisfiedBy(currentUser));
}
```

Show: the `Specification<T>` abstract class with `and`, `or`, `not` methods returning new composite specifications, `whyNotSatisfiedBy` returning the failing sub-specification names, and using specifications for filtering collections (`users.filter(spec.isSatisfiedBy.bind(spec))`).''',

'''**Task (Code Generation):**
Implement a `createReactiveGraph<N, E>` for building event-driven dependency graphs:

```ts
const graph = createReactiveGraph<ComputeNode, DataEdge>();

const priceNode    = graph.addNode({ id: 'price',    compute: () => fetchPrice() });
const taxNode      = graph.addNode({ id: 'tax',      compute: (inputs) => inputs.price * 0.2 });
const discountNode = graph.addNode({ id: 'discount', compute: (inputs) => applyDiscounts(inputs.price) });
const totalNode    = graph.addNode({ id: 'total',    compute: (inputs) => inputs.price + inputs.tax - inputs.discount });

graph.addEdge(priceNode, taxNode,      { name: 'price' });
graph.addEdge(priceNode, discountNode, { name: 'price' });
graph.addEdge(taxNode,      totalNode, { name: 'tax' });
graph.addEdge(discountNode, totalNode, { name: 'discount' });
graph.addEdge(priceNode,    totalNode, { name: 'price' });

// On price change: auto-propagates through the DAG:
priceNode.invalidate();
const total = await totalNode.getValue(); // Recomputes tax, discount, then total
```

Show: topological sort for evaluation order, memoized node values (only recompute on invalidation), change propagation using BFS/DFS from the invalidated node, and cycle detection.''',

'''**Task (Code Generation):**
Build a `createGraphQLDataLoader` for N+1 query elimination:

```ts
// Without DataLoader — N+1 queries in GraphQL:
// Query 100 posts → 100 queries for each post's author

// With DataLoader:
const userLoader = new DataLoader<string, User>(async (userIds) => {
  const users = await db.users.findMany({ where: { id: { in: [...userIds] } } });
  return userIds.map(id => users.find(u => u.id === id) ?? new Error(`User ${id} not found`));
}, { cache: true, maxBatchSize: 100 });

// In resolvers:
const resolvers = {
  Post: {
    author: (post, _, { loaders }) => loaders.user.load(post.authorId),
    // 100 post resolvers all call load() → batched into ONE query!
  },
};
```

Show: the DataLoader constructor requiring batched load function returning values in same order as IDs, `load()` vs `loadMany()`, per-request DataLoader instances (to avoid cross-request caching), and `clearAll()` for cache invalidation.''',

'''**Task (Code Generation):**
Implement a `createRateLimitedQueue` for throttling API calls to third-party services:

```ts
const stripeQueue = createRateLimitedQueue({
  maxPerSecond: 25,           // Stripe: 25 RPS on free tier
  maxPerMinute: 500,
  burst: { max: 50, window: 1000 },   // Allow up to 50 requests in a burst window
  priority: {
    HIGH:   0,   // Process immediately
    NORMAL: 100, // 100ms delay
    LOW:    500, // 500ms delay
  },
  onThrottle: (queued) => logger.warn('Stripe rate limit — queued', { queued }),
});

// Enqueue calls:
const charge = await stripeQueue.enqueue(() => stripe.charges.create(chargeData), { priority: 'HIGH' });
```

Show: the token bucket algorithm for burst management, the priority queue sorted by deadline, measuring actual throughput with a sliding window counter, and `onThrottle` alerting when the queue depth exceeds a threshold.''',

'''**Task (Code Generation):**
Build a `createWebhookDeliveryEngine` for reliable webhook dispatch:

```ts
const webhookEngine = createWebhookDeliveryEngine({
  storage: new PostgresWebhookStorage(db),
  retry: {
    maxAttempts: 7,
    backoff: (attempt) => Math.min(Math.pow(2, attempt) * 1000, 3_600_000),
    // 2s, 4s, 8s, 16s, 32s, 64s, 1h
  },
  signature: {
    algorithm: 'sha256',
    headerName: 'X-Webhook-Signature',
    secret: (endpointId) => getEndpointSecret(endpointId),
  },
  timeout: 30_000,
  concurrency: 50,
});

await webhookEngine.dispatch({
  endpointId: 'ep_1',
  eventType: 'payment.completed',
  payload: { orderId, amount, currency },
});
```

Show: HMAC signature generation (`crypto.createHmac('sha256', secret).update(payload).digest('hex')`), the `attempts` table with status tracking, exponential backoff retry scheduling, marking endpoints as `DISABLED` after exhausting retries, and `svix` library as a managed alternative.''',

'''**Task (Code Generation):**
Implement a `createMultiRegionRouter` for latency-based request routing:

```ts
const router = createMultiRegionRouter({
  regions: {
    'us-east-1': { endpoint: 'https://api-us.example.com', latency: measureLatency('us-east-1') },
    'eu-west-1': { endpoint: 'https://api-eu.example.com', latency: measureLatency('eu-west-1') },
    'ap-south-1':{ endpoint: 'https://api-ap.example.com', latency: measureLatency('ap-south-1') },
  },
  strategy: 'lowest-latency',          // or 'round-robin', 'failover'
  healthCheck: { interval: 30_000, path: '/health', threshold: 2 },
  fallback: 'us-east-1',               // Use this region if all health checks fail
  stickySession: {
    enabled: true,
    cookieName: 'preferred-region',
    ttl: 60 * 60 * 24,
  },
});
```

Show: measuring region latency using `performance.now()` with a lightweight ping (HEAD /health), the health check failure counter and circuit-breaking unhealthy regions, sticky routing via cookie (once a user is routed to a region, keep them there), and Cloudflare's anycast routing as an alternative.''',

'''**Task (Code Generation):**
Build a `createSchemaMigration` framework for database schema versioning:

```ts
const migrationEngine = createSchemaMigration({
  db,
  migrationsDir: './migrations',
  migrationsTable: 'schema_migrations',
  checksumValidation: true,  // Detect if a previously-run migration file changed
});

// Migration file: 001_create_users.ts
export const up = async (db: DatabaseClient) => {
  await db.raw(`CREATE TABLE users (id UUID PRIMARY KEY, email TEXT UNIQUE NOT NULL, created_at TIMESTAMPTZ DEFAULT NOW())`);
  await db.raw(`CREATE INDEX idx_users_email ON users (email)`);
};

export const down = async (db: DatabaseClient) => {
  await db.raw(`DROP TABLE IF EXISTS users`);
};

// Run:
await migrationEngine.up();      // Apply all pending migrations in order
await migrationEngine.down(3);   // Roll back last 3 migrations
await migrationEngine.status();  // List applied vs pending migrations
```

Show: the `schema_migrations` table tracking applied migrations, file ordering by timestamp prefix, the checksum comparison to detect tampering with applied migrations, and running migrations in a transaction with rollback on error.''',

'''**Task (Code Generation):**
Implement a `createApiVersioningStrategy` for managing breaking API changes:

```ts
// URL versioning: /api/v1/users, /api/v2/users
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// Header versioning: 'API-Version: 2024-01-01'
const versionMiddleware = createVersionMiddleware({
  header: 'API-Version',
  supported: ['2023-01-01', '2023-07-01', '2024-01-01'],
  default: '2023-01-01',
  deprecated: ['2023-01-01'],  // Respond with Deprecation header
  sunset: { '2023-01-01': new Date('2025-01-01') },  // Sunset: indicate end-of-life
});

// Type-safe version-aware handler:
router.get('/users/:id', withVersion({
  '2023-07-01': getUser_v2,
  '2024-01-01': getUser_v3,
}));
```

Show: the `Deprecation: true` and `Sunset: <date>` response headers per RFC 8594, the version router pattern, version negotiation (find the earliest supported version ≥ requested), and `version-range` header for requesting a range of compatible versions.''',

'''**Task (Code Generation):**
Build a `createCacheHierarchy<T>` with L1/L2/L3 caching layers:

```ts
const cache = createCacheHierarchy<Product>({
  L1: { store: new Map(),            ttl: 60_000,       maxSize: 100  }, // In-process memory
  L2: { store: new RedisStore(redis), ttl: 600_000,      maxSize: 10000 }, // Shared Redis
  L3: { store: new CdnStore({ ... }), ttl: 3_600_000,    maxSize: null  }, // CDN edge cache
  keyFn: (id: string) => `product:${id}`,
  serialize:   JSON.stringify,
  deserialize: (s) => JSON.parse(s) as Product,
  onHit: (layer) => metrics.increment(`cache.hit.${layer}`),
  onMiss:       () => metrics.increment('cache.miss'),
});

const product = await cache.get('p-1', async () => db.products.findById('p-1'));
// Checks L1 → L2 → L3 → DB (writes to all layers on DB hit)
```

Show: the read-through logic (try L1, then L2, then L3, then source), write-through on miss (populate all layers on DB read), L1 eviction when at maxSize (LRU), and cache stampede protection (single-flight / promise coalescing).''',

'''**Task (Code Generation):**
Implement a `createEventDrivenWorkflow` for orchestrating complex business processes:

```ts
const orderWorkflow = createEventDrivenWorkflow('order-fulfillment', {
  events: {
    'order.created':     [reserveInventory, createShipmentLabel],
    'inventory.reserved':[chargeCustomer],
    'payment.succeeded': [dispatchShipment, sendConfirmation],
    'payment.failed':    [releaseInventory, notifyCustomer],
    'shipment.delivered':[updateOrderStatus, requestReview],
  },
  compensations: {
    'reserveInventory': releaseInventory,
    'chargeCustomer':   refundCustomer,
  },
  deadLetterQueue: dlqPublisher,
  traceId: (event) => event.correlationId,
});

// Subscribe the workflow to events:
eventBus.subscribe(orderWorkflow.handler);
```

Show: the event-handler mapping, each handler producing new events (chaining), compensation triggers on failure events, correlation IDs for tracing across handlers, dead letter queue for unhandled errors, and idempotency (event `id` dedup to avoid double processing).''',

'''**Task (Code Generation):**
Build a `createConsumerGroupManager` for Kafka consumer group coordination:

```ts
const consumerGroup = createConsumerGroupManager({
  brokers: ['kafka-1:9092', 'kafka-2:9092'],
  groupId: 'order-processor',
  topics: ['orders', 'inventory', 'payments'],
  fromBeginning: false,
  sessionTimeout: 30_000,
  heartbeatInterval: 3_000,
  handlers: {
    'orders':    orderHandler,
    'inventory': inventoryHandler,
    'payments':  paymentHandler,
  },
  concurrency: 5,       // 5 parallel message handlers per consumer instance
  autoCommit: false,     // Manual commit after successful processing
  onRebalance: () => flushLocalCaches(),
});

await consumerGroup.start();
```

Show: KafkaJS setup (`new Kafka({ brokers, clientId })`), `consumer.run({ eachMessage })` vs `eachBatch`, manual commit (`consumer.commitOffsets()`), graceful shutdown (drain in-flight messages, then `consumer.disconnect()`), and rebalance handling ("stop the world" vs cooperative/incremental rebalancing).''',

'''**Task (Code Generation):**
Implement a `createApiGateway` with routing, auth, and rate limiting:

```ts
const gateway = createApiGateway({
  routes: [
    { path: '/api/products',   upstream: 'product-service:3001',  auth: 'optional' },
    { path: '/api/orders',     upstream: 'order-service:3002',     auth: 'required' },
    { path: '/api/payments',   upstream: 'payment-service:3003',   auth: 'required', rateLimit: 'strict' },
    { path: '/api/admin',      upstream: 'admin-service:3004',     auth: 'admin-only' },
  ],
  auth: {
    verify: (token) => verifyJWT(token, process.env.JWT_SECRET),
    extractUser: (payload) => ({ id: payload.sub, roles: payload.roles }),
  },
  rateLimits: {
    default: { requests: 100, window: 60_000 },
    strict:  { requests: 10,  window: 60_000 },
  },
  upstream: { timeout: 10_000, retries: 2, healthCheck: '/health' },
});
```

Show: the reverse proxy using `http-proxy-middleware`, JWT verification in middleware, rate limiting with Redis sliding window, upstream health checks, and request/response transformation (stripping internal headers, adding correlation IDs).''',

'''**Task (Code Generation):**
Build a `createProcessManager` for coordinating multiple microservice processes:

```ts
const processManager = createProcessManager({
  services: {
    'api-server':  { command: 'node dist/api.js',     port: 3000, healthPath: '/health' },
    'worker':      { command: 'node dist/worker.js',  replicas: 4 },
    'scheduler':   { command: 'node dist/scheduler.js', singleton: true },
    'metrics':     { command: 'node dist/metrics.js', port: 9464 },
  },
  startup: {
    order: ['metrics', 'api-server', 'scheduler', 'worker'],
    waitForHealth: true,
    timeout: 30_000,
  },
  shutdown: {
    order: ['worker', 'scheduler', 'api-server', 'metrics'],
    gracefulTimeout: 10_000,
  },
  restartPolicy: { maxRestarts: 5, window: 60_000 },
});
```

Show: `child_process.spawn` for each service, `SIGTERM` propagation on shutdown, health check polling during startup, crash detection with restart backoff, and `pm2` as a production alternative.''',

# ── Debugging ─────────────────────────────────────────────────────────────────

'''**Debug Scenario:**
A microservice architecture shows "split brain" — two service instances both believe they are the "leader" and process the same job simultaneously:

```ts
// Leader election using Redis SETNX:
async function electLeader(instanceId: string) {
  const acquired = await redis.set('leader', instanceId, 'NX', 'EX', 30);
  return !!acquired;
}
// Instance A: acquires lock with 30s TTL
// Instance B: cannot acquire — waits
// Instance A crashes after 25s → lock expires
// Both A (recovered) and B try to acquire simultaneously!
```

SETNX with TTL has a race condition at the TTL boundary. Show: using Redlock (multi-node Redis distributed lock for true mutual exclusion), renewal before expiry (`setInterval(renewLock, 15_000)` when TTL is 30s), and checking that the lock token matches before renewal (prevents renewing someone else's lock).''',

'''**Debug Scenario:**
A CQRS system's read model is inconsistently updated — some records show old data even after the write side confirms:

```ts
// Write side: updates DB, emits event
await commandBus.dispatch({ type: 'UpdatePrice', productId: 'p1', price: 99 });
// Event emitted: 'PriceUpdated' → read model projection should update

// Read side query (too fast):
const product = await queryBus.query({ type: 'GetProduct', id: 'p1' });
// product.price: still shows old price!
```

Events are processed asynchronously — the read model hasn't caught up. Show: eventual consistency acceptance (this is correct behavior for CQRS), client-side optimistic update while the projection catches up, a `version` field on the read model for staleness detection, and using Kafka consumer lag metrics to monitor projection delay.''',

'''**Debug Scenario:**
An API Gateway times out when one upstream microservice is slow, causing a cascade failure for unrelated routes:

```ts
// All routes share one connection pool to all upstream services:
const proxy = httpProxy.createServer({ target: upstreamUrl });
// When payment-service is slow (holds pool connections):
// /api/products also times out — unrelated but shares the pool!
```

Connection pool exhaustion from one slow service blocks all routes. Show: separate connection pools per upstream service (isolate the blast radius), request hedging (duplicate the request to a different instance after a threshold), implementing timeout per route (`{ '/api/payments': 5000, '/api/products': 2000 }`), and connection pool `max` and `acquireTimeout` settings.''',

'''**Debug Scenario:**
A developer's Kubernetes readiness probe causes all pods to restart simultaneously during a deployment:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3
```

During deployment, new pods start too quickly, their health check fails 3 times (app not fully started), Kubernetes kills and restarts them — cascading restarts because `initialDelaySeconds: 5` is too short for a 15-second Node.js startup. Show: increasing `initialDelaySeconds` to 20-30s, using `startupProbe` (separate from liveness, allows longer startup grace period), a `readinessProbe` (separate from liveness — pod is removed from Service load balancer, not restarted), and the difference between `livenessProbe` (restart?) and `readinessProbe` (receive traffic?).''',

'''**Debug Scenario:**
A message queue consumer acknowledges messages before processing completes, causing data loss on crashes:

```ts
consumer.on('message', async (msg) => {
  channel.ack(msg); // Acknowledge FIRST — BUG!
  await processPayment(msg.content); // If this throws, message is already acked
});
```

If `processPayment` throws after `ack`, the message is gone forever — no replay possible. Show: acknowledging AFTER successful processing (`await processPayment(msg.content); channel.ack(msg)`), using `nack(msg, false, true)` to requeue on failure, idempotency keys to safely retry requeued messages, and dead letter queues for messages that fail repeatedly.''',

'''**Debug Scenario:**
A developer's gRPC streaming call creates a memory leak because the stream is never closed:

```ts
const stream = grpcClient.StreamData({ startTime: Date.now() });

stream.on('data', (chunk) => {
  processChunk(chunk);
});
// Component unmounts / function exits → stream.cancel() never called!
```

gRPC streaming connections stay open until explicitly closed. Show: calling `stream.cancel()` in cleanup (`return () => stream.cancel()` in `useEffect`), the `stream.on('end', ...)` cleanup handler, setting a timeout (`setTimeout(() => stream.cancel(), MAX_DURATION)`), and the gRPC call deadline option (`const deadline = new Date(Date.now() + 30_000); client.method({}, { deadline })`).''',

'''**Debug Scenario:**
A Redis pub/sub system loses messages when a subscriber is briefly disconnected and reconnects:

```ts
// Subscriber:
const sub = redis.duplicate();
sub.subscribe('events', (message) => processEvent(message));
// If sub disconnects for 5 seconds → all messages published during that time are LOST
```

Redis Pub/Sub is fire-and-forget — no persistence, no message acknowledgment. Disconnected subscribers miss all messages. Show: using Redis Streams instead of Pub/Sub (`XADD`/`XREAD` with consumer groups), consumer groups providing at-least-once delivery with `XACK`, `XREADGROUP` delivering from a pending list for unacknowledged messages, and persistent offset tracking so reconnected consumers only read new messages.''',

'''**Debug Scenario:**
A developer's API endpoint is vulnerable to SSRF (Server-Side Request Forgery) via an unvalidated URL parameter:

```ts
app.get('/proxy', async (req, res) => {
  const { url } = req.query;
  const response = await fetch(url); // Attacker can pass: http://169.254.169.254/latest/meta-data/
  res.json(await response.json());   // Returns AWS EC2 instance metadata!
});
```

Show: an allowlist of safe destinations (`if (!ALLOWED_DOMAINS.includes(new URL(url).hostname)) throw`), blocking private IP ranges (10.x, 192.168.x, 169.254.x — `ipaddr.js` library), blocking non-HTTP protocols (file://, gopher://), and using a dedicated outbound proxy that enforces network-level restrictions.''',

'''**Debug Scenario:**
A service's database migration fails in production because it holds a table lock, blocking all queries for 30 minutes:

```sql
-- Migration file:
ALTER TABLE products ADD COLUMN description TEXT;
-- In PostgreSQL, ADD COLUMN with no default acquires AccessExclusiveLock — blocks ALL reads and writes!
```

PostgreSQL `ALTER TABLE` acquires the strongest lock, blocking all concurrent operations. Show: using `ADD COLUMN description TEXT DEFAULT NULL` in modern PostgreSQL (no rewrite needed for nullable columns without default), `CREATE INDEX CONCURRENTLY` instead of regular `CREATE INDEX`, zero-downtime migration pattern (add nullable column → deploy → backfill → add constraint), and `lock_timeout: '2s'` to fail fast instead of hanging.''',

'''**Debug Scenario:**
A developer's service mesh times out on inter-service calls despite the target service responding in 50ms:

```
Service A → (via Envoy sidecar) → Service B
Service A configured: timeout = 1s
Service B responds: 50ms
But Service A gets timeout errors!
```

The Envoy sidecar's own timeout (default: 15s) isn't the issue — check if retries are configured. Envoy retries on 503, each with its own timeout. With 3 retries × 50ms response time + retry timing overhead, the total can exceed Service A's 1s timeout. Show: disabling retries for non-idempotent endpoints (`x-envoy-retry-on: retriable-status-codes`), aligning timeout hierarchies (`serviceA.timeout > retries × serviceB.timeout + jitter`), and Istio's `VirtualService` timeout and retry configuration.''',

'''**Debug Scenario:**
A developer's container is labeled as "running" by Kubernetes but the application is actually deadlocked:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  # /health returns 200 even when the app is deadlocked!
```

The `/health` endpoint always returns 200 (it's a static handler that never touches the deadlocked service layer). Show: adding meaningful health checks that probe actual functionality (`await db.raw('SELECT 1')`, `await redis.ping()`), using deep vs shallow health checks (k8s liveness = shallow: "am I running?", readiness = deep: "can I serve traffic?"), and a `readinessProbe` that checks queue depth, active requests, and connection pool availability.''',

'''**Debug Scenario:**
An API's `Content-Security-Policy` header is configured incorrectly, and `'unsafe-inline'` negates all script-src restrictions:

```ts
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.example.com; style-src 'self' 'unsafe-inline'");
  next();
});
```

`'unsafe-inline'` allows all inline scripts — equivalent to having no CSP for XSS protection. Show: replacing `'unsafe-inline'` with a nonce (`script-src 'self' 'nonce-${randomNonce}'`), adding the `nonce` attribute to legitimate `<script>` tags, the `strict-dynamic` keyword for loading scripts dynamically, and using `Content-Security-Policy-Report-Only` with a `report-uri` to incrementally tighten policy without breaking the site.''',

'''**Debug Scenario:**
A developer's Node.js cluster with 4 workers shows one worker handling 90% of all requests:

```ts
const cluster = require('cluster');
if (cluster.isPrimary) {
  for (let i = 0; i < 4; i++) cluster.fork();
} else {
  app.listen(3000); // All workers listen on port 3000
}
```

Node.js cluster's default scheduling on Linux is `SCHED_RR` (round-robin) but on some systems defaults to `OS` scheduling which routes all connections to the same worker (connection inheritance from the primary). Show: setting `cluster.schedulingPolicy = cluster.SCHED_RR`, using nginx or HAProxy as the actual load balancer (instead of Node.js cluster), and PM2's cluster mode which handles this correctly.''',

'''**Debug Scenario:**
A developer's S3 presigned URL expires too quickly under high load because clock skew between the signing server and S3 differs:

```ts
const signedUrl = s3.getSignedUrl('getObject', {
  Bucket: 'my-bucket',
  Key: 'file.pdf',
  Expires: 300,  // 5 minutes
});
// Users get "Request has expired" errors after 3 minutes!
```

S3 validates the signature expiry based on the request arrival time. If the signing server's clock is ahead of S3's expected time by 2 minutes, the URL effectively expires in 3 minutes instead of 5. Show: using `aws-sdk` with `credentials.getPromise()` + `Date.now()` logging to detect clock drift, NTP sync for the signing server, increasing the `Expires` value to compensate, and `x-amz-date` header validation (must within 15-minute window).''',

]

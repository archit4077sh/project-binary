"""
snippets/q_testing.py — BATCH 7: 55 brand-new Testing questions
Zero overlap with batches 1-6 archives.
"""

Q_TESTING = [

'''**Task (Code Generation):**
Implement a `createTestDatabase` factory for Vitest integration tests using Prisma and PostgreSQL:

```ts
async function createTestDatabase() {
  const schemaName = `test_${randomBytes(8).toString('hex')}`;

  await prisma.$executeRawUnsafe(`CREATE SCHEMA "${schemaName}"`);

  const testPrisma = new PrismaClient({
    datasources: { db: { url: `${process.env.DATABASE_URL}?schema=${schemaName}` } },
  });

  await testPrisma.$executeRaw`SET search_path TO ${Prisma.raw(schemaName)}`;
  await migrate(testPrisma);

  return {
    prisma: testPrisma,
    cleanup: async () => {
      await testPrisma.$disconnect();
      await prisma.$executeRawUnsafe(`DROP SCHEMA "${schemaName}" CASCADE`);
    },
  };
}

// Usage:
let db: PrismaClient;
beforeAll(async () => { ({ prisma: db, cleanup } = await createTestDatabase()); });
afterAll(async () => cleanup());
```

Show: the unique schema per test file (true isolation — schemas don't interfere), PostgreSQL's `DROP SCHEMA CASCADE` for cleanup, running migrations inside the test schema, and the `vitest --pool=forks` option for true process isolation between test files.''',

'''**Task (Code Generation):**
Build a `createApiTestHarness` for testing Express/Fastify routes with real middleware:

```ts
const harness = createApiTestHarness({
  app: expressApp,
  globalMocks: {
    authentication: (req) => { req.user = { id: 'test-user', role: 'user' }; },
    rateLimit: 'bypass',
  },
  plugins: [
    { name: 'database', inject: (app) => app.set('db', testDb) },
    { name: 'logger', inject: (app) => app.set('logger', silentLogger) },
  ],
});

const { request, as } = harness;

// Regular request:
const res = await request.get('/api/products').expect(200);

// Request as admin:
const adminRes = await as({ role: 'admin' }).get('/api/admin/users').expect(200);

// Request without auth:
const unauthedRes = await as(null).get('/api/protected').expect(401);
```

Show: `supertest`'s `request(app)` for HTTP testing without a live server, the `as()` helper swapping the authentication middleware, bypassing rate limiting for tests, and `nock` for mocking outbound HTTP calls from the app.''',

'''**Task (Code Generation):**
Implement a `createCypressCustomCommands` file for reusable E2E testing helpers:

```ts
// cypress/support/commands.ts:
Cypress.Commands.add('loginAs', (role: UserRole) => {
  cy.request('POST', '/api/test/auth', { role }).its('body.token').then(token => {
    window.localStorage.setItem('auth-token', token);
  });
  cy.visit('/dashboard');
});

Cypress.Commands.add('seedDatabase', (fixture: string) => {
  cy.fixture(fixture).then(data => {
    cy.request('POST', '/api/test/seed', data);
  });
});

Cypress.Commands.add('getByTestId', (testId: string) => {
  cy.get(`[data-testid="${testId}"]`);
});

// With TypeScript declarations:
declare global {
  namespace Cypress {
    interface Chainable {
      loginAs(role: UserRole): Chainable<void>;
      seedDatabase(fixture: string): Chainable<void>;
      getByTestId(testId: string): Chainable<JQuery<HTMLElement>>;
    }
  }
}
```

Show: the `cypress/support/commands.ts` + `cypress/support/e2e.ts` pattern, a `/api/test/*` controller for test helpers (only active in test mode), the `data-testid` attribute convention for stable selectors, and `cy.intercept()` for mocking specific API calls.''',

'''**Task (Code Generation):**
Build a `createFuzzTest` framework for testing with random valid inputs:

```ts
describe('OrderProcessor fuzz tests', () => {
  const arbitrary = {
    orderId:  fc.uuid(),
    quantity: fc.integer({ min: 1, max: 10000 }),
    price:    fc.float({ min: 0.01, max: 99999.99, noNaN: true }),
    currency: fc.constantFrom('USD', 'EUR', 'GBP', 'JPY'),
    discount: fc.float({ min: 0, max: 1, noNaN: true }),
  };

  fc.assert(
    fc.asyncProperty(
      fc.record(arbitrary),
      async (order) => {
        const result = await processOrder(order);
        // Invariants that MUST hold regardless of input:
        expect(result.total).toBeGreaterThanOrEqual(0);
        expect(result.total).toBeLessThanOrEqual(order.price * order.quantity);
        expect(result.currency).toBe(order.currency);
        expect(result.orderId).toBe(order.orderId);
      }
    ),
    { numRuns: 1000 }
  );
});
```

Show: `fast-check`'s `fc.record`, `fc.uuid`, `fc.float` with `noNaN`, `fc.asyncProperty` for async tests, the invariant-based testing mindset (what must ALWAYS be true?), and `fc.statistics` to analyze the distribution of generated inputs.''',

'''**Task (Code Generation):**
Implement a `createBehaviorTest` using Gherkin/BDD style with Vitest:

```ts
// Use tagged template literals for BDD-style test structure:
Feature('User Authentication', () => {
  Background(() => {
    Given('the application is loaded', () => render(<App />));
  });

  Scenario('Successful login', () => {
    Given('user enters valid credentials', async () => {
      await user.type(screen.getByLabelText('Email'), 'alice@example.com');
      await user.type(screen.getByLabelText('Password'), 'SecurePass123!');
    });
    When('user clicks Sign In', async () => {
      await user.click(screen.getByRole('button', { name: 'Sign In' }));
    });
    Then('user sees the dashboard', () => {
      expect(screen.getByRole('heading', { name: 'Dashboard' })).toBeInTheDocument();
    });
  });
});
```

Show: implementing the `Feature`, `Scenario`, `Given/When/Then` functions as wrappers around `describe`/`it`/`beforeEach`, the `@cucumber/cucumber` library for full Gherkin support, and `vitest-cucumber` for Vitest-native BDD.''',

'''**Task (Code Generation):**
Build a `createApiDocTest` for testing OpenAPI spec compliance:

```ts
// Verify that API responses match the OpenAPI schema:
const docTester = createApiDocTester({
  spec: './openapi.yaml',
  baseUrl: 'http://localhost:3000',
});

describe('GET /api/products', () => {
  it('response matches OpenAPI schema', async () => {
    const res = await request.get('/api/products');
    await docTester.assertResponse(res, {
      path: '/api/products',
      method: 'GET',
      status: 200,
    });
    // Validates: status code, headers, body shape against the spec
  });
});
```

Show: using `openapi-response-validator` or `express-openapi-validator`, loading and parsing the YAML/JSON spec with `js-yaml`, AJV for JSON schema validation, the `dredd` tool for API conformance testing, and `spectral` for linting the OpenAPI spec itself.''',

'''**Task (Code Generation):**
Implement a `createReactTestUtils` wrapper with enhanced queries:

```ts
const { renderWithProviders } = createReactTestUtils({
  providers: [
    (children) => <QueryClientProvider client={createTestQueryClient()}>{children}</QueryClientProvider>,
    (children) => <StoreProvider store={createTestStore()}>{children}</StoreProvider>,
    (children) => <ThemeProvider theme={testTheme}>{children}</ThemeProvider>,
  ],
  queries: {
    getByTestId:    (id)   => screen.getByTestId(id),
    findByTestId:   (id)   => screen.findByTestId(id),
    getFormField:   (label) => screen.getByRole('textbox', { name: label }),
    getSubmitButton:()     => screen.getByRole('button', { name: /submit/i }),
  },
});

const { getByTestId, getFormField, user, store, queryClient } = renderWithProviders(
  <CheckoutForm />,
  { initialStore: { cart: { items: mockItems } } }
);
```

Show: the provider composition pattern, `createTestQueryClient` disabling retries and stale time, custom query shortcuts, `userEvent.setup()` in the render result, exposing `store` and `queryClient` for post-action assertions, and `renderHook` integration.''',

'''**Task (Code Generation):**
Build a `createPerformanceTest` for tracking component render times in tests:

```ts
describe('ProductGrid performance', () => {
  it('renders 100 products within 100ms', () => {
    const start = performance.now();
    render(<ProductGrid products={generateProducts(100)} />);
    const renderTime = performance.now() - start;

    // Assert render time budget:
    expect(renderTime).toBeLessThan(100); // 100ms budget for initial render
  });

  it('re-renders efficiently on filter change', async () => {
    const { rerender } = render(<ProductGrid products={allProducts} filter="" />);
    const renders: number[] = [];

    const start = performance.now();
    rerender(<ProductGrid products={allProducts} filter="react" />);
    renders.push(performance.now() - start);

    expect(Math.max(...renders)).toBeLessThan(50); // <50ms for re-render
  });
});
```

Show: `performance.now()` for micro-benchmarks in tests, running 5 iterations and using the median (avoid outliers), React Profiler API integration for render counting (`<Profiler id="grid" onRender={...}>`), and separating timing tests from behavior tests (don't mix in CI).''',

'''**Task (Code Generation):**
Implement a `createTestRecorder` for automatically generating test cases from user sessions:

```ts
// In development, record user interactions:
const recorder = createTestRecorder({
  output: './tests/__generated__/',
  format: 'playwright',  // or 'cypress', 'testing-library'
  events: ['click', 'type', 'navigate', 'assertion'],
  assertions: {
    auto:     true, // Auto-generate assertions after each action
    selector: 'data-testid', // Prefer data-testid selectors
  },
});

// Records: click('[data-testid="add-to-cart"]') → assert('[data-testid="cart-count"]', '1')

// Generated test:
test('user adds item to cart', async ({ page }) => {
  await page.click('[data-testid="add-to-cart"]');
  await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');
});
```

Show: listening to DOM events (`addEventListener` on `document`), mapping event properties to Playwright/Cypress commands, using `MutationObserver` for detecting DOM changes to auto-assert, and the Playwright Code Generator (`playwright codegen`) as a production-ready alternative.''',

'''**Task (Code Generation):**
Build a `createContractVerifier` for backend provider tests using Pact:

```ts
// Provider test (verifies the frontend's expectations):
describe('Product API Provider Tests', () => {
  const provider = new PactV3({
    consumer: 'ShopFrontend',
    provider: 'ProductAPI',
    pactBrokerUrl: process.env.PACT_BROKER_URL,
    pactBrokerToken: process.env.PACT_BROKER_TOKEN,
  });

  it('verifies contracts from the broker', async () => {
    await provider
      .addStateHandler('product p-1 exists', async () => {
        await db.product.upsert({ where: { id: 'p-1' }, create: testProduct, update: testProduct });
      })
      .addStateHandler('product p-1 does not exist', async () => {
        await db.product.deleteMany({ where: { id: 'p-1' } });
      })
      .verifyProvider({
        providerBaseUrl: 'http://localhost:3001',
        stateHandlers: true,
      });
  });
});
```

Show: the Pact provider state handlers for setting up DB state, `publishVerificationResults: true` for CI PR status, the `can-i-deploy` check before production deployment, and running the provider tests in CI after every backend change.''',

'''**Task (Code Generation):**
Implement a `createVisualComponentTest` with Chromatic integration:

```ts
// Storybook-based visual test + Chromatic CI:
// Button.stories.tsx:
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
      {(['primary', 'secondary', 'danger', 'ghost'] as const).map(variant =>
        (['sm', 'md', 'lg'] as const).map(size =>
          <Button key={`${variant}-${size}`} variant={variant} size={size}>Button</Button>
        )
      )}
    </div>
  ),
  parameters: {
    chromatic: { viewports: [375, 768, 1440], delay: 300 },
  },
};
```

```bash
# CI: npx chromatic --project-token $CHROMATIC_TOKEN --exit-zero-on-changes
```

Show: the `parameters.chromatic` storybook config for Chromatic-specific options, `viewports` for responsive visual tests, `delay` for waiting for animations to complete, `diffThreshold` for pixel-diff tolerance, and the Chromatic Turbosnap feature (only test changed components on PR).''',

'''**Task (Code Generation):**
Build a `createStateTransitionTest` for exhaustively testing reducer logic:

```ts
const testTransitions = createStateTransitionTest(authReducer, {
  states: ['idle', 'loading', 'authenticated', 'error'],
  events: [
    { type: 'LOGIN_START',   payload: { email: 'a@b.com' } },
    { type: 'LOGIN_SUCCESS', payload: { user: mockUser } },
    { type: 'LOGIN_ERROR',   payload: { message: 'Invalid credentials' } },
    { type: 'LOGOUT' },
  ],
});

// Auto-tests all valid transitions:
testTransitions.verifyTransitions([
  { from: 'idle',    event: 'LOGIN_START',   to: 'loading' },
  { from: 'loading', event: 'LOGIN_SUCCESS', to: 'authenticated' },
  { from: 'loading', event: 'LOGIN_ERROR',   to: 'error' },
  { from: 'authenticated', event: 'LOGOUT', to: 'idle' },
]);

// Verify invalid transitions are no-ops:
testTransitions.verifyNoOp('idle', 'LOGIN_SUCCESS'); // Should not change state
```

Show: the `verifyTransitions` function applying each event and asserting the resulting state shape, `verifyNoOp` calling the reducer with an event from an invalid state and asserting the state doesn't change, and the XState `createModel` testing utilities for state machine-based tests.''',

'''**Task (Code Generation):**
Implement a `createServerComponentTest` for testing Next.js RSCs:

```ts
// Testing React Server Components directly:
import { render } from '@testing-library/react';
import { cache } from 'react';

// Mock the RSC data dependencies:
vi.mock('./lib/data', () => ({
  getProduct: vi.fn().mockResolvedValue(mockProduct),
  getRelatedProducts: vi.fn().mockResolvedValue(mockRelated),
}));

it('renders product details with related products', async () => {
  const component = await ProductPage({ params: { slug: 'test-product' } });
  const { getByRole } = render(component);

  expect(getByRole('heading', { name: mockProduct.name })).toBeInTheDocument();
  expect(getByRole('list', { name: 'Related products' })).toBeInTheDocument();
});
```

Show: calling RSC functions directly (they're just async functions), mocking data fetching dependencies with `vi.mock`, the `experimental_taintObjectReference` API for security testing, known limitations (server-only APIs like `cookies()` and `headers()` require additional mocking), and the Next.js official `jest-environment-jsdom` integration.''',

'''**Task (Code Generation):**
Build a `createParallelTestSuite` for running integration tests with maximum parallelism:

```ts
// vitest.config.ts:
export default defineConfig({
  test: {
    pool: 'forks',              // Each file in its own process (true parallelism)
    poolOptions: {
      forks: {
        singleFork: false,
        maxForks: os.cpus().length,
        minForks: 2,
      },
    },
    sequence: {
      concurrent: true,         // Tests within a file can run concurrently
    },
    globalSetup: './test/global-setup.ts', // Run ONCE before all test files
    setupFiles: ['./test/setup.ts'],       // Run per-file
    fileParallelism: true,
  },
});

// global-setup.ts — runs once, shared across all test processes:
export default async function globalSetup() {
  await startTestServer();
  await seedGlobalTestData();
  return async () => { await teardownTestServer(); };
}
```

Show: Vitest `forks` vs `threads` pool (forks = more isolated, slower start; threads = faster, shared memory), `globalSetup` vs `setupFiles` (global runs once; setup runs per file), and `isolate: false` for sharing module state within a worker.''',

'''**Tasks (Code Generation):**
Implement a `createMockWebSocket` server for testing WebSocket-based features:

```ts
const mockWs = createMockWebSocketServer({ port: 8765 });

beforeAll(() => mockWs.listen());
afterAll(() => mockWs.close());
afterEach(() => mockWs.resetHandlers());

mockWs.on('connect', (socket) => {
  socket.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.type === 'AUTH') socket.send(JSON.stringify({ type: 'AUTH_OK', token: 'mock-token' }));
    if (msg.type === 'SUBSCRIBE') socket.send(JSON.stringify({ type: 'DATA', payload: mockData }));
  });
});

// In test:
render(<LiveDataComponent wsUrl="ws://localhost:8765" />);
await screen.findByText('Connected');
await waitFor(() => expect(screen.getByTestId('data-table')).toBeInTheDocument());
```

Show: the `ws` library for the mock server, `socket.send` for responses, connection lifecycle events, simulating disconnection/reconnection scenarios (`mockWs.simulateDisconnect()`), and the `mock-socket` library for browser-based WebSocket mocking without a real server.''',

'''**Task (Code Generation):**
Build a `createGraphQLTestServer` for testing GraphQL resolvers without HTTP:

```ts
const testServer = createGraphQLTestServer({
  schema,
  context: () => ({
    db: testDb,
    user: { id: 'test-user', role: 'user' },
    loaders: createTestLoaders(testDb),
  }),
});

it('fetches product with reviews', async () => {
  const res = await testServer.execute(`
    query GetProduct($id: ID!) {
      product(id: $id) {
        id
        name
        price
        reviews { rating body author }
      }
    }
  `, { id: 'p-1' });

  expect(res.errors).toBeUndefined();
  expect(res.data.product.name).toBe('Test Product');
  expect(res.data.product.reviews).toHaveLength(3);
});
```

Show: Apollo Server's `executeOperation` for in-process testing (no HTTP round-trip), providing test context with mock DB and users, testing subscription resolvers, `toMatchSnapshot()` for full response shape testing, and the `@apollo/server` testing utilities.''',

'''**Debug Scenario:**
A developer's `waitFor` callback throws "Expected condition not met" even though the UI has updated:

```ts
it('shows loading then data', async () => {
  render(<DataComponent />);
  expect(screen.getByText('Loading...')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    expect(screen.getByText('Data Loaded!')).toBeInTheDocument(); // Sometimes fails!
  });
});
```

`waitFor` retries until the callback passes or times out. If the `queryByText('Loading...')` passes but `getByText('Data Loaded!')` throws before the next retry clears it — the callback passes in one retry but the data hasn't appeared yet. Show: splitting into two `waitFor` calls (wait for loading to disappear, then wait for data to appear), using `findByText('Data Loaded!')` (single async query that auto-retries), and setting `waitFor` timeout via `{ timeout: 3000 }`.''',

'''**Debug Scenario:**
A Cypress test is flaky because it asserts on an element's `value` before the debounced update fires:

```ts
cy.get('[data-testid="search-input"]').type('react');
cy.get('[data-testid="results-count"]').should('have.text', '42 results'); // Flaky!
// The search has a 300ms debounce — results haven't updated yet
```

The `type` command is synchronous from Cypress's perspective but the debounce fires after 300ms. Show: adding `cy.wait(400)` for the debounce delay (fragile but explicit), using `cy.clock()` and `cy.tick(300)` to control time precisely (`cy.tick` advances fake timers), `cy.intercept` to wait for the API call triggered by the debounce, and `should('eventually.have.text', '42 results')` with a longer timeout.''',

'''**Debug Scenario:**
A developer's Vitest test file importing CSS modules fails because CSS is not handled:

```ts
// Component test:
import { render } from '@testing-library/react';
import Button from './Button';  // Button imports './Button.module.css'
// Error: Unknown file extension ".css"
```

Vitest (running in Node.js) doesn't understand CSS modules by default. Show: adding the `identity-obj-proxy` package which returns the class name as-is for CSS modules, configuring in `vitest.config.ts`:

```ts
moduleNameMapper: { '\\.module\\.css$': 'identity-obj-proxy' }
```

Or using `@vitest/browser` for browser-native testing (handles CSS correctly), and why mocking CSS is the correct approach for unit tests (testing behavior, not styles).''',

'''**Debug Scenario:**
A developer's test spy on a method doesn't intercept the call because the method is called directly on the instance:

```ts
const service = new UserService();
const findSpy = vi.spyOn(service, 'findUser');

// Calling through the instance — spy works:
service.findUser('u1'); // Spy intercepts ✓

// Called internally — spy doesn't intercept:
service.createUser({ id: 'u1' }); // Internally calls: this.findUser() — NOT intercepted!
```

`vi.spyOn(service, 'findUser')` replaces `service.findUser` (the property on the instance) but the method body calls `this.findUser` — which goes through the prototype chain, not the spied property. Show: spying on the prototype (`vi.spyOn(UserService.prototype, 'findUser')`), the design implication (methods calling `this.method` make mocking harder — prefer dependency injection), and using DI to replace the whole dependency.''',

'''**Debug Scenario:**
A developer's `screen.getByRole` throws "Unable to find role" for a custom ARIA role:

```tsx
render(<div role="status" aria-live="polite">Loading...</div>);
screen.getByRole('status'); // Throws: Unable to find accessible element with role "status"
```

ARIA role `status` is an abstract role — some Testing Library versions or ARIA spec interpretations don't support it as a queryable role. Show: using `screen.getByText('Loading...')`, `screen.getByRole('region')` (with `aria-label`), checking the `roles` list from `@testing-library/aria-query`, using `aria-live="polite"` + `getByLiveRegion` from `@testing-library/user-event` extensions, and `getByTestId` as an escape hatch for non-standard roles.''',

'''**Debug Scenario:**
A developer's custom Jest matcher doesn't format the failure message correctly:

```ts
expect.extend({
  toBeValidEmail(received: string) {
    const pass = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(received);
    return {
      pass,
      message: () => pass
        ? `expected ${received} not to be a valid email`
        : `expected ${received} to be a valid email`,
      // Missing: this.utils for pretty-printing
    };
  },
});
```

The failure message is functional but doesn't use Jest's pretty-printer for consistent formatting. Show: using `this.utils.printReceived(received)` and `this.utils.printExpected('valid email')` for colorized output, `this.isNot` to handle the negated case (`not.toBeValidEmail`), `this.utils.matcherHint('toBeValidEmail')` for the header line, and the full `expect.extend` TypeScript declaration.''',

'''**Debug Scenario:**
A developer's MSW handler doesn't intercept requests from a `useEffect` in tests because the server isn't started before render:

```ts
// BUG — server starts AFTER render:
render(<DataComponent />);  // useEffect fires → fetch starts → no handler yet!
server.listen();             // Server starts too late

// Correct:
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it('fetches and displays data', async () => {
  render(<DataComponent />);
  await screen.findByText('Loaded data');
});
```

Show: the correct `beforeAll/afterAll/afterEach` MSW setup pattern, `server.resetHandlers()` after each test (prevents per-test handler overrides from leaking), `server.use(http.get('/api', () => HttpResponse.error()))` for per-test error scenarios (reset after the test), and `{ onUnhandledRequest: 'error' }` in `server.listen()` to catch unmocked requests.''',

'''**Debug Scenario:**
A developer's Playwright test fails in CI because the browser isn't installed:

```
Error: browserType.launch: Executable doesn't exist at /root/.cache/ms-playwright/chromium-1091/...
```

Playwright browsers must be explicitly installed — they're not included in `npm install`. Show: adding `npx playwright install chromium` (or `--with-deps` for system dependencies) to the CI steps:

```yaml
- name: Install Playwright Browsers
  run: npx playwright install --with-deps chromium
```

And `npx playwright install-deps` for Linux system dependencies (libglib, libX11, etc.), using the official `playwright/action-playwright` GitHub Action, and caching the Playwright browser binaries with `actions/cache`.''',

'''**Debug Scenario:**
A developer's `renderHook` test for a data-fetching hook doesn't wait for the async state update:

```ts
it('fetches user data', async () => {
  const { result } = renderHook(() => useUser('u1'));

  expect(result.current.user).toEqual(mockUser); // Fails! Still null
  // The hook fetches asynchronously — result hasn't loaded yet
});
```

`renderHook` renders the hook synchronously — async operations haven't completed. Show: using `await act(async () => { await result.current.refetch?.(); })`, using `waitFor` from `@testing-library/react`: `await waitFor(() => expect(result.current.user).toEqual(mockUser))`, and MSW for intercepting the fetch that occurs inside the hook.''',

'''**Debug Scenario:**
A developer's `toThrowError` assertion passes even though the error is thrown asynchronously:

```ts
it('throws on invalid input', () => {
  expect(async () => {
    await processPayment({ amount: -1 });
  }).toThrowError('Amount must be positive'); // Passes but shouldn't!
  // The async function returns a Promise — the throw is in the rejection
  // toThrowError checks if the function throws synchronously (not rejects)
});
```

`toThrowError` catches synchronous throws. An async function that rejects doesn't throw synchronously — it returns a rejected Promise. Show: the correct async error assertion: `await expect(processPayment({ amount: -1 })).rejects.toThrow('Amount must be positive')`, and the difference between `toThrow` (sync), `.rejects.toThrow` (async rejection), and wrapping in `async () => await fn()` vs calling directly.''',

'''**Debug Scenario:**
A developer's Vitest `vi.mock` of a local module doesn't affect the module's internal imports:

```ts
// api/users.ts imports from './db':
import { db } from './db';

// Test file:
vi.mock('./api/users', () => ({ getUser: vi.fn().mockResolvedValue(mockUser) }));
// This replaces the entire module — but the component uses './api/users', not './db'

// The REAL issue:
vi.mock('./db', () => ({ db: { findUser: vi.fn() } }));
// 'users.ts' still uses the REAL db — vi.mock at test level doesn't affect './db' inside users.ts
```

`vi.mock` hoists to the module system — imports inside a mocked module's dependencies are also mocked IF the mock is for the correct module ID. Show: the correct path resolution (test files have different cwd than the mocked module), using `vi.mock` with the factory `() => ({ ... })` for full replacement, and `vi.spyOn` for partial mocking.''',

'''**Debug Scenario:**
A developer's `beforeAll` setup runs in parallel with other test files' `beforeAll`, causing database conflicts:

```ts
// users.test.ts → beforeAll: seeds test users
// orders.test.ts → beforeAll: reads all users (gets users from users.test.ts's seed!)
// Tests interfere with each other because they share the same database
```

Vitest's `fileParallelism: true` runs test files concurrently — `beforeAll` in different files runs simultaneously. Show: using unique identifiers for each test file's seed data (suffix with file hash), using separate database schemas per file (`test_users_xyz`, `test_orders_abc`), `fileParallelism: false` for database-heavy tests (safer but slower), and `--sequence.shuffle` for detecting order-dependent tests.''',

'''**Debug Scenario:**
A developer's React Testing Library test asserts `toBeVisible` but the element is visually hidden with `visibility: hidden`:

```ts
render(<Tooltip content="Help text" hidden />);
// CSS applies: visibility: hidden to tooltip

expect(screen.getByRole('tooltip')).not.toBeVisible(); // Passes ✓
expect(screen.getByRole('tooltip')).not.toBeInTheDocument(); // Fails! Element IS in DOM
expect(screen.queryByRole('tooltip')).toBeNull(); // Fails! tooltip IS found
```

The element is in the DOM (just not visible). Show: `toBeVisible` checks CSS (visibility, display, opacity, hidden attribute) — `visibility: hidden` makes it not visible but it stays in the DOM, `toBeInTheDocument` checks DOM presence only, `queryByRole` still finds hidden elements (use `{ hidden: true }` to include ARIA `hidden` elements), and the difference between DOM presence and visual visibility in tests.''',

]

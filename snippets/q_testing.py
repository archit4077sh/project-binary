"""
snippets/q_testing.py — BATCH 6: 55 brand-new Testing questions
Zero overlap with batches 1-5 archives.
"""

Q_TESTING = [

"""**Task (Code Generation):**
Implement a `createTestServer` factory for integration testing API routes without mocking:

```ts
const server = await createTestServer({
  app: expressApp,
  db: await setupTestDatabase({
    migrate: true,
    seed: seedData,
    schema: 'test_schema',
  }),
  env: {
    NODE_ENV: 'test',
    JWT_SECRET: 'test-secret',
    STRIPE_SECRET: 'sk_test_xxx',
  },
});

// In tests:
const response = await server.request.post('/api/orders').send({ productId: 'p1' }).set('Authorization', `Bearer ${server.createToken({ userId: 'u1' })}`);
expect(response.status).toBe(201);

afterAll(() => server.teardown()); // drops test schema, closes connections
```

Show: spinning up an Express server on a random port, isolated PostgreSQL schema per test file (prevents test interference), the `createToken` JWT helper, and `supertest` for HTTP assertions.""",

"""**Task (Code Generation):**
Build a `createComponentHarness<Props>` for testing React components in an isolated environment:

```ts
const harness = createComponentHarness(ShoppingCart, {
  defaultProps: { items: [], currency: 'USD' },
  wrappers: [QueryClientWrapper, StoreWrapper, ThemeWrapper],
  mocks: {
    'api/cart': { GET: { items: mockItems, total: 45.99 } },
  },
});

const { getByText, user, queryClient } = harness.render({ items: [item1] });
await user.click(getByText('Remove'));

expect(getByText('Cart is empty')).toBeInTheDocument();
expect(queryClient.getQueryData(['cart'])).toBeNull();
```

Show: composing wrapper providers automatically, `@testing-library/user-event` for realistic user interactions, MSW mocks inline with the harness, and the `queryClient` exposed for asserting cache state after interactions.""",

"""**Task (Code Generation):**
Implement a `createE2EScenario` framework for Playwright test suites with reusable page objects:

```ts
const scenario = createE2EScenario({
  pages: {
    login:    new LoginPage(page),
    dashboard: new DashboardPage(page),
    checkout: new CheckoutPage(page),
  },
  fixtures: {
    user:    { email: 'test@example.com', password: 'TestPass123!' },
    product: { id: 'prod-1', name: 'Test Widget', price: 19.99 },
  },
});

test('complete checkout flow', async () => {
  await scenario.pages.login.loginAs(scenario.fixtures.user);
  await scenario.pages.dashboard.addToCart(scenario.fixtures.product);
  await scenario.pages.checkout.completeCheckout({ cardNumber: '4242424242424242' });
  await expect(page).toHaveURL('/order-confirmation');
});
```

Show: the Page Object Model pattern, Playwright's `test.extend` for fixture injection, `page.waitForResponse` for network assertions, and the `@playwright/test` tags for test categorization (`@smoke`, `@regression`).""",

"""**Task (Code Generation):**
Build a `createMSWHandlers` factory for typed API mocking in tests:

```ts
const handlers = createMSWHandlers<AppAPI>({
  '/api/users': {
    GET: (req) => HttpResponse.json(mockUsers, { status: 200 }),
    POST: async (req) => {
      const body = await req.json();
      const user = UserSchema.parse(body);
      return HttpResponse.json({ ...user, id: 'new-user-1' }, { status: 201 });
    },
  },
  '/api/users/:id': {
    GET: (req, { params }) => HttpResponse.json(mockUsers.find(u => u.id === params.id)),
    DELETE: (_, { params }) => {
      mockUsers = mockUsers.filter(u => u.id !== params.id);
      return new HttpResponse(null, { status: 204 });
    },
  },
});

const server = setupServer(...handlers);
```

Show: the MSW v2 `http.get/post/put/delete` handler factory, `HttpResponse` for response construction, `server.use(http.get('/api/override', ...))` for per-test overrides, and TypeScript ensuring handler return types match the `AppAPI` schema.""",

"""**Task (Code Generation):**
Implement a `createSnapshot` testing approach for complex component trees with inline snapshots:

```ts
describe('ProductCard', () => {
  it('renders correctly for a discounted product', async () => {
    const { container } = render(
      <ProductCard
        product={{ id: 'p1', name: 'Widget', price: 19.99, discountedPrice: 14.99 }}
        onAddToCart={vi.fn()}
      />
    );

    // Inline snapshot — shows in the test file:
    expect(container.firstChild).toMatchInlineSnapshot(`
      <div class="product-card">
        <img alt="Widget" src="/images/p1.jpg" />
        <h3>Widget</h3>
        <span class="original-price">$19.99</span>
        <span class="discounted-price">$14.99</span>
        <button>Add to Cart</button>
      </div>
    `);
  });
});
```

Show: `toMatchInlineSnapshot` for self-updating snapshots (run vitest -u), `toMatchSnapshot` for external files, custom snapshot serializers for complex objects, and when to use snapshots vs explicit assertions (snapshots for structure, assertions for behavior).""",

"""**Task (Code Generation):**
Build a `createPropertyTest` framework for property-based testing with `fast-check`:

```ts
describe('formatCurrency', () => {
  it('always produces a string starting with $', () => {
    fc.assert(
      fc.property(
        fc.float({ min: 0, max: 1_000_000 }),
        fc.constantFrom('USD', 'EUR', 'GBP'),
        (amount, currency) => {
          const result = formatCurrency(amount, currency);
          expect(typeof result).toBe('string');
          expect(result.length).toBeGreaterThan(0);
          // Idempotent: formatting already-formatted string fails gracefully
          expect(() => formatCurrency(parseFloat(result), currency)).not.toThrow();
        }
      )
    );
  });
});
```

Show: `fc.property` for arbitrary input generation, `fc.float`, `fc.string`, `fc.integer`, `fc.record`, shrinking (fast-check finds minimal failing examples), and `fc.sample` to inspect generated values.""",

"""**Task (Code Generation):**
Implement a `createTimeTravelTest` pattern for testing time-dependent code:

```ts
describe('SessionTimeout', () => {
  it('expires session after 30 minutes of inactivity', async () => {
    vi.useFakeTimers();

    const session = createSession({ userId: 'u1', timeout: 30 * 60 * 1000 });
    expect(session.isValid()).toBe(true);

    vi.advanceTimersByTime(29 * 60 * 1000); // 29 minutes
    expect(session.isValid()).toBe(true);

    vi.advanceTimersByTime(60 * 1000); // 1 more minute = 30 total
    expect(session.isValid()).toBe(false);
    expect(session.expiredAt).toBe(new Date('2024-01-15T10:30:00Z').getTime());
  });

  afterEach(() => vi.useRealTimers());
});
```

Show: `vi.useFakeTimers()` / `jest.useFakeTimers()`, `vi.setSystemTime(new Date('2024-01-15T10:00:00Z'))` for a fixed start time, `vi.advanceTimersByTime()`, `vi.runAllTimers()`, and the `@sinonjs/fake-timers` library for lower-level control.""",

"""**Task (Code Generation):**
Build a `createAccessibilityTest` suite using `axe-core` and Testing Library:

```ts
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

describe('LoginForm accessibility', () => {
  it('has no accessibility violations in default state', async () => {
    const { container } = render(<LoginForm />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('announces validation errors to screen readers', async () => {
    const { getByRole, user } = renderWithUser(<LoginForm />);
    await user.click(getByRole('button', { name: 'Sign In' }));
    expect(getByRole('alert')).toHaveTextContent('Email is required');
  });
});
```

Show: `jest-axe` integration, `@testing-library/jest-dom` matchers (`toBeInTheDocument`, `toHaveRole`, `toBeVisible`), testing `aria-live` announcements, keyboard navigation testing (`user.keyboard('{Tab}')`), and the `toHaveAccessibleName` matcher.""",

"""**Task (Code Generation):**
Implement a `createContractTest` for API contract testing between frontend and backend:

```ts
// frontend/tests/contracts/product.contract.test.ts
const productProvider = new Pact({
  consumer: 'ShopFrontend',
  provider: 'ProductAPI',
});

describe('Product API contract', () => {
  it('fetches product by ID', async () => {
    await productProvider
      .addInteraction({
        state: 'product p-1 exists',
        uponReceiving: 'a request for product p-1',
        withRequest: { method: 'GET', path: '/api/products/p-1' },
        willRespondWith: {
          status: 200,
          body: like({ id: 'p-1', name: string(), price: number(), inStock: boolean() }),
        },
      });

    const product = await fetchProduct('p-1');
    expect(product.inStock).toBeDefined();
  });
});
```

Show: the Pact consumer-driven contract testing approach, `like()` and `eachLike()` matchers for flexible contracts, publishing the pact file for provider verification, and the pact broker CLI.""",

"""**Task (Code Generation):**
Build a `createLoadTest` framework using `k6` for API performance testing:

```js
// load-tests/checkout.k6.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const checkoutRate = new Rate('checkout_success_rate');
const checkoutDuration = new Trend('checkout_duration_ms');

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // ramp up
    { duration: '1m',  target: 50 },   // sustained load
    { duration: '30s', target: 0 },    // ramp down
  ],
  thresholds: {
    checkout_success_rate: ['rate>0.95'],  // 95% must succeed
    checkout_duration_ms:  ['p(95)<2000'], // P95 < 2s
  },
};

export default function() {
  const res = http.post('http://api.test/checkout', JSON.stringify({ items: [...] }), {
    headers: { 'Content-Type': 'application/json' },
  });
  checkoutRate.add(res.status === 201);
  checkoutDuration.add(res.timings.duration);
  sleep(1);
}
```

Show: k6 stages (ramp-up/sustained/ramp-down), custom metrics (`Rate`, `Trend`, `Counter`), thresholds for pass/fail, and running with `k6 run --out influxdb=http://localhost:8086/k6` for Grafana dashboards.""",

"""**Task (Code Generation):**
Implement a `createVisualRegressionTest` using Playwright's screenshot comparison:

```ts
test('ProductCard visual regression', async ({ page }) => {
  await page.goto('/storybook/product-card--default');
  await page.waitForLoadState('networkidle');

  // Mask dynamic content (dates, ads):
  await expect(page).toHaveScreenshot('product-card-default.png', {
    mask: [page.locator('.timestamp'), page.locator('.ad-banner')],
    maxDiffPixels: 100,
    threshold: 0.2,
  });
});

test('ProductCard dark mode', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto('/storybook/product-card--default');
  await expect(page).toHaveScreenshot('product-card-dark.png');
});
```

Show: Playwright's `toHaveScreenshot` with tolerance settings, masking dynamic elements, `--update-snapshots` flag for updating baselines, integrating with CI (store screenshots as artifacts), and `percy.io` or `chromatic.com` for cloud visual testing.""",

"""**Task (Code Generation):**
Build a `createMutationTest` setup using Stryker for mutation testing:

```javascript
// stryker.config.mjs
export default {
  testRunner: 'vitest',
  mutate: ['src/**/*.ts', '!src/**/*.test.ts', '!src/**/types.ts'],
  coverageAnalysis: 'perTest',
  reporters: ['html', 'progress', 'dashboard'],
  thresholds: { high: 80, low: 60, break: 50 },
  ignorePatterns: ['node_modules', 'dist'],
};
```

Show: the mutation score concept (% of mutations caught by tests), common mutation operators (arithmetic: `+→-`, boundary: `>→>=`, boolean: `&&→||`), identifying undertested code (surviving mutants reveal missing assertions), and running Stryker in CI with `--dryRun` to check config before full run.""",

"""**Task (Code Generation):**
Implement a `createApiMock` using MSW for realistic network simulation in development:

```ts
// src/mocks/handlers.ts
export const handlers = [
  http.get('/api/products', async ({ request }) => {
    const url = new URL(request.url);
    const page = Number(url.searchParams.get('page') ?? '1');
    const limit = Number(url.searchParams.get('limit') ?? '20');

    // Realistic delay simulation:
    await delay(Math.random() * 200 + 100); // 100-300ms

    const products = mockProducts.slice((page-1)*limit, page*limit);
    return HttpResponse.json({ products, total: mockProducts.length, page });
  }),

  http.post('/api/products', async ({ request }) => {
    const body = await request.json();
    const validated = ProductCreateSchema.safeParse(body);
    if (!validated.success) {
      return HttpResponse.json({ errors: validated.error.flatten() }, { status: 422 });
    }
    const created = { ...validated.data, id: `prod-${Date.now()}` };
    return HttpResponse.json(created, { status: 201 });
  }),
];
```

Show: the MSW `browser.js` setup for development, `worker.js` setup for tests, `delay()` for realistic latency, error simulation (`http.get('/api/flaky', () => { if (Math.random() > 0.8) return HttpResponse.error(); })`), and the Storybook MSW integration.""",

"""**Task (Code Generation):**
Build a `createDatabaseTest` utility for integration tests with transactions and isolation:

```ts
// Each test gets a fresh transaction that's rolled back after:
describe('UserRepository integration tests', () => {
  let txn: Transaction;

  beforeEach(async () => {
    txn = await db.beginTransaction();
  });

  afterEach(async () => {
    await txn.rollback(); // All changes reverted — DB stays clean
  });

  it('creates a user with hashed password', async () => {
    const repo = new UserRepository(txn);
    const user = await repo.create({ email: 'test@example.com', password: 'plaintext' });

    expect(user.id).toBeDefined();
    expect(user.passwordHash).not.toBe('plaintext');
    expect(await bcrypt.compare('plaintext', user.passwordHash)).toBe(true);
  });
});
```

Show: PostgreSQL `SAVEPOINT` for nested transactions, passing the transaction to repository constructors, the test isolation guarantee (rollback = no cleanup SQL needed), and Prisma's `$transaction` for testing transactional operations.""",

"""**Task (Code Generation):**
Implement a `createStorybook` test-driven component development workflow:

```ts
// src/components/Button/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { expect, fn, userEvent, within } from '@storybook/test';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  component: Button,
  args: { onClick: fn() },
};
export default meta;

export const Primary: StoryObj<typeof Button> = {
  args: { variant: 'primary', children: 'Click Me' },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');
    await userEvent.click(button);
    await expect(args.onClick).toHaveBeenCalledOnce();
  },
};
```

Show: Storybook 7+ `play` functions for interaction testing, `fn()` for spy functions, the `@storybook/test` assertion library, running play tests with `storybook test`, and importing stories as test cases in Vitest (`StorybookVitestPlugin`).""",

# ── Debugging ─────────────────────────────────────────────────────────────────

"""**Debug Scenario:**
A developer's Jest test suite takes 8 minutes to run 500 tests, even with `--runInBand` disabled:

```
# jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  /* No other optimization */
};
```

Investigation: each test file imports `@testing-library/react` which re-initializes a jsdom environment (expensive). Show: using `jsdom: { ... }` global setup instead of per-file env, switching to Vitest (faster startup), `--testPathPattern` to run only changed tests, `--passWithNoTests` for CI skipping, and the `jest.config.js` `projects` array for separate environments (unit: node, component: jsdom).""",

"""**Debug Scenario:**
A React Testing Library test fails because `getByRole` can't find a button element that clearly exists in the DOM:

```tsx
render(<form><button type="submit">Submit</button></form>);
screen.getByRole('button', { name: 'Submit' }); // Error: Unable to find role 'button' with name 'Submit'
```

Investigation: the `<form>` has `aria-hidden="true"` set accidentally, hiding all its children from the accessibility tree. Show: using `screen.debug()` to inspect the rendered output, the `aria-hidden` propagation (hides all descendants), fixing by removing `aria-hidden` from the ancestor, and `screen.getByTestId` as an escape hatch (though role-based queries are preferred).""",

"""**Debug Scenario:**
A `useEffect`-based test fails with "act() warning" even though `act` is used:

```tsx
it('loads data on mount', async () => {
  render(<UserProfile userId="u1" />);
  // Warning: An update to UserProfile inside a test was not wrapped in act(...)!
});
```

The component fetches data in `useEffect` and updates state asynchronously. `render()` is wrapped in a sync `act` but the async updates happen after. Show: using `waitFor` from Testing Library (`await waitFor(() => expect(screen.getByText('Alice')).toBeInTheDocument())`), `findByText` (async variant that auto-waits), and why `act` needs to be `async` for async updates (`await act(async () => { render(...); })`).""",

"""**Debug Scenario:**
A developer's test mocks don't reset between tests, causing test pollution:

```ts
jest.mock('./api', () => ({ fetchUser: jest.fn() }));

it('shows loading state', () => {
  (fetchUser as jest.Mock).mockReturnValue(new Promise(() => {}));
  render(<UserCard id="u1" />);
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});

it('shows user data', async () => {
  // Bug: fetchUser still returns a pending Promise from the previous test!
  (fetchUser as jest.Mock).mockResolvedValue({ name: 'Alice' });
  // Race condition: previous mock might win
});
```

Show: calling `jest.clearAllMocks()` / `vi.clearAllMocks()` in `beforeEach` (or `clearMocks: true` in config), `jest.resetAllMocks()` (clears AND resets implementations), `jest.restoreAllMocks()` (also restores spied originals), and the difference between the three.""",

"""**Debug Scenario:**
A Playwright test is flaky — it fails 20% of the time with "element not found" even though the element appears in the video recording:

```ts
await page.click('#submit-button'); // Fast click
await page.waitForSelector('.success-message'); // Flaky!
```

The test clicks the button and immediately waits for a success message, but the button might not be clickable yet (form validation running, or network request in-flight). Show: using `await page.click('#submit-button')` → Playwright auto-waits for the element to be stable (clickable, visible, enabled), then `await expect(page.locator('.success-message')).toBeVisible()` with built-in retry (up to 5 seconds), and `page.waitForResponse` for network assertions instead of DOM assertions.""",

"""**Debug Scenario:**
A test spy is correctly attached but the mock function is never called because the module is imported before the mock is set up:

```ts
import { sendEmail } from './email'; // Module imported at top!

jest.mock('./email'); // Mock set up AFTER import

it('sends welcome email', async () => {
  await registerUser({ email: 'alice@example.com' });
  expect(sendEmail).toHaveBeenCalledWith(expect.objectContaining({ to: 'alice@example.com' }));
  // sendEmail is never called!
});
```

`jest.mock()` is hoisted to the top of the file by Babel/Jest transform, so this actually works correctly in Jest. The real bug: `registerUser` imports `email` from a different path alias. Show: checking the actual import path used by `registerUser`, `jest.mock` with factory function, and `vi.mock` hoisting behavior in Vitest.""",

"""**Debug Scenario:**
A developer's `toHaveBeenCalledWith` assertion fails because of extra arguments passed to the mock:

```ts
const mockHandler = vi.fn();
button.onclick = () => mockHandler('click', { bubbles: true, extra: 'data' });

expect(mockHandler).toHaveBeenCalledWith('click', { bubbles: true });
// Fails! Extra 'extra' property in the actual call
```

`toHaveBeenCalledWith` uses deep equality — extra properties cause failure. Show: using `expect.objectContaining({ bubbles: true })` for partial object matching, `expect.arrayContaining` for partial array matching, `toHaveBeenCalledWith('click', expect.objectContaining({ bubbles: true }))`, and `toHaveBeenLastCalledWith` vs `toHaveBeenNthCalledWith`.""",

"""**Debug Scenario:**
A developer's Vitest test uses `vi.spyOn` but the spy doesn't intercept calls because of ES module mocking:

```ts
import * as api from './api';

vi.spyOn(api, 'fetchUser').mockResolvedValue(mockUser);

it('should call fetchUser', async () => {
  await loadUser('u1');
  expect(api.fetchUser).toHaveBeenCalled(); // Never called!
});
```

`loadUser` imports `fetchUser` directly (`import { fetchUser } from './api'`) — it holds a direct reference to the function, not via the module namespace `api`. Spying on `api.fetchUser` replaces the object property but not the imported binding. Show: using `vi.mock('./api', () => ({ fetchUser: vi.fn().mockResolvedValue(mockUser) }))` for complete module mocking, and the ES module static binding vs CommonJS dynamic reference difference.""",

"""**Debug Scenario:**
A developer's React Testing Library test queries break after updating from RTL v12 to v14:

```tsx
// RTL v12 (old):
const { getByText } = render(<Component />);
getByText('Submit');

// RTL v14 (current):
render(<Component />); // screen is preferred
screen.getByText('Submit'); // Works, but old destructured queries also still work

// Actual breaking change: custom render wrapper no longer forwards all queries:
const { getByText, findByRole } = customRender(<Component />);
findByRole('button'); // TypeError: findByRole is not a function!
```

The custom render function only returns synchronous queries but not async ones. Show: updating the custom render to return the full result of RTL's `render` (`return { ...renderResult, ...extraUtils }`), using `screen` from Testing Library (always up-to-date, no need to destructure), and the migration guide for RTL v13/v14 breaking changes.""",

"""**Debug Scenario:**
A developer's test coverage shows 100% for a utility function, but the function has a critical bug:

```ts
function divide(a: number, b: number): number {
  return a / b; // 100% line coverage, but...
}

// Tests only cover:
expect(divide(10, 2)).toBe(5);  // Lines covered: all (only 1 line)
expect(divide(6, 3)).toBe(2);

// Missing: divide(10, 0) → returns Infinity, not an error!
```

100% line coverage doesn't mean complete testing. Show: branch coverage (if/else paths), edge case testing (0, negative, NaN, Infinity), adding the missing test `expect(divide(10, 0)).toThrow()` (or deciding `Infinity` is acceptable), and why code coverage is a FLOOR metric (failing below threshold is bad) but not a CEILING (100% doesn't mean no bugs).""",

"""**Debug Scenario:**
A developer's test for an async function incorrectly uses `.resolves` with `expect` and the test always passes:

```ts
it('rejects with invalid input', async () => {
  // BUG: Using resolves when testing a rejection!
  await expect(processPayment({ amount: -1 })).resolves.toThrow();
  // This test always passes because resolves is used, not rejects!
});
```

`.resolves` unwraps a resolved Promise — if the Promise rejects, the test FAILS (because `.resolves` expects resolution). But if the function accidentally resolves instead of rejecting, the test still passes. Show: using `.rejects.toThrow()` for rejected promises, `try/catch` pattern with `fail('should have thrown')`, and `await expect(fn()).rejects.toThrow(PaymentError)`.""",

"""**Debug Scenario:**
A Playwright test clicks a button but the action fails silently because the element is covered by a cookie banner:

```ts
await page.click('[data-testid="add-to-cart"]'); // No error thrown!
// But the cart count doesn't update — click was intercepted by cookie banner
```

Playwright's click succeeds (the element is technically clickable), but a cookie banner `z-index: 99999` intercepts the click event. Show: dismissing the cookie banner in `beforeEach` (`await page.click('[data-testid="accept-cookies"]')`), using `page.locator('[data-testid="add-to-cart"]').click({ force: true })` to bypass intercept detection, `page.screenshot({ path: 'debug.png' })` for debugging, and the `--headed` flag to watch the test in the browser.""",

"""**Debug Scenario:**
A developer's Jest transform config causes TypeScript tests to fail because JSX isn't transformed:

```
Error: Cannot read properties of undefined (reading 'createElement')
SyntaxError: Unexpected token '<'
```

```js
// jest.config.js
module.exports = {
  transform: {
    '^.+\\.tsx?$': 'ts-jest',
  },
};
```

`ts-jest` is configured but the `tsconfig.json` has `"jsx": "react-jsx"` (new JSX transform) while the test environment doesn't have React in scope. Show: setting `"jsx": "react"` in the tsconfig used by ts-jest, OR adding `import React from 'react'` to test files, OR configuring ts-jest to use `@swc/jest` which handles JSX automatically, and the Jest `testEnvironment: 'jsdom'` requirement for `document` and `window`.""",

"""**Debug Scenario:**
A developer's test uses `setTimeout` assertions but the timer callback is never called:

```ts
it('shows a tooltip after 500ms hover', async () => {
  render(<TooltipButton />);
  fireEvent.mouseEnter(screen.getByRole('button'));

  // Wait for tooltip:
  await waitFor(() => {
    expect(screen.getByRole('tooltip')).toBeInTheDocument();
  }, { timeout: 1000 });
  // Fails! Tooltip never appears.
});
```

Real timers run, but in test environment the 500ms might not have elapsed within `waitFor`'s polling interval. Show: using `vi.useFakeTimers()` + `act(() => vi.advanceTimersByTime(500))` for deterministic timer control, OR configuring `waitFor` with a longer timeout (`{ timeout: 2000, interval: 100 }`), and the trade-off between fake timers (fast, deterministic) vs real timers (realistic but slower).""",

"""**Debug Scenario:**
A developer's React component test using `userEvent.type` causes unexpected behavior because `userEvent.setup()` is not called:

```ts
// RTL @testing-library/user-event v14:
it('filters products as user types', async () => {
  render(<SearchInput onSearch={mockSearch} />);
  await userEvent.type(screen.getByRole('searchbox'), 'react'); // Missing setup!
});
```

In `@testing-library/user-event` v14, calling `userEvent.type` directly (without `userEvent.setup()`) uses a legacy API that doesn't fire all events (pointerdown, pointermove, focus, input, etc.) accurately. Show: the correct pattern:

```ts
const user = userEvent.setup();
await user.type(screen.getByRole('searchbox'), 'react');
```

And for `vi.useFakeTimers` compatibility with userEvent: `userEvent.setup({ advanceTimers: vi.advanceTimersByTime })`.""",

"""**Debug Scenario:**
A developer's snapshot test fails on CI but passes locally because of OS-dependent rendering:

```
Snapshot failed:
- Expected: "1,234.56"
+ Received: "1.234,56"
```

`Intl.NumberFormat` uses the system locale. The developer's Mac formats numbers with commas, but the Linux CI server uses a different locale. Show: mocking `Intl.NumberFormat` in tests to use a fixed locale, setting `LC_ALL=en-US` in the CI environment, using `new Intl.NumberFormat('en-US')` explicitly (not relying on system locale), and the `toLocaleString` gotcha (also locale-dependent).""",

"""**Debug Scenario:**
A developer's Playwright test fails intermittently because it asserts on the URL before the navigation completes:

```ts
await page.click('[data-testid="checkout-button"]');
expect(page.url()).toContain('/checkout'); // Flaky! Sometimes fails
```

`page.url()` is read synchronously immediately after `click`. The navigation might not have started yet. Show: using `await page.waitForURL('**/checkout')` which waits until the URL changes, `await expect(page).toHaveURL(/checkout/)` (Playwright's assertion with retry), and wrapping navigation-triggering actions with `Promise.all([page.waitForNavigation(), page.click(...)])` for the old approach.""",

"""**Debug Scenario:**
A developer's test for a React hook crashes because hooks can't be called outside a React component:

```ts
it('useCounter increments correctly', () => {
  const { count, increment } = useCounter(0); // Error: Invalid hook call!
  increment();
  expect(count).toBe(1);
});
```

Hooks can only be called inside React components (or other hooks). Show: using `renderHook` from `@testing-library/react`:

```ts
const { result } = renderHook(() => useCounter(0));
act(() => result.current.increment());
expect(result.current.count).toBe(1);
```

And the `initialProps` option for hooks that accept props, and the `rerender` function for testing hooks that respond to prop changes.""",

"""**Debug Scenario:**
A developer's E2E test is extremely slow because it navigates through the full UI for each test, including the login flow:

```ts
// Every test file:
beforeEach(async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('[type="submit"]');
  await page.waitForURL('/dashboard'); // ~3s per test
});
// 100 tests × 3s = 5 minutes just for login!
```

Show: Playwright's `storageState` fixture for authentication:
1. Run login once in `globalSetup` and save `storageState` (cookies + localStorage) to a file
2. Load the saved state in tests: `use: { storageState: 'playwright/.auth/user.json' }`
This skips the login UI and restores the session directly.""",

"""**Debug Scenario:**
A developer's test for error boundaries doesn't catch errors thrown in `useEffect`:

```ts
it('shows error UI when data fetch fails', async () => {
  render(
    <ErrorBoundary fallback={<div>Error!</div>}>
      <UserProfile userId="bad-id" />
    </ErrorBoundary>
  );
  // UserProfile throws in useEffect when fetch fails
  // But ErrorBoundary doesn't catch it!
  expect(screen.getByText('Error!')).toBeInTheDocument(); // Fails
});
```

React Error Boundaries don't catch errors in `useEffect` or async callbacks — only errors thrown during rendering. Show: using React 18's `startTransition` + error boundary pattern for some async cases, handling fetch errors in state (`setError(err)`) and rendering accordingly, and the Playwright approach (E2E testing verifies the full behavior without this limitation).""",

"""**Debug Scenario:**
A developer's mock for `fetch` is not being called even though the component triggers a network request:

```ts
global.fetch = vi.fn().mockResolvedValue({
  ok: true,
  json: () => Promise.resolve({ users: [] }),
});

render(<UserList />);
// fetch is never called!
```

Investigation: `UserList` uses `axios` internally, not the native `fetch`. The mock targets the wrong library. Show: using `vi.mock('axios')` to mock the library directly, or MSW (which intercepts at the network level — catches both `fetch` and `axios`), and inspecting `global.fetch.mock.calls` vs `axios.get.mock.calls` to confirm which is called.""",

"""**Debug Scenario:**
A developer's test for localStorage interaction fails because `localStorage` is not available in the test environment:

```ts
it('saves draft to localStorage', () => {
  const { getByRole } = render(<DraftEditor />);
  fireEvent.change(getByRole('textbox'), { target: { value: 'Hello' } });
  expect(localStorage.getItem('draft')).toBe('Hello');
  // ReferenceError: localStorage is not defined
});
```

The test environment is Node.js (no browser APIs). Show: switching the Jest/Vitest `testEnvironment` to `jsdom` (provides `localStorage`), or mocking `localStorage` manually (`global.localStorage = { getItem: vi.fn(), setItem: vi.fn() }`), and the `jest-localstorage-mock` package for automatic localStorage mocking with `vi.resetModules()` between tests.""",

"""**Debug Scenario:**
A developer's Vitest coverage report shows a function as uncovered even though there is a test for it:

```ts
// utils.ts
export function clampValue(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

// utils.test.ts
it('clamps values', () => {
  expect(clampValue(5, 0, 10)).toBe(5);
});
// Coverage shows clampValue as covered, but...
// V8 coverage shows the 'min' branch is not covered (value < min never tested)
```

Line coverage shows the function is called, but branch coverage reveals the `min` path isn't tested. Show: testing the under-limit case (`clampValue(-1, 0, 10)` → 0), over-limit case (`clampValue(15, 0, 10)` → 10), and using `v8` coverage provider (more accurate branch coverage) vs `istanbul` (default in Vitest).""",

"""**Debug Scenario:**
A developer's component test uses `screen.queryByText` but a slightly different text causes the test to pass incorrectly:

```tsx
render(<ErrorMessage message="User not found" />);
expect(screen.queryByText('User not found!')).not.toBeInTheDocument(); // Passes! Wrong.
// The element has 'User not found' (no exclamation)
// queryByText doesn't match partial text by default but this is a different string
```

`queryByText` returns `null` for 'User not found!' when the element contains 'User not found' — the test incorrectly passes because the element isn't found (so `not.toBeInTheDocument` is true). Show: using `screen.getByText('User not found')` (would throw and catch the bug), using the `exact: false` option for partial matching, and why the test assertion should be verifying presence, not absence.""",

"""**Debug Scenario:**
A developer's test double leaks between test files when using `jest.spyOn` without restoration:

```ts
// user.test.ts:
jest.spyOn(Date, 'now').mockReturnValue(1_700_000_000_000);
// Missing: jest.restoreAllMocks() or afterEach cleanup!

// session.test.ts (runs after user.test.ts):
const now = Date.now();
// Still returns 1_700_000_000_000! Test from prev file affected this
```

`jest.spyOn` modifies the original object. Without restoration, the mock persists across test files in the same runner process. Show: adding `restoreMocks: true` to `jest.config.js` (auto-restores all spies after each test), `jest.restoreAllMocks()` in `afterEach`, and `vi.spyOn` + `vi.restoreAllMocks()` in Vitest.""",

"""**Debug Scenario:**
A developer's integration test fails because the database state from a previous test leaked:

```ts
describe('OrderService', () => {
  it('creates order', async () => {
    await orderService.create({ userId: 'u1', items: [{ id: 'p1' }] });
    const orders = await db.orders.findMany();
    expect(orders).toHaveLength(1); // ✓ First test passes

    it('lists all orders', async () => {
      const orders = await db.orders.findMany();
      expect(orders).toHaveLength(0); // ✗ Fails! 1 order from previous test!
    });
  });
```

Tests share database state without cleanup. Show: using `beforeEach`/`afterEach` to truncate relevant tables (`DELETE FROM orders`, `DELETE FROM order_items`), using database `TRUNCATE ... CASCADE` for cleanup, transaction rollback approach (start transaction in `beforeEach`, rollback in `afterEach`), and database seeding for consistent test data.""",

"""**Debug Scenario:**
A developer's `waitFor` in Testing Library adds unnecessary test latency because it uses the default timeout:

```ts
it('shows error after failed submission', async () => {
  await user.click(submitButton);
  await waitFor(() => {
    expect(screen.getByRole('alert')).toBeInTheDocument();
  }); // Waits up to 1000ms (default), but the error appears in 10ms
});
```

`waitFor` polls every 50ms up to 1000ms by default — fine for async, but it ALSO adds overhead even when the assertion passes quickly. Show: using `findByRole('alert')` instead of `waitFor` + `getByRole` (findByRole is a convenient shortcut for `waitFor(() => getByRole(...))`), reducing the timeout for known-fast assertions (`{ timeout: 200 }`), and ensuring MSW handlers resolve immediately in tests (use `delay: 0` or no delay).""",

"""**Debug Scenario:**
A developer's custom Vitest reporter fails in CI because it writes files to a relative path:

```ts
// custom-reporter.ts
class Reporter {
  onFinished(files) {
    fs.writeFileSync('./test-results.json', JSON.stringify(files));
    // In CI: current directory is not the project root!
  }
}
```

CI runners often execute from a different working directory than the project. Show: using `path.resolve(__dirname, '../test-results.json')` for absolute paths, using the `outputFile` option in Vitest config for standard reporters, and environment variables (`process.env.CI` and `process.env.GITHUB_WORKSPACE`) for CI-specific output paths.""",

]

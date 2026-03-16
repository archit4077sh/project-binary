"""
snippets/q_testing.py — 28 FRESH Testing questions (mix of debugging + code generation)
Zero overlap with archived set.
"""

Q_TESTING = [

"""**Task (Code Generation):**
Write a custom RTL `renderWithProviders` utility that wraps components with all required providers (React Query, Redux, Router, Theme):

```ts
const { getByRole, user } = renderWithProviders(<LoginForm />, {
  preloadedState: { auth: { user: null } },
  queryClient: new QueryClient({ defaultOptions: { queries: { retry: false } } }),
});
```

Show the utility function, how to configure each provider for testing (query client with retries disabled, in-memory router, Redux store with preloaded state), and a `user` setup using `@testing-library/user-event` v14.""",

"""**Debug Scenario:**
A test for a form component is flaky — it passes locally but fails in CI with "Unable to find element with the text: Submit". The form renders a loading state during submission and hides the Submit button.

```ts
await user.click(screen.getByText('Submit'));
// Test continues immediately — button disappears during loading
expect(screen.getByText('Success')).toBeInTheDocument(); // fails
```

Show the correct RTL async waiting patterns: `findByText`, `waitFor`, `waitForElementToBeRemoved`, and explain when each is appropriate. Show why `getBy*` queries fail for async UI changes.""",

"""**Task (Code Generation):**
Implement a comprehensive MSW (Mock Service Worker) setup for a Next.js 14 app that works in:
1. Browser (Storybook, manual testing)
2. Jest (unit/integration tests with `msw/node`)
3. Playwright E2E tests

Show: the handler files, the browser setup (`public/mockServiceWorker.js`), the Jest setup file (`beforeAll`, `afterEach`, `afterAll`), the Playwright global setup, and a shared handler for `/api/users` used across all three environments.""",

"""**Debug Scenario:**
A Playwright test clicks a button that opens a modal, then interacts with the modal. The test fails intermittently because Playwright clicks the button before the modal's animation has completed, and the interactive elements inside are not yet clickable.

```ts
await page.click('[data-testid="open-modal"]');
await page.click('[data-testid="modal-confirm"]'); // flaky
```

Show the correct Playwright waiting strategies: `waitForSelector` with `state: 'attached'` vs `'visible'` vs `'stable'`, how to wait for animation completion using CSS `transition-duration`, and the `page.waitForFunction` approach for complex readiness conditions.""",

"""**Task (Code Generation):**
Write a Vitest + RTL test suite for a `useCart` hook that manages shopping cart state:

```ts
describe('useCart', () => {
  it('adds items to cart')
  it('removes items from cart')
  it('calculates total correctly')
  it('applies discount code via API')
  it('persists cart to localStorage')
  it('restores cart from localStorage on mount')
});
```

Show complete implementations of at least 4 of these tests, demonstrating: `renderHook`, `act`, localStorage mocking, and MSW for the discount API endpoint.""",

"""**Debug Scenario:**
A Jest test for a Redux slice is failing with `TypeError: Cannot read properties of undefined (reading 'type')` when dispatching an action created by RTK's `createAsyncThunk`.

```ts
test('fetchUser updates state', async () => {
  const dispatch = jest.fn();
  await fetchUser('1')(dispatch, () => store.getState(), undefined);
  expect(dispatch).toHaveBeenCalledWith(fetchUser.fulfilled(...));
});
```

Explain why testing `createAsyncThunk` via direct invocation is fragile, and show the correct approach: testing the reducer with manually dispatched `fulfilled`/`rejected` actions, and an integration test using the real store.""",

"""**Task (Code Generation):**
Implement a visual regression testing setup using Playwright + `@playwright/test` screenshots:

```ts
test('dashboard renders correctly', async ({ page }) => {
  await page.goto('/dashboard');
  await page.waitForSelector('[data-testid="chart"]', { state: 'visible' });
  await expect(page).toHaveScreenshot('dashboard.png', { 
    threshold: 0.1,
    mask: [page.locator('[data-testid="live-clock"]')] // mask dynamic content
  });
});
```

Show: the Playwright config for screenshot comparison, how to update baselines (`--update-snapshots`), how to mask dynamic content (timestamps, live data), and a CI GitHub Actions workflow that fails PRs on visual regressions.""",

"""**Debug Scenario:**
A Jest test suite for a React component that uses `IntersectionObserver` crashes with `ReferenceError: IntersectionObserver is not defined` in jsdom.

```ts
// Component uses IntersectionObserver for lazy loading
test('lazy loads content when visible', () => {
  render(<LazySection />);
});
```

Show how to:
1. Mock `IntersectionObserver` globally in Jest setup
2. Simulate intersection events in tests (trigger the observer callback manually)
3. Test both the "not intersecting yet" and "intersecting" states
4. Avoid the mock leaking between tests""",

"""**Task (Code Generation):**
Write a complete test for an optimistic update mutation using React Query's `useMutation`:

The component shows a list of reports. Clicking "Archive" immediately removes the report from the list (optimistic), and re-adds it if the API fails.

```ts
describe('Archive report', () => {
  it('removes report optimistically')
  it('re-adds report if API fails')
  it('does not re-add if API succeeds')
});
```

Show all three tests with MSW handlers for success and failure cases, `waitFor` assertions, and how to verify the rollback.""",

"""**Debug Scenario:**
Storybook stories for a form component throw an error when running in Storybook's test runner (Playwright-based):

```
Error: Invalid hook call. Hooks can only be called inside of a function component.
```

The story uses decorators:
```ts
export const WithAuth: Story = {
  decorators: [(Story) => <AuthProvider><Story /></AuthProvider>],
};
```

The error comes from `AuthProvider` calling a hook internally. It works in the browser but fails in the test runner. Diagnose whether this is a React version mismatch between Storybook's internal React and the app's React, and show the fix.""",

"""**Task (Code Generation):**
Implement a contract testing setup between a Next.js frontend and a backend API using Pact.js:

```ts
// Consumer test (frontend):
await provider
  .given('user 1 exists')
  .uponReceiving('a request for user 1')
  .withRequest({ method: 'GET', path: '/api/users/1' })
  .willRespondWith({ status: 200, body: like({ id: '1', name: string() }) });
```

Show: the Pact consumer test for a `useUser` hook, how the generated pact file is published to a Pact Broker, and the provider verification test on the backend side.""",

"""**Debug Scenario:**
A test for a file upload component needs to simulate a user selecting a file. `userEvent.upload` is used but the component receives an empty `FileList`:

```ts
const file = new File(['content'], 'test.csv', { type: 'text/csv' });
const input = screen.getByLabelText('Upload file');
await user.upload(input, file);
// Component receives: e.target.files.length === 0
```

Diagnose why `userEvent.upload` might fail to populate `files` in jsdom, and show the correct approach: using `Object.defineProperty` to set `files` on the input, the correct v14 `@testing-library/user-event` API for uploads, and how to test drag-and-drop file input.""",

"""**Task (Code Generation):**
Write a full Playwright E2E test for a multi-step checkout flow:

Steps: Cart → Shipping → Payment → Confirmation

Requirements:
- Uses Page Object Model for each page
- Mocks the payment API (Stripe) to avoid real charges
- Tests: happy path, invalid card number, network error during payment
- Retries once on flaky network errors
- Records a video of the test run on failure

Show the `CartPage`, `PaymentPage` Page Object classes and the test file.""",

"""**Debug Scenario:**
A Jest test using `jest.useFakeTimers()` for a debounced search input hangs indefinitely. `act()` isn't warning, but the test never resolves.

```ts
jest.useFakeTimers();
render(<SearchInput onSearch={mockFn} debounce={300} />);
await userEvent.type(input, 'hello');
jest.advanceTimersByTime(300);
await waitFor(() => expect(mockFn).toHaveBeenCalledWith('hello'));
// hangs here...
```

Explain why mixing `jest.useFakeTimers()` with `waitFor` can cause infinite loops (waitFor uses real timers internally), and show the correct approach using `jest.runAllTimers()` vs `jest.advanceTimersByTime()` with and without async `waitFor`.""",

"""**Task (Code Generation):**
Implement property-based testing for a `sortProducts` function using `fast-check`:

```ts
// The function should be deterministic and stable
expect(sortProducts(reverse(products))).toEqual(sortProducts(products)); // order invariant
expect(sortProducts(sortProducts(products))).toEqual(sortProducts(products)); // idempotent
```

Show:
1. The `fast-check` arbitrary for generating Product objects
2. Properties to test: idempotence, stability, correctness of sort criteria
3. A shrinking example (when a test fails, fast-check finds the minimal failing case)
4. Integration with Jest/Vitest""",

"""**Debug Scenario:**
A Playwright test for a dashboard with real-time WebSocket updates is flaky because the test asserts on data that arrives via WebSocket, and the timing is non-deterministic.

```ts
await page.goto('/dashboard');
await expect(page.locator('[data-testid="live-price"]')).toHaveText('$42.50');
// Flaky: WebSocket hasn't delivered the price yet
```

Show how to:
1. Mock the WebSocket server in Playwright using `page.routeWebSocket()`
2. Send controlled messages from the test
3. Assert on UI updates after specific WebSocket messages
4. Avoid arbitrary `page.waitForTimeout()` calls""",

"""**Task (Code Generation):**
Write a snapshot test strategy for a component library that avoids brittle "big blob" snapshots:

Instead of:
```ts
expect(render(<DataTable rows={rows} />)).toMatchSnapshot(); // 500-line snapshot
```

Use:
```ts
// Focused structural snapshots:
expect(table.columnHeaders).toMatchSnapshot();
expect(table.rowCount).toBe(5);
expect(firstRow.textContent).toMatchSnapshot();
```

Show the custom `toMatchSnapshot` matchers, how to serialize only semantically meaningful parts of the component, and `inline snapshots` for small assertions. Explain when to use `toMatchInlineSnapshot` vs external `.snap` files.""",

"""**Debug Scenario:**
A component test for a `<RichTextEditor>` (using TipTap/ProseMirror) passes in jsdom but fails in Playwright with:

```
Error: ResizeObserver is not defined
```

TipTap uses `ResizeObserver` internally. Diagnose whether this is a polyfill issue or a Playwright configuration issue, show how to add `ResizeObserver` polyfill to Playwright's browser context, and explain why `ResizeObserver` is available in modern browsers natively but might not be in test environments.""",

"""**Task (Code Generation):**
Implement a test data factory system for a TypeScript/Jest test suite:

```ts
const user = UserFactory.build({ role: 'admin' }); // all fields filled with realistic defaults
const users = UserFactory.buildList(10, { active: true });
const userWithPosts = UserFactory.buildWithRelations(['posts', 'comments']);
```

Show:
1. The `Factory<T>` base class with `build`, `buildList`, `buildWithRelations`
2. The `UserFactory` concrete implementation with Faker.js for realistic data
3. How to override specific fields while defaulting others
4. Sequence support (each `build` call increments ID)""",

"""**Debug Scenario:**
A Next.js API route test using `node:test` (without Jest) fails to import the route handler because it uses Next.js-specific APIs (`cookies()`, `headers()`):

```ts
import { GET } from '../app/api/users/route';
// Error: cookies is not defined (Next.js internal not available in plain Node)
```

Show how to mock Next.js server-side APIs (`cookies`, `headers`, `NextRequest`, `NextResponse`) for unit testing Route Handlers without running a full Next.js server, and compare this to integration testing with `supertest` against a running server.""",

"""**Task (Code Generation):**
Write a comprehensive accessibility test suite for a modal component using `jest-axe` and RTL:

```ts
describe('Modal accessibility', () => {
  it('has no axe violations when open')
  it('traps focus inside the modal')
  it('returns focus to trigger on close')
  it('closes on Escape key')
  it('announces to screen readers via aria-live')
  it('has correct ARIA roles and attributes')
});
```

Show complete implementations of all 6 tests, demonstrating `jest-axe`, keyboard event simulation, and `aria-*` attribute assertions.""",

"""**Debug Scenario:**
A Jest test uses `jest.mock()` to mock an ES module. The mock works for named exports but the default export is still the real implementation:

```ts
jest.mock('../api/users', () => ({
  ...jest.requireActual('../api/users'),
  fetchUsers: jest.fn(), // named export mocked ✓
  // default export not mocked
}));
```

The component imports `import ApiClient from '../api/users'`. Show the correct pattern for mocking both named and default exports from ES modules, the `__esModule: true` flag, and why `jest.spyOn` is preferable for partial mocking.""",

"""**Task (Code Generation):**
Implement a CI/CD testing strategy for a Next.js app with GitHub Actions:

1. **Unit tests** (Vitest) — run on every push, fast (<60s)
2. **Integration tests** (Playwright component testing) — run on PR
3. **E2E tests** (Playwright full browser) — run on merge to main
4. **Visual regression** — run on PR, block merge if images differ

Show the complete GitHub Actions workflow YAML with:
- Parallelized test sharding for E2E (4 shards)
- Playwright report upload to GitHub artifacts
- Test result caching between runs
- Failure notifications via GitHub PR comments""",

"""**Debug Scenario:**
After upgrading from `@testing-library/user-event@13` to `v14`, all tests that use `userEvent.type` are broken. The v14 API requires `setup()` but existing tests use the v13 direct import pattern.

```ts
// v13 (broken):
userEvent.type(element, 'hello');

// v14 requires:
const user = userEvent.setup();
await user.type(element, 'hello');
```

Beyond the migration, explain the behavioral differences: v14 simulates real browser events (pointerdown, mousedown, focus, keydown, input, keyup) while v13 used `fireEvent`. Show a codemod or migration helper to update 200+ test files automatically using jscodeshift.""",

"""**Task (Code Generation):**
Write mutation tests using Stryker for a critical `calculateDiscount` utility:

```ts
function calculateDiscount(price: number, code: string): number {
  if (code === 'SAVE10') return price * 0.9;
  if (code === 'SAVE20') return price * 0.8;
  if (price > 100) return price * 0.95; // loyalty discount
  return price;
}
```

Show:
1. The Stryker configuration (`stryker.config.mjs`)
2. Why standard unit tests might pass with 100% line coverage but miss mutations
3. Mutations Stryker would apply to this function
4. Additional tests needed to kill each mutation (achieve >90% mutation score)""",

"""**Debug Scenario:**
A React Testing Library test asserts on the text content of a formatted currency value. The test passes on the developer's macOS machine but fails on Linux CI:

```ts
expect(screen.getByTestId('total')).toHaveTextContent('$1,234.56');
// CI output: Expected "$1,234.56" → Received "$ 1 234,56"
```

Diagnose the `Intl.NumberFormat` locale sensitivity issue — `toLocaleString()` uses the OS locale, which differs between macOS (`en-US`) and Linux (`C` or `en_GB`). Show how to fix the formatter to always produce a specific locale, and how to detect locale-sensitive rendering issues in tests before they reach CI.""",

"""**Task (Code Generation):**
Implement a test coverage enforcement system for a monorepo with Turborepo:

```json
// Each package's vitest.config.ts enforces thresholds:
{
  "coverage": {
    "thresholds": { "statements": 80, "branches": 75, "functions": 80 }
  }
}
```

Show:
1. Per-package coverage thresholds in vitest config
2. A script that generates a monorepo-wide coverage report by merging per-package reports
3. A GitHub Actions check that blocks PRs if coverage drops below baseline
4. How to exclude generated files and test utilities from coverage counts

Show the `vitest.config.ts`, the merge script, and the CI workflow.""",

"""**Debug Scenario:**
A Playwright test that fills a form and checks validation messages fails because the error messages appear asynchronously with a 300ms debounce, but the test immediately asserts after `fill()`:

```ts
await page.fill('[name="email"]', 'bad-email');
// Error message appears 300ms later
await expect(page.locator('.error')).toBeVisible(); // fails immediately
```

Show advanced Playwright waiting: `expect.poll()` for repeated assertion retries, `waitForSelector` with custom timeouts, and how to configure Playwright's default assertion timeout globally. Also show how to test the negative case: that no error appears for a valid email.""",

]

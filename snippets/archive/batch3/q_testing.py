"""
snippets/q_testing.py — BATCH 3: 28 brand-new Testing questions
Zero overlap with batch1 or batch2 archives.
"""

Q_TESTING = [

"""**Task (Code Generation):**
Implement a custom React Testing Library `renderWithProviders` utility that wraps components with all global providers:

```ts
const { getByRole, user } = renderWithProviders(
  <UserProfile userId="1" />,
  {
    preloadedState: { auth: { user: mockUser } },
    queryClient: createTestQueryClient(),
    router: { pathname: '/profile/1' },
  }
);
```

Show: the wrapper with all providers (Redux, React Query, NextRouter mock, Theme), the `userEvent.setup()` integration, a factory for pre-configured test QueryClient (no retries, no cache time), and TypeScript generics for the `preloadedState` type derived from the Redux root state.""",

"""**Debug Scenario:**
A test for a form submit handler passes locally but fails flakily in CI:

```ts
test('submits form', async () => {
  render(<ContactForm />);
  await userEvent.type(screen.getByRole('textbox', { name: 'Email' }), 'test@example.com');
  await userEvent.click(screen.getByRole('button', { name: 'Submit' }));
  expect(screen.getByText('Thank you!')).toBeInTheDocument();
});
```

CI machines are slower and the async state update (after form submit API call) completes after the assertion. `getByText` doesn't wait for the element to appear. Show: replacing `getByText` with `findByText` (which returns a Promise and polls), the `waitFor` wrapper for complex async assertions, and setting `fakertimers: { now: Date.now() }` to fix time-dependent flakiness.""",

"""**Task (Code Generation):**
Build a `mockComponentTree` testing utility that replaces deep child components with test doubles:

```ts
const { mocks } = mockComponentTree(<UserDashboard />, {
  UserProfile: (props) => <div data-testid="mock-profile" data-user-id={props.userId} />,
  ActivityFeed: () => <div data-testid="mock-feed" />,
});

// Now test UserDashboard in isolation without real UserProfile/ActivityFeed
expect(screen.getByTestId('mock-profile')).toHaveAttribute('data-user-id', '123');
```

Show: the Jest `jest.mock()` factory pattern, the utility that auto-generates test IDs, how to capture props passed to mocked components for assertions, and why this is better than shallow rendering (tests actual DOM interactions).""",

"""**Debug Scenario:**
A Vitest test for an async hook times out after 5 seconds:

```ts
test('fetches user data', async () => {
  const { result } = renderHook(() => useUser('1'));
  await waitFor(() => expect(result.current.data).toBeDefined());
  // Timeout!
});
```

`useUser` calls `fetch()` which isn't mocked. In Vitest, `fetch` is not available by default (Node.js environment). Show: setting up MSW (Mock Service Worker) for Vitest with the `msw/node` server, the `beforeAll/afterAll/afterEach` setup in `vitest.setup.ts`, and configuring `globalThis.fetch` using `undici` as the polyfill for Node.js environments.""",

"""**Task (Code Generation):**
Implement a `createApiMockServer` factory using MSW 2.0 for integration tests:

```ts
const server = createApiMockServer({
  'GET /api/users': (req, res, ctx) => res(ctx.json(mockUsers)),
  'POST /api/users': async (req, res, ctx) => {
    const body = await req.json();
    return res(ctx.json({ ...body, id: 'new-id' }));
  },
  'GET /api/users/:id': (req, res, ctx) => {
    const { id } = req.params;
    const user = mockUsers.find(u => u.id === id);
    return user ? res(ctx.json(user)) : res(ctx.status(404));
  },
});

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

Show: MSW 2.0 handler syntax, per-test handler overrides with `server.use()`, error scenario simulation, and TypeScript types for handler config.""",

"""**Debug Scenario:**
End-to-end Playwright tests pass on CI's Linux environment but fail on a developer's Windows machine with:

```
Error: Cannot find element with locator: .nav-item >> text="Dashboard"
```

Investigation reveals the app uses CSS `text-transform: uppercase`. The text "Dashboard" is visually displayed as "DASHBOARD" on Windows (certain font rendering differences) but the DOM text content is "Dashboard". Playwright's `text=` locator matches DOM text, not CSS-rendered text.

Show: using `getByRole('link', { name: /dashboard/i })` (case-insensitive) instead of text locator, comparing `textContent` vs `innerText` when debugging, and writing a custom matcher that uses `getComputedStyle` to account for `text-transform`.""",

"""**Task (Code Generation):**
Build a `testFactory` pattern for generating typed test fixtures:

```ts
const userFactory = createFactory<User>({
  defaults: {
    id: () => crypto.randomUUID(),
    name: 'Alice Johnson',
    email: () => `user-${Date.now()}@example.com`,
    role: 'user',
    createdAt: () => new Date(),
  },
});

const admin = userFactory.build({ role: 'admin', name: 'Bob Admin' });
const users = userFactory.buildList(10);
const [alice, bob] = userFactory.buildList(2, [
  { name: 'Alice' },
  { name: 'Bob' },
]);
```

Show: the factory type inferring defaults from the type parameter, overrides merging, list generation, and a `create` method that persists to a test database.""",

"""**Debug Scenario:**
A React component test uses `jest.spyOn(console, 'error')` to suppress React's prop-type warnings but the spy leaks between tests because the `mockRestore()` isn't called in `afterEach`:

```ts
beforeEach(() => {
  jest.spyOn(console, 'error').mockImplementation(() => {});
});
// Missing: afterEach(() => jest.restoreAllMocks());
```

Show: the correct setup/teardown, using `jest.restoreAllMocks()` in `afterEach` to prevent cross-test pollution, configuring Jest's `restoreMocks: true` in `jest.config.js` for automatic restoration, and why `mockReset()` vs `mockRestore()` vs `mockClear()` differ (clears calls / resets implementation / restores original).""",

"""**Task (Code Generation):**
Implement a snapshot testing utility for design system components that catches visual regressions:

```ts
// Generates stable snapshots with semantic selectors:
const tree = renderToSnapshot(<Button variant="primary" size="lg">Click me</Button>, {
  excludeProps: ['onClick', 'style'],   // ignore ephemeral props
  normalizeClassNames: true,            // sort classes alphabetically
  prettify: true,                       // format HTML
});

expect(tree).toMatchSnapshot();
```

Show: the custom serializer that excludes volatile props, class name normalization (CSS Modules generate hash-based names), integration with Storybook's `storyshots` addon, and the workflow for updating snapshots after intentional changes.""",

"""**Debug Scenario:**
An accessibility test using `jest-axe` reports no violations but users with screen readers report that a modal is inaccessible. The test is:

```ts
const { container } = render(<Modal isOpen={false} />);
const results = await axe(container);
expect(results).toHaveNoViolations();
```

The modal is tested while closed (`isOpen={false}`). Open-state accessibility violations (missing `aria-modal`, `role="dialog"`, focus management) are never checked. Show: testing the modal in its open state, using `userEvent.click` to open the modal before axe analysis, and the full set of modal accessibility requirements per WCAG (focus trap, `aria-labelledby`, `aria-describedby`, escape key handling).""",

"""**Task (Code Generation):**
Build a `contractTest` utility for API contract testing between a React app and its backend:

```ts
// Client declares what it expects:
contractTest('GET /api/user/:id', {
  request: { params: { id: '123' } },
  response: {
    status: 200,
    body: z.object({
      id: z.string(),
      name: z.string(),
      email: z.string().email(),
    }),
  },
});

// Runs against real API in CI and generates a pact file for backend validation
```

Show: Zod schema validation of real API responses, Pact library integration for consumer-driven contract testing, and the CI workflow that breaks the build if the API violates the contract.""",

"""**Debug Scenario:**
A Playwright test that navigates between two pages occasionally fails with "Context was destroyed, most likely trying to navigate while an older test is still loading":

```ts
test('navigates to profile', async ({ page }) => {
  await page.goto('/dashboard');
  await page.click('[data-testid="profile-link"]');
  await expect(page).toHaveURL('/profile');
});
```

The test suite runs tests in parallel — another test navigates the same page. Show: proper page isolation (each test should use a fresh `page` fixture), the `browser.newPage()` pattern for parallel isolation, configuring `workers: 1` for sequential (safe but slow), and `test.describe.serial` for sequencing related tests without disabling parallelism globally.""",

"""**Task (Code Generation):**
Implement a `testPerformance` utility that asserts React component render count:

```ts
const counter = renderWithRenderCounter(<ProductList products={mockProducts} />);

// Simulate filtering:
await userEvent.type(screen.getByRole('searchbox'), 'laptop');

expect(counter.renderCount).toBeLessThan(5); // should not over-render
expect(counter.lastRenderDuration).toBeLessThan(16); // under 1 frame
```

Show: using React's `Profiler` component to count renders and measure duration, a custom `renderWithRenderCounter` that wraps RTL's `render` with profiling, and why `React.StrictMode` doubles render counts (and how to account for it in assertions).""",

"""**Debug Scenario:**
A component test is asserting on text content, but the assertion keeps failing due to whitespace differences between the rendered HTML and the expected string:

```ts
expect(screen.getByRole('heading')).toHaveTextContent('Total: $1,234.56');
// Element text: 'Total:  $1,234.56' (double space from CSS layout)
```

`toHaveTextContent` uses `textContent` which includes all whitespace. Show: the `normalizeWhitespace: true` option in `toHaveTextContent`, using `getByRole` with `name` option which normalizes whitespace for ARIA accessible name computation, and the difference between `textContent`, `innerText`, and `innerHTML` for testing text assertions.""",

"""**Task (Code Generation):**
Build a visual regression testing system using Playwright screenshots with pixel-diff:

```ts
test('renders dashboard correctly', async ({ page }) => {
  await page.goto('/dashboard?seed=123'); // deterministic data
  await page.waitForLoadState('networkidle');
  
  // Mask dynamic elements:
  await expect(page).toHaveScreenshot('dashboard.png', {
    mask: [page.locator('.current-time'), page.locator('.live-chart')],
    threshold: 0.01, // 1% pixel difference threshold
    animations: 'disabled',
  });
});
```

Show: the Playwright screenshot comparison setup, CI vs local baseline management (baselines committed to git), a GitHub Actions workflow that uploads diff images as artifacts on failure, and handling dynamic content (dates, random data) with fixed seeds or masking.""",

"""**Debug Scenario:**
A test for a `useLocalStorage` hook fails in Jest because `localStorage` is not available:

```ts
test('persists to localStorage', () => {
  const { result } = renderHook(() => useLocalStorage('key', 'default'));
  act(() => result.current[1]('new-value'));
  expect(result.current[0]).toBe('new-value');
  expect(localStorage.getItem('key')).toBe('"new-value"'); // localStorage is not defined
});
```

Jest's default JSDOM environment does include `localStorage`, but the test environment is set to `node` in `jest.config.ts`. Show: setting `testEnvironment: 'jsdom'` globally, using `@jest-environment jsdom` docblock per file, mocking localStorage with `jest.spyOn(Storage.prototype, 'getItem')`, and the `localStorage` mock object pattern for full control.""",

"""**Task (Code Generation):**
Implement a `testDataBuilder` for domain-driven test data that reads naturally:

```ts
const order = aBuilder()
  .anOrder()
    .withStatus('pending')
    .withItems([
      anItem().withName('Laptop').withPrice(999).build(),
      anItem().withName('Mouse').withPrice(29).build(),
    ])
    .withCustomer(aCustomer().withEmail('alice@example.com').build())
  .build();
```

Show: the fluent builder TypeScript implementation, how builders compose (order contains items and customer), the `build()` method that validates required fields, and integration with Zod schemas for runtime validation of built objects.""",

"""**Debug Scenario:**
A React context test fails because the component under test reads from a context but the test doesn't provide it, causing the component to use the context's default value instead of the mocked value:

```ts
// UserContext default: { user: null }
test('shows user name', () => {
  render(<UserHeader />);
  expect(screen.getByText('Alice')).toBeInTheDocument(); // fails: uses default null
});
```

The test is missing the Provider. Show: wrapping with the Provider in `render(<UserContext.Provider value={{ user: mockUser }}><UserHeader /></UserContext.Provider>)`, extracting this to a `renderWithContext` utility, and using RTL's `wrapper` option in `renderHook` for context-dependent hooks.""",

"""**Task (Code Generation):**
Build a `waitForAnimations` testing utility for Framer Motion components:

```ts
const { getByTestId } = render(<AnimatedModal isOpen={true} />);
await waitForAnimations(); // waits for all Framer Motion animations to complete

expect(getByTestId('modal')).toHaveStyle({ opacity: '1', transform: 'scale(1)' });
```

Show: mocking Framer Motion's `animate` with `jest.mock('framer-motion')` to skip animations in tests, using `MotionConfig` with `reducedMotion="always"` in the test wrapper to disable animations, and the `act` + `jest.runAllTimers()` pattern for animation-complete assertions. Discuss tradeoffs between each approach.""",

"""**Debug Scenario:**
A Storybook interaction test using `play` function fails with a timeout when clicking a button that triggers an async action:

```ts
export const Default: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button', { name: 'Save' }));
    await expect(canvas.getByText('Saved!')).toBeInTheDocument(); // timeout
  },
};
```

The `getByText` assertion doesn't wait for the 'Saved!' text to appear. Show: using `findByText` (async query with built-in polling), `waitFor` from `@storybook/test`, and configuring the `play` function's timeout via `parameters.chromatic.delay`. Also show how to mock API calls in Storybook using MSW's `mswLoader`.""",

"""**Task (Code Generation):**
Implement property-based testing for a data validation utility using `fast-check`:

```ts
import fc from 'fast-check';

test('parseCurrency always returns a number or throws', () => {
  fc.assert(fc.property(
    fc.string(),
    (input) => {
      try {
        const result = parseCurrency(input);
        expect(typeof result).toBe('number');
        expect(Number.isFinite(result)).toBe(true);
      } catch (e) {
        expect(e).toBeInstanceOf(CurrencyParseError);
      }
    }
  ));
});
```

Show: `fc.string()`, `fc.float()`, `fc.integer()` generators, custom arbitraries for domain types (e.g., `fc.emailAddress()`), shrinking examples on failure, and applying property-based testing to a React reducer (properties: state is always valid, actions are idempotent).""",

"""**Debug Scenario:**
A React Testing Library test clicks a button that opens a dialog, then checks for dialog content. The test fails with "Unable to find role=dialog":

```ts
await userEvent.click(screen.getByRole('button', { name: 'Open Settings' }));
expect(screen.getByRole('dialog')).toBeInTheDocument();
```

The dialog renders in a React Portal, outside the `render()` container. RTL's `screen.getByRole` queries the entire document body (including portals) by default — so portals should be findable. The real issue is that the dialog has `role="presentation"` instead of `role="dialog"`.

Show: debugging element roles using `screen.debug()`, `aria-query` library for ARIA role lookup, and the accessible markup that makes a dialog findable with `getByRole('dialog')` (requires `role="dialog"` + `aria-labelledby` or `aria-label`).""",

"""**Task (Code Generation):**
Build a mutation testing workflow to measure test suite quality:

```bash
# Runs Stryker on the utils/ directory:
npx stryker run --mutate "src/utils/**/*.ts" --testRunner jest
```

Show: configuring `stryker.config.mjs` for a React/TypeScript project, understanding mutation score (percentage of mutants killed by tests), adding targeted tests for surviving mutants (boundary conditions, null checks), and integrating the mutation score threshold into CI (`--minMutationScore 80`).""",

"""**Debug Scenario:**
A test suite has 500 tests and takes 8 minutes to run in CI. `jest --watch` is fast locally, but full CI runs are slow. Analysis shows 80% of the time is spent in 20 integration tests that make real database queries.

Show: separating unit and integration tests with Jest projects config (`testPathPattern` per project), running unit tests on every commit and integration tests nightly or on `main`, using `--shard=1/4` for parallel sharding across 4 CI machines, and `--bail` to fail fast on first test failure in PR checks.""",

"""**Task (Code Generation):**
Implement a `recordNetworkRequests` test utility for asserting API call sequences:

```ts
const recorder = recordNetworkRequests([
  { url: '/api/users', method: 'GET', response: mockUsers },
  { url: '/api/users/1', method: 'PATCH', response: updatedUser },
]);

// Interact with component:
await userEvent.click(screen.getByRole('button', { name: 'Update User' }));

// Assert request sequence:
recorder.assertCalled('GET /api/users');
recorder.assertCalledWith('PATCH /api/users/1', { body: { name: 'New Name' } });
recorder.assertCallCount('GET /api/users', 1); // called exactly once
recorder.assertNotCalled('DELETE /api/users/1');
```

Show: MSW handler setup, request capture, and the assertion API.""",

"""**Debug Scenario:**
A component test for a rich text editor fails because `contenteditable` elements don't support `userEvent.type`:

```ts
const editor = screen.getByRole('textbox'); // contenteditable div
await userEvent.type(editor, 'Hello world');
expect(editor).toHaveTextContent('Hello world'); // fails: no text added
```

`userEvent.type` dispatches keyboard events but `contenteditable` elements rely on `beforeinput` and `input` events with `InputEvent.data` for text insertion, not `keypress` alone. Show: using `userEvent.setup()` with clipboard option for paste-based input, directly setting `innerHTML` + firing `input` event for unit tests, and Playwright (which handles `contenteditable` correctly) for E2E tests.""",

"""**Task (Code Generation):**
Build a `testCoverage` badge generator that creates an SVG coverage badge from Istanbul's output:

```ts
// Runs after jest --coverage:
const { statements, branches, functions, lines } = parseCoverageReport('./coverage/coverage-summary.json');

generateBadge({
  label: 'coverage',
  message: `${lines.pct}%`,
  color: lines.pct >= 80 ? 'brightgreen' : lines.pct >= 60 ? 'yellow' : 'red',
  outputPath: './coverage/badge.svg',
});
```

Show: parsing `coverage-summary.json`, the SVG badge template with `foreignObject` for text, the color thresholds, writing to file, and integrating into CI to update the badge in the README via the GitHub API.""",

"""**Debug Scenario:**
A Next.js API Route test using `node-mocks-http` fails because the mock response doesn't support streaming:

```ts
const { req, res } = createMocks({ method: 'GET' });
await GET(req as NextRequest); // Returns ReadableStream
res._getJSONData(); // Error: response was streamed, cannot get JSON
```

Modern Next.js App Router Route Handlers return `Response` objects with streaming support, not classic `res.json()`. Show: using `fetch()` with `unstable_httpHandler` (Next.js testing), the `Response` mock that captures streamed body, and using `supertest` with a running Next.js dev server for integration testing Route Handlers.""",

]

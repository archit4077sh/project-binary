"""
snippets/q_testing.py - 28 Testing questions
"""

Q_TESTING = [

"""**Context:**
We write unit tests for our React components using React Testing Library (RTL) and Jest. A test for our DataTable component is flaky -- it passes locally but fails in CI with "Unable to find an element with the role 'row'."

**Observed Issue:**
The test queries by ARIA role immediately after render, but the DataTable fetches data asynchronously. The rows are not in the DOM yet when the assertion runs.

**Specific Ask:**
What's the RTL pattern for waiting on async renders after a data fetch? Should we use findBy queries (which return Promises and wait up to timeout), waitFor wrappers, or mock the fetch to return synchronously? And should we prefer mocking fetch/axios or using MSW (Mock Service Worker) for a component with multiple internal fetches?""",

"""**Context:**
We use MSW (Mock Service Worker) to mock API responses in our RTL tests. A test for the report creation form passes in isolation but fails when run alongside other tests.

**Observed Issue:**
MSW handlers set up in one test's beforeEach are leaking into subsequent tests. The handler registered for POST /api/reports in Test A persists into Test B, overriding Test B's handler.

**Specific Ask:**
What's the correct MSW handler lifecycle for Jest test suites? Should server.resetHandlers() be called in afterEach to clear per-test overrides? And what's the difference between setting handlers in server.use() (test-specific, reset with resetHandlers) vs. in the handlers array (global, always active)?""",

"""**Context:**
We want to write tests that verify the DataTable correctly handles 10,000 rows with virtualization. The virtualization library only renders visible rows.

**Observed Issue:**
RTL queries (getAllByRole('row')) only find DOM-present elements. With virtualization, only 30 rows are rendered. Our tests can't verify row 5,000 without scrolling programmatically, which RTL's DOM simulation doesn't support natively.

**Specific Ask:**
How do you test a virtualized list's correctness when RTL can only query rendered elements? Is the correct approach to test the virtualization library separately from your business logic (which rows to show), using a Playwright/Cypress e2e test for the scroll behavior, and RTL only for non-virtualized unit concerns?""",

"""**Context:**
We're adding Playwright e2e tests for our dashboard's authentication flow. The tests need to log in first, then navigate to the authenticated area.

**Observed Issue:**
Logging in via the UI for every test takes 3-5 seconds per test (network to auth API, session cookie set). With 50 tests requiring auth, the e2e suite takes 4+ minutes just for login flows.

**Specific Ask:**
What's the Playwright pattern for reusing authenticated state across tests to avoid repeated login flows? Is storageState (save session to a file, restore in subsequent tests' contexts) the correct approach? And what are the risks of sharing a single auth session across parallel test workers -- does Playwright's test isolation still hold?""",

"""**Context:**
We have a Playwright test that clicks a button and expects a toast notification to appear, then disappear. The toast has a 3-second auto-dismiss.

**Observed Issue:**
When running in CI with Playwright's parallel execution, the test is flaky. The toast sometimes disappears before the assertion runs because the auto-dismiss timer fires faster on the CI server than locally.

**Specific Ask:**
How do you make time-dependent UI tests (auto-dismiss, polling intervals) deterministic in Playwright? Should tests mock timers (page.clock.install() in Playwright 1.45+) or extend timeouts? What's Playwright's recommendation for testing elements with CSS animations that add to dismiss timing?""",

"""**Context:**
We want visual regression tests for our design system Storybook stories. Running a screenshot diff after every PR catches unintended UI changes.

**Observed Issue:**
Our current Playwright screenshot tests have a 2-3% pixel difference tolerance because of font rendering differences between developers' Macs and the CI Linux runner. This tolerance is wide enough to miss genuine regressions.

**Specific Ask:**
What's the standard practice for eliminating font rendering differences in visual regression tests between macOS dev machines and Linux CI runners? Is running Playwright in a Docker container with the same rendering stack the fix? And what tools (Argos, Chromatic, Percy) handle the screenshot diff infrastructure better than rolling our own Playwright screenshot comparison?""",

"""**Context:**
We're testing a custom React hook (useReportFilter) that manages complex filter state. The hook internally calls a debounced API fetch.

**Observed Issue:**
Tests using renderHook from RTL pass, but the debounced fetch complicates assertions. act() warnings appear and sometimes the fetch mock is called 0 times, sometimes 1 time depending on test execution speed.

**Specific Ask:**
How do you test React hooks that contain debounced async operations deterministically? Should we use Jest's fake timers (jest.useFakeTimers()) + act(jest.runAllTimers()) to advance past the debounce? And how does this interact with RTL's act() wrapper, which also manages async state updates?""",

"""**Context:**
We want 100% statement coverage for our utility functions. Our coverage report shows 94% and we're trying to identify which branches are uncovered.

**Observed Issue:**
Jest's coverage report (--coverage) shows which lines are uncovered but not why a branch wasn't taken. We have a complex parseFilterExpression function with 12 conditional branches and we can't identify which input would exercise the missing branch.

**Specific Ask:**
How do you use Jest's branch coverage (B column in the coverage report) to identify which specific conditions are untested? Is there a V8-based coverage reporter that shows which branch of a ternary is uncovered (unlike Istanbul which only shows line coverage)? And is 100% branch coverage a realistic goal for a complex parser, or does it produce low-value tests that test internal implementation?""",

"""**Context:**
We test our Next.js Server Actions with Jest. A Server Action validates form input and writes to the database.

**Observed Issue:**
Running Server Actions in Jest requires mocking the Next.js request context (cookies, headers) which are accessed via next/headers. The server action imports from next/headers, which is not available in the Jest/Node.js test environment.

**Specific Ask:**
What's the strategy for unit testing Next.js Server Actions that depend on next/headers or next/cache? Should we abstract the header/cookie access into a wrapper and mock the wrapper, or set up a Next.js test server and call actions via HTTP? Is there an official Next.js approach for testing Server Actions?""",

"""**Context:**
We added Zod schema validation to our API routes. We want to test that invalid input returns 422 with specific error messages, not just that the route throws.

**Observed Issue:**
In Jest, we test the route handler directly by calling the function with a mocked NextRequest. But the response from the handler is a NextResponse object, and accessing the JSON body requires calling await response.json() which is async.

**Specific Ask:**
What's the correct testing pattern for Next.js 14 App Router API Route Handlers (route.ts) in Jest? How do you correctly mock NextRequest with a body, and how do you read the NextResponse body in an assertion? Is using supertest against a running Next.js server easier for route testing than mocking NextRequest?""",

"""**Context:**
We have a component test for our ThemeToggle component. The component reads theme from a React Context and the test needs to provide the Context.

**Observed Issue:**
We wrap each test with <ThemeProvider>. But ThemeProvider has a side effect: reading localStorage on mount. This causes a "localStorage is not defined" error because RTL runs in jsdom which doesn't have localStorage by default.

**Specific Ask:**
What's the correct approach to test a component that has Context dependencies with side effects (localStorage, fetch)? Is the fix to mock localStorage in Jest's setupFiles, add a jsdom-based localStorage polyfill, or mock the ThemeProvider itself? What's the tradeoff between testing with a real provider (integration) vs. mocking the context value directly?""",

"""**Context:**
We use Storybook for component development and documentation. We want to integrate accessibility testing into Storybook so a11y violations are visible in component development, not just at audit time.

**Observed Issue:**
We've added @storybook/addon-a11y. It runs axe-core on the rendered story. But the addon only runs when the story is viewed -- there's no CI enforcement and developers often ignore the badge.

**Specific Ask:**
How do you enforce a11y requirements in CI using Storybook? Can you run all Storybook stories through axe-core headlessly in CI using Storybook Test Runner + axe integration? What types of violations does automated axe-core testing catch reliably vs. what requires manual testing?""",

"""**Context:**
We're writing tests for a component that renders a large list of items with infinite scroll. The test using RTL verifies that the 51st item loads when the user scrolls to the bottom.

**Observed Issue:**
RTL tests run in jsdom which doesn't support actual scrolling or IntersectionObserver (used for the scroll sentinel). The IntersectionObserver is undefined in jsdom, causing the component to throw.

**Specific Ask:**
How do you test IntersectionObserver-based infinite scroll in RTL/jsdom? Is polyfilling IntersectionObserver in Jest setupFiles the right approach, or should you mock IntersectionObserver and programmatically trigger its callback? What's the argument for moving this kind of test to Playwright instead of RTL?""",

"""**Context:**
Our RTL tests mock useRouter() from next/navigation for components that use the router for navigation. After upgrading Next.js from 13 to 14, the mock started failing with "Cannot read properties of undefined (reading 'push')."

**Observed Issue:**
In Next.js 14, useRouter from next/navigation returns a different object shape, and some internals changed. Our blanket jest.mock('next/navigation', ...) overrides all exports, including ones we didn't intend to mock.

**Specific Ask:**
What's the correct way to mock next/navigation (useRouter, useSearchParams, usePathname) in RTL tests for Next.js 14? Is jest.requireActual('next/navigation') combined with partial override the right approach? Is there an official or community testing utility for Next.js navigation mocking (like next-router-mock) that stays in sync with Next.js versions?""",

"""**Context:**
We want to test our Zustand store independently -- not through components but as a pure state machine test.

**Observed Issue:**
Tests that directly call store actions work in isolation. But tests share the store instance between test cases because Zustand creates a module-level store. State from Test A persists into Test B.

**Specific Ask:**
How do you reset Zustand store state between tests? Is the correct pattern to export a resetStore function, or use the Zustand devtools middleware's ability to reset to initial state? And should Zustand stores be tested directly (testing state transitions) or only through components (testing behavior)?""",

"""**Context:**
We're testing a complex async workflow: submit form → optimistic update → API call → success route redirect. This spans multiple components in a realistic integration test.

**Observed Issue:**
RTL renders one component at a time. The redirect navigates to a different "page" component. RTL can't handle route transitions between different component trees.

**Specific Ask:**
Is Playwright (full browser, real routing) the right tool for testing workflows that span multiple pages? Or can you mock next/navigation's redirect in RTL to simulate the redirect and then render the destination component? What's the line between RTL integration tests and Playwright e2e tests for a Next.js app?""",

"""**Context:**
We have a custom fetch wrapper that adds auth headers and retries on 401 (with token refresh). We need to test the retry logic.

**Observed Issue:**
With MSW, we can simulate a 401 response followed by a 200 response. But the test needs to verify that the retry only happens once (not infinite), that the token refresh is called between requests, and that the original failed request is retried with the new token.

**Specific Ask:**
How do you sequence multiple MSW responses to the same endpoint (first call returns 401, second returns 200) for testing retry logic? Is the correct approach an MSW response array, or using a call counter in the handler? And how do you assert that specifically the token refresh endpoint was called between the two requests?""",

"""**Context:**
We want to test our rate limiting logic in our Next.js API routes. Requests exceeding the limit should return 429.

**Observed Issue:**
Rate limiting is implemented using an in-memory Map that counts requests per IP in a sliding window. In Jest tests, the in-memory state persists between test cases in the same module.

**Specific Ask:**
How do you test rate limiting logic that uses module-level state (the Map persists between tests)? Is jest.resetModules() between tests the right fix, or should the rate limiter be designed with a factory pattern (accepts an external store) to allow test injection? And how do you test the sliding window decay correctly without time manipulation?""",

"""**Context:**
We have a component that renders 200 items in a flat list. Our RTL test renders the full list and runs queries on it. The test takes 8 seconds to run.

**Observed Issue:**
RTL queries (getAllByRole) on 200 items are slow because they perform a full DOM search. Rendering 200 items in jsdom is also expensive.

**Specific Ask:**
Is the test slow because of DOM rendering, RTL query performance, or both? How do you profile a slow RTL test to find the bottleneck? Should you limit the test scope (render only 10 items for unit tests, use Playwright for full-list behavior), or is there a more performant RTL query pattern?""",

"""**Context:**
A property-based test (using fast-check) for our parseFilterExpression utility found an edge case: passing an expression with 10,000 nested parentheses causes a stack overflow.

**Observed Issue:**
Our recursive parser has no depth limit. Legitimate user input never exceeds 10 levels of nesting, but the parser is now exposed to intentional abuse (malicious input from an API endpoint).

**Specific Ask:**
When property-based testing reveals an edge case (stack overflow from adversarial input), what's the correct fix: add a recursion depth limit, rewrite the parser to use an iterative stack, or reject inputs that exceed a practical nesting limit at the API boundary? And how do you add the depth-limit constraint to the property-based test to verify the fix?""",

"""**Context:**
We're measuring code coverage for our RTL tests and find that our conditional rendering branches (show empty state when no results, error state on API failure) are uncovered.

**Observed Issue:**
Most tests mock the API to return successful data. The error and empty state branches are never exercised because the MSW handlers always return 200 with data.

**Specific Ask:**
What's the structure for a test file that covers all rendering states (loading, empty, error, populated) for a data-driven component? Should each state be its own describe block with its own MSW handler override? Is there a test pattern (parameterized tests with jest.each) that systematically ensures all states are tested?""",

"""**Context:**
We added Playwright tests for mobile viewport (375x812) alongside our desktop tests. The mobile tests run separately but share the same page fixture.

**Observed Issue:**
In our CI matrix, desktop and mobile tests run in parallel. A shared base URL is used for both, but the Next.js dev server starts once. When both test suites run simultaneously, they cause intermittent failures because of shared server state (sessions, test data).

**Specific Ask:**
How do you isolate Playwright test suites that run in parallel against the same development server? Is each test creating its own authenticated session (storageState per worker) sufficient isolation? Or should the test data (reports, users) also be isolated per test worker to prevent cross-test data pollution?""",

"""**Context:**
Our dashboard has a keyboard-navigable command palette. Pressing Ctrl+K opens it, and arrows/enter navigate/select. We have a Playwright test for this flow.

**Observed Issue:**
The test uses page.keyboard.press('Control+K') to open the palette. In some CI runs, the palette opens but the ArrowDown press doesn't move the selection highlight -- it seems focus is on the page, not the palette input.

**Specific Ask:**
How do you reliably test keyboard-driven focus flows in Playwright where focus state is critical? Is it safer to explicitly click the palette's input after opening it, or wait for a locator that indicates the input is focused (locator.isFocused())? What's Playwright's approach to ensuring keyboard interactions target the correct focused element?""",

"""**Context:**
We have a React Error Boundary that catches render errors and shows a fallback UI. We want to test that the fallback renders correctly when a child throws.

**Observed Issue:**
When a child component throws in a test, React logs the error to console.error even when correctly handled by an Error Boundary. Our CI runs fail on any unexpected console.error output.

**Specific Ask:**
How do you test Error Boundary behavior in RTL without triggering console.error noise? Is the correct approach to mock console.error at the start of the test (jest.spyOn(console, 'error').mockImplementation(() => {})? and restore after? What does RTL's official docs say about testing error boundaries?""",

"""**Context:**
We're adding contract tests between our Next.js frontend and the backend API. The contract tests verify that the frontend relies only on agreed-upon API shapes, so backend changes that break the contract fail CI.

**Observed Issue:**
We've explored Pact for consumer-driven contract testing. Running Pact requires a Pact Broker and a complex CI integration. Our team is unsure if the full Pact setup is worth it for an API we control end-to-end.

**Specific Ask:**
When is consumer-driven contract testing (Pact) overkill vs. the right tool? For a single company owning both frontend and backend, is snapshot testing the API response shape in RTL tests sufficient contract coverage? What's the tradeoff between Pact (formal contract with broker) and JSON schema validation (lightweight, no broker) for internal API contract testing?""",

"""**Context:**
We write Playwright tests that authenticate via a real login API. We discovered that running 20 parallel test workers causes 429 rate limit responses from our auth service during CI.

**Observed Issue:**
Parallel Playwright workers all try to authenticate simultaneously at test startup. The auth service rate limits by IP and our CI runner has one IP, so ~15 workers fail to authenticate.

**Specific Ask:**
What's the architecture for Playwright authentication that scales to 20+ parallel workers without rate-limiting the auth service? Is the global setup pattern (one login before all tests, save auth state to a file) the standard fix? And how do you handle the case where different tests need different user roles (admin vs. viewer)?""",

"""**Context:**
We're adding mutation testing to our test suite using Stryker. The first run shows a mutation score of 52% -- nearly half of code mutations survive (aren't detected by tests).

**Observed Issue:**
The surviving mutations are mostly in our conditional branches: changing > to >=, replacing && with ||, and removing return statements. Our tests don't verify behavior precisely enough to catch these mutations.

**Specific Ask:**
How do you interpret a low mutation score and prioritize which tests to improve first? Is the goal 100% mutation score for every module, or is there a diminishing-returns threshold (80%?) beyond which the test quality gain doesn't justify the effort? What types of test additions improve mutation score most efficiently -- boundary value tests, state transition tests, or error case tests?""",

"""**Context:**
We want to add performance regression tests that verify our key dashboard pages render within budget. The test should fail CI if First Contentful Paint exceeds 1.5s.

**Observed Issue:**
Playwright's performance API (page.metrics()) returns navigation timing data. But in CI, performance numbers vary by 30-40% between runs due to VM resource contention, making fixed-threshold tests flaky.

**Specific Ask:**
How do you write stable performance regression tests in CI where absolute numbers are noisy? Is the correct approach a percentage-of-baseline comparison (current run must be within 20% of a recorded baseline) rather than a fixed threshold? What tools (WebPageTest CLI, Lighthouse CI, Playwright Trace Viewer) give the most stable, comparable performance measurements across CI runs?""",

]

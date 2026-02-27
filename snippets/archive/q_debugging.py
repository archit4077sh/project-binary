"""
snippets/q_debugging.py - 28 Debugging questions
"""

Q_DEBUGGING = [

"""**Context:**
A dashboard component fetches report data based on a reportId prop. We noticed that rapidly clicking between reports sometimes shows data from a previous report for 1-2 seconds.

**Code:**
```ts
useEffect(() => {
  fetchReport(reportId).then(data => setReport(data));
}, [reportId]);
```

**Observed Issue:**
Two concurrent fetches -- one for the old reportId, one for the new -- can both resolve. If the slower old fetch resolves after the faster new fetch, setReport is called with stale data.

**Specific Ask:**
What's the idiomatic React pattern for canceling or ignoring stale async fetches when a dependency changes? For fetch-based requests, AbortController is clean -- but what about third-party SDK calls that aren't cancellable? Is the ignore flag pattern (let cancelled = false) safe in React 18 concurrent mode?""",

"""**Context:**
We have a search input that debounces API calls. The debounced handler captures the filter state at the time of creation.

**Code:**
```ts
const search = useCallback(
  debounce(() => {
    api.search(filter); // filter is stale here
  }, 400),
  [] // empty deps
);
```

**Observed Issue:**
filter always has the value from the first render. Typing quickly results in all searches using the initial empty filter, not the current one.

**Specific Ask:**
What's the clean solution for a debounced function that needs to read the latest reactive state? The useRef(filter) pattern (store latest in a ref, read in the debounce) is common -- but does it have any gotchas in React 18 concurrent mode where the ref might be read across different render lanes?""",

"""**Context:**
After refactoring our filters to use a Zustand store, a component that reads from the store is stuck in an infinite render loop.

**Observed Issue:**
The Zustand selector returns a new object reference on every render. The component reads this object, which triggers a useMemo that depends on it, which triggers another state update, which triggers a re-render.

**Specific Ask:**
How do you debug a Zustand-triggered infinite render loop? What DevTools or console patterns let you identify: (1) which exact state value is changing, (2) which selector is returning an unstable reference, and (3) which downstream hook is turning that into the circular update?""",

"""**Context:**
Our useActivityTracker hook attaches a mousemove listener on mount for idle detection. The hook is used in 12 components.

**Code:**
```ts
useEffect(() => {
  window.addEventListener('mousemove', handleActivity);
  // cleanup missing
}, []);
```

**Observed Issue:**
After 10 minutes of navigation, Memory Profiler shows 1,200 active 'mousemove' listeners. Each component re-mount adds new listeners without removing old ones.

**Specific Ask:**
Beyond fixing the obvious cleanup: how do you reliably detect this class of accumulating listener leak during development before it reaches production? Is there a ResizeObserver-style mechanism that automatically disconnects? What Chrome DevTools workflow catches this in a 5-minute audit?""",

"""**Context:**
Our dashboard connects to a WebSocket feed. When users navigate away and back, the WebSocket cleanup in useEffect sometimes doesn't fire.

**Observed Issue:**
React 18 StrictMode double-invokes effects. The first cleanup closes the socket, the second setup opens a new one. But in production (non-StrictMode), we occasionally see stale socket connections from navigated-away pages still receiving messages and calling setState on unmounted components.

**Specific Ask:**
Why would WebSocket cleanup in useEffect not reliably fire in production? Is this related to React 18's concurrent rendering batching unmounts? How do you make a WebSocket hook bulletproof against concurrent navigation patterns?""",

"""**Context:**
A polling mechanism uses setInterval to refresh dashboard metrics every 30 seconds. After a few hours, memory usage climbs and the polling frequency increases.

**Code:**
```ts
useEffect(() => {
  const id = setInterval(refresh, 30000);
  return () => clearInterval(id); // correctly returns cleanup
}, [refresh]);
```

**Observed Issue:**
refresh is not stable (recreated each render), causing the effect to re-run. Each effect re-run sets a new interval while the previous one may not have been cleared before registration.

**Specific Ask:**
How does useEffect cleanup interact with re-runs when a dependency changes? Is the cleanup always called before the next effect runs? In this specific case, would useRef(refresh) + useLatest pattern solve the re-registration? Or is there a race between cleanup and re-setup at the scheduler level?""",

"""**Context:**
A Server Action wraps a database call in a try/catch and logs errors. In production, some mutations are silently failing with no user feedback.

**Code:**
```ts
async function updateReport(formData: FormData) {
  try {
    await db.reports.update(parse(formData));
  } catch (e) {
    console.error('update failed', e); // error is swallowed
  }
}
```

**Observed Issue:**
The error is caught and logged but not re-thrown or returned. The Server Action returns undefined to the client, which interprets it as success.

**Specific Ask:**
What's the correct error propagation pattern in Next.js Server Actions so silent failures are impossible? Should errors always be returned as typed discriminated unions rather than thrown? And how do you distinguish between "user error" (validation failure, should return to form) vs "system error" (DB failure, should trigger error.tsx)?""",

"""**Context:**
After a route change in our dashboard, some components that have been unmounted still call setState when their pending fetch resolves.

**Observed Issue:**
We get the warning: "Can't perform a React state update on an unmounted component." This doesn't crash the app but suggests memory leaks. We thought React 18 removed this warning.

**Specific Ask:**
Did React 18 remove the "setState on unmounted component" warning? If yes, why might we still see it? Is this coming from a third-party library using an older React version? And regardless of the warning, does setting state on an unmounted component cause an actual memory leak in React 18's memory model?""",

"""**Context:**
We have a list where each item has type: 'user' | 'team'. We render different components based on type with the same numeric key.

**Code:**
```tsx
{items.map(item => (
  <div key={item.id}>
    {item.type === 'user' ? <UserCard data={item} /> : <TeamCard data={item} />}
  </div>
))}
```

**Observed Issue:**
When an item changes from type 'user' to 'team' (after an update), the component doesn't unmount/remount -- React reuses the existing component instance and the TeamCard receives props meant for UserCard.

**Specific Ask:**
Even with proper div keys, why would React reuse the wrong component type in a conditional render? Is this because both UserCard and TeamCard are at the same position in the tree? Should the key be moved to the inner component, or should we add a type-specific key like key={`${item.type}-${item.id}`}?""",

"""**Context:**
Our dashboard fetches data from a GraphQL API. A specific panel intermittently shows no data even though the network tab shows the query returning a response.

**Observed Issue:**
The GraphQL response has both a data field (with partial results) AND an errors array. Our GraphQL client (Apollo) considers this a partial success and returns data without throwing. The UI reads data and renders, never seeing the errors array.

**Specific Ask:**
How do you correctly handle GraphQL partial errors (response has both data and errors)? Should error handling check both the Apollo error state AND inspect the data for null fields that indicate a partial failure? What's the pattern in Apollo Client for treating any errors in the errors array as a failure state?""",

"""**Context:**
Our Next.js API route calls an external service. In development, some requests fail with a CORS error even though the external service has CORS headers configured.

**Observed Issue:**
The CORS error appears in the browser DevTools Network tab. But the request is from a Next.js API route (server-side), so CORS shouldn't apply -- servers making server-to-server requests don't have CORS restrictions.

**Specific Ask:**
If a Next.js API route is making a server-side fetch, why would CORS appear as the error? Is the browser somehow making the fetch directly (e.g., the API route is actually a client-side fetch)? How do you definitively verify whether a fetch is happening server-side vs. client-side in a Next.js component?""",

"""**Context:**
Our dashboard sends authentication cookies with requests to our API. In production, API requests from the dashboard work. In staging (different subdomain), the auth cookie is never sent.

**Observed Issue:**
The API sets cookies with SameSite=Lax and no Domain attribute. The dashboard is on app.company.com, the API is on api.company.com. On same-domain navigations (app → app) cookies are sent; cross-subdomain requests (app → api) don't include the cookie.

**Specific Ask:**
How do SameSite=Lax vs. Strict vs. None interact with cross-subdomain requests? Should the cookie Domain be set to .company.com to enable subdomain sharing? What are the security implications of broadening the cookie domain vs. using a proxy to make the API same-origin?""",

"""**Context:**
Our dashboard uses localStorage to cache user preferences. A console error appears intermittently: "Cannot read properties of null (reading 'getItem')."

**Code:**
```ts
const pref = localStorage.getItem('theme'); // throws in SSR
```

**Observed Issue:**
localStorage is undefined in the Node.js SSR environment. The code runs in an RSC (server) context where window and localStorage don't exist.

**Specific Ask:**
What's the correct pattern for accessing browser-only APIs (localStorage, window, document) in a Next.js codebase where the same code might run on the server? Is typeof window !== 'undefined' the correct guard? What are the gotchas with this check in Next.js specifically?""",

"""**Context:**
We added a new feature using the document object in a Next.js Middleware. The deployment pipeline throws an error in CI.

**Observed Issue:**
Middleware runs in the Edge Runtime which is not a full Node.js environment. document, window, navigator, and other browser globals are not available. The code works in local dev but breaks in production.

**Specific Ask:**
What are all the APIs unavailable in Next.js Edge Middleware vs. Node.js API routes? Is there a reliable way to catch edge runtime incompatibilities at build time rather than at CI/deployment? Can you progressively test edge compatibility of a module without manually checking every import?""",

"""**Context:**
A server-rendered date on our dashboard (formatted as "Feb 24, 2026") sometimes appears as "Feb 25, 2026" for some users.

**Observed Issue:**
The server renders in UTC (Feb 24, 23:30 UTC). Users in UTC+5:30 see "Feb 25" because the client formats the date in their local timezone, and their "local midnight" has already passed.

**Specific Ask:**
What's the correct pattern for server-rendering dates that should display consistently regardless of user timezone? Should dates always be sent as ISO strings and formatted exclusively client-side (with suppressHydrationWarning)? Or should the user's timezone be passed to the server and used for initial render?""",

"""**Context:**
We have a global search regex that's used to highlight matches in search results across multiple items.

**Code:**
```ts
const pattern = new RegExp(query, 'gi'); // global flag
items.forEach(item => {
  const match = pattern.test(item.text); // always returns alternating true/false
});
```

**Observed Issue:**
The /g flag makes RegExp stateful -- lastIndex persists between .test() calls. Every other call returns false because lastIndex advances past the match position.

**Specific Ask:**
How do you fix this without losing the global flag behavior needed for multiple matches? Is the correct fix to create a new RegExp per item, reset lastIndex manually (pattern.lastIndex = 0), or use a non-global pattern and String.match for counting? What's the performance cost of each at 5,000 items?""",

"""**Context:**
Our currency formatter displays amounts to 2 decimal places. Some entries in the report table show subtly wrong values -- "0.30" displayed as "0.29" for certain amounts.

**Observed Issue:**
0.1 + 0.2 === 0.30000000000000004 in JavaScript floating point. The formatter rounds this but some chained calculations (amount - fee - tax) accumulate enough error to show the wrong cent.

**Specific Ask:**
What's the correct approach for financial calculations in JavaScript to avoid floating point errors? Is multiplying by 100, using integer arithmetic, then dividing sufficient? Or should we use a decimal library (decimal.js, big.js)? What's the tradeoff between library overhead and correctness guarantees for a 200k DAU financial dashboard?""",

"""**Context:**
A bug report shows that adding an item to the favorites list sometimes duplicates items in other users' sessions. The bug is intermittent and only appears in production.

**Code:**
```ts
const [favorites, setFavorites] = useState(initialFavorites);

function addFavorite(item) {
  favorites.push(item); // mutating state directly
  setFavorites(favorites); // same reference
}
```

**Observed Issue:**
Direct mutation of the state array plus passing the same reference to setState causes React to sometimes not detect the change, and sometimes carry mutations across renders in unexpected ways. In React's strict mode pooling, this can affect other component instances.

**Specific Ask:**
Explain exactly why direct state mutation in React causes intermittent bugs that are hard to reproduce in development but appear in production. How does React's Object.is comparison for bailout detection interact with mutated-in-place arrays?""",

"""**Context:**
A sort operation on our report list is intermittently reversing the sort order.

**Code:**
```ts
const sorted = reports.sort((a, b) => a.date - b.date);
setReports(sorted);
```

**Observed Issue:**
Array.sort() mutates the original array in place. The sorted result is the same reference as the original. React doesn't detect a change and bails out, serving the previous render. On the next render, the sorted order may differ.

**Specific Ask:**
Beyond the obvious fix (use [...reports].sort()), how does the exact failure mode manifest? Does React ever render the mutated-in-place sorted array, or does the bail-out mean users always see the unsorted version? And what ESLint rule would catch direct array.sort without a spread?""",

"""**Context:**
We're debugging an issue where Promise.all in an API aggregation function sometimes returns results in a different order from the input array.

**Observed Issue:**
A developer on the team believes Promise.all returns results in resolution order, not input order. They restructured dependent code to wait for the "fastest" promise. Several subtle bugs emerged.

**Specific Ask:**
Does Promise.all guarantee that results are returned in the same order as the input array, regardless of resolution order? Please clarify the execution semantics. And what's the pattern for getting both the values and their resolution order when order matters -- Promise.allSettled, race conditions, or a custom ordered resolver?""",

"""**Context:**
We use AbortController to cancel fetch requests when a filter changes. The abort signal is correctly attached to the fetch, but we're seeing "AbortError: The operation was aborted" in our error reporting.

**Code:**
```ts
useEffect(() => {
  const ctrl = new AbortController();
  fetchData(filter, ctrl.signal).catch(err => {
    reportError(err); // reports AbortError as a real error
  });
  return () => ctrl.abort();
}, [filter]);
```

**Observed Issue:**
AbortErrors are expected (filter changed, cancel old request) but they're being reported as genuine errors to our error tracking system, inflating error counts.

**Specific Ask:**
How do you distinguish between an expected AbortError (user changed filter) and an unexpected fetch error in a catch block? Is err.name === 'AbortError' the correct check? And is it safe to ignore AbortErrors entirely, or could a real network error manifest as an AbortError in some scenarios?""",

"""**Context:**
A CSS class applied to a card component doesn't appear to be taking effect. DevTools shows the element has the class but the visual style isn't applied.

**Observed Issue:**
DevTools Styles panel shows the rule as crossed out with "Specificity: 0-1-0 overridden by 0-2-0." A global stylesheet has `.dashboard .card { ... }` which overrides our component's `.card { ... }`.

**Specific Ask:**
What's your systematic approach to diagnosing CSS specificity conflicts in a codebase with global styles, CSS Modules, styled-components, and Tailwind all coexisting? Is the long-term fix higher specificity classes, CSS Layers (@layer), or forcing CSS Modules to generate unique class names that can't be overridden?""",

"""**Context:**
A modal overlay should render above all other content. The modal's z-index is set to 1000, but it's appearing behind a dropdown in the header that has z-index: 50.

**Observed Issue:**
The modal is inside a parent container with transform: scale(1) applied for an animation. This creates a new stacking context, localizing all z-index values. The dropdown is in the root stacking context, so z-index: 50 (root) beats z-index: 1000 (inside transform context).

**Specific Ask:**
How do you systematically debug z-index issues caused by unexpected stacking contexts? What CSS properties besides z-index create new stacking contexts (transform, filter, opacity, will-change, isolation)? Is the fix to move the modal outside the transformed parent (via Portal), or to restructure the stacking contexts entirely?""",

"""**Context:**
A click-outside handler on a dropdown doesn't trigger when clicking certain elements.

**Code:**
```ts
document.addEventListener('click', (e) => {
  if (!dropdownRef.current?.contains(e.target)) {
    closeDropdown();
  }
});
```

**Observed Issue:**
Clicking on a label element connected to an input doesn't trigger the handler. The click fires on the label but the browser also fires a synthetic click on the associated input -- the handler sees the input click, which IS inside the dropdown, so it doesn't close.

**Specific Ask:**
How do you write a robust click-outside handler that handles: (1) label/input synthetic click pairs, (2) shadow DOM elements (e.target is the shadow host, not the inner element), and (3) SVG elements with pointer-events: none? Is there a battle-tested library pattern for click-outside that handles all these edge cases?""",

"""**Context:**
We implemented a focus trap for our modal using a custom hook. Tab key cycles focus within the modal correctly. But after closing the modal, focus returns to the document body instead of the button that opened it.

**Observed Issue:**
The return-focus-on-close logic stores a ref to document.activeElement when the modal opens, but by the time the modal closes and the ref is read, activeElement has already moved to body.

**Specific Ask:**
What's the correct timing to capture the "trigger element" for focus return on modal close? Should the trigger ref be captured before the modal opens (at the moment the open button is clicked)? How does Radix UI's Dialog handle focus return correctly, and is their approach reusable as a standalone focus-trap hook?""",

"""**Context:**
We added a keyboard shortcut (Ctrl+K) to open a command palette. It works on all Windows/Linux browsers but not on macOS Chrome.

**Observed Issue:**
On macOS, Ctrl+K is a line-deletion shortcut in some input fields. When an input is focused, the browser handles Ctrl+K before our event listener. On macOS, the user-facing shortcut should be Cmd+K.

**Specific Ask:**
How do you implement keyboard shortcuts that work correctly across OS conventions (Cmd on Mac, Ctrl on Windows)? Is e.metaKey || e.ctrlKey the correct cross-platform check? What's the pattern for keyboard shortcut management in a large React app where shortcuts might conflict with browser defaults, input field behavior, or other shortcuts in the app?""",

"""**Context:**
Our dashboard has a print view triggered by Ctrl+P. The print preview shows the page header, navigation sidebar, action buttons, and the actual report data all on one page -- the layout is unusable.

**Observed Issue:**
We have no @media print stylesheet. Every element renders as-is in the print view, including elements that should be print-only (report footer) or hidden-when-printing (nav, header, action buttons).

**Specific Ask:**
What's the correct strategy for implementing a print stylesheet in a Next.js app with CSS Modules and styled-components? Should @media print be in global.css, in the component's module, or in a dedicated print.css? How do you test print styles in CI -- can Playwright or Cypress capture a print-media render for visual regression?""",

"""**Context:**
We added @container queries to make our card component responsive to its container's width rather than the viewport. The styles aren't being applied even when the container is clearly narrower than the breakpoint.

**Code:**
```css
.card-grid {
  container-type: inline-size;
}
@container (max-width: 400px) {
  .card { flex-direction: column; }
}
```

**Observed Issue:**
The .card elements never receive the column flex direction regardless of grid width. DevTools shows the container query evaluating but the rule shows as "not applied."

**Specific Ask:**
What are the common reasons a container query fails to apply even when the container-type is set? Is there an issue with the queried container needing to be an ancestor (not the same element)? Does the .card selector inside @container need to be a descendant of .card-grid, and does it fail if .card is a direct child but the @container block doesn't have the right containment context?""",

]
